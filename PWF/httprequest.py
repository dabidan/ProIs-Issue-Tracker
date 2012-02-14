'''
Created on 11.02.2012

@author: user
'''

import re
import StringIO
import cgi
import mimetypes
from xml.etree import ElementTree as ET
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
import traceback

def encode_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

class RedirectLocation(Exception):
    def __init__(self, location):
        self.location=location

def redirect_location(location):
    raise RedirectLocation(location)

class RDFResponse(object):
    mime='application/rdf+xml'
    def __init__(self, element):
        self.element=element
        
    def __str__(self):
        s=StringIO.StringIO()
        ET.ElementTree(element=self.element).write(s)
        return s.getvalue()

class XMLResponse(object):
    mime='text/xml'
    def __init__(self, element):
        self.element=element
        
    def __str__(self):
        s=StringIO.StringIO()
        ET.ElementTree(element=self.element).write(s)
        return s.getvalue()

class TemplateResponse(object):
    mime='text/html'
    def __init__(self, filename, values):
        self.filename=filename
        self.values=values
        
    def __str__(self):
        temp=open(self.filename)
        template=temp.read().decode('utf-8')
        temp.close()
        return re.sub(r'{([A-Za-z0-9_]+)}',lambda x: self.values.get(x.group(1),''),template).encode('utf-8')

class MimeResponse(object):
    def __init__(self, string, mime='text/html'):
        self.string=string
        self.mime=mime
    def __str__(self):
        if 'text/'==self.mime[:5] and isinstance(self.string,unicode):
            return self.string.encode('utf-8') 
        return self.string
    
class FileHandler(object):
    def __init__(self, path):
        self.path=path
    def __call__(self, request, **kw):
        filename=self.path+request.normpath
        try:
            w=open(filename)
        except IOError:
            filename+='/index.html'
            w=open(filename)
        mimetype=mimetypes.types_map.get('.'+filename.split('.')[-1],'text/html') #@UndefinedVariable
        return MimeResponse(w.read(),mimetype)

class DynamicHTTPRequestHandler(BaseHTTPRequestHandler):

    def _split_path(self):
        if '?' in self.path:
            path, query = self.path.split('?',1)
        else:
            path, query = self.path, ''
        # Normalize path
        path=re.sub(r'(/+\.)*/+','/','/'+path)
        n=1
        while n>0: path,n=re.subn(r'(/[^/]+)?/\.\./','/',path,1)
        self.normpath=path
        self._handle_query(query)

    def _handle_cookies(self):
        self.cookies={}
        for cooks in self.headers.getheaders('cookie'):
            for cook in cooks.split(';'):
                key,val = map(str.strip,cook.split('=',1))
                self.cookies[key]=val

    def _handle_query(self, querystr, encoding="utf-8"):
        for q in querystr.split('&'):
            if '=' not in q: continue
            if len(self.query)>1000: break # prevent DoS-Attack ;-)
            key,val=q.split('=',1)
            self.query.setdefault(key,[]).append(urllib.unquote_plus(val).decode(encoding))

    def _dispatch(self):
        self.add_headers={}
        self.set_cookies={}
        self._handle_cookies()
        self._split_path()
        handler, multiparam = self.server.get_handler(self.normpath)
        if multiparam:
            query=self.query
        else:
            query=dict([(key,val[-1]) for key,val in self.query.iteritems()])
    
        try:
            response = handler(self, **query)
            content_type = getattr(response,'mime', 'text/html')
            response = str(response)                
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.send_header("Content-length", str(len(response)))
            for key,hh in self.add_headers.iteritems():
                self.send_header(key,hh)
            for cookie,value in self.set_cookies.iteritems():
                self.send_header('Set-Cookie', '%s=%s'%(cookie,value))
            self.end_headers()
            self.wfile.write(response)
            # shut down the connection
            self.wfile.flush()
            #self.connection.shutdown(1)
        except RedirectLocation, location:
            self.send_response(302)
            self.send_header("Location",location.location)
            #self.send_header('Refresh',' 0; url=%s'%location)
            for cookie,value in self.set_cookies.iteritems():
                self.send_header('Set-Cookie', '%s=%s'%(cookie,value))
            self.end_headers()
            self.wfile.flush()
            print "Redirect",location
        except Exception, e:
            traceback.print_exc()
            print e
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_GET(self):
        self.query={}
        self._dispatch()
     
    def do_POST(self):
        self.query={}
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            boundary=pdict['boundary']
            boundary_start='--'+boundary
            boundary_end=boundary_start+'--'
            qs=self.rfile.read(int(self.headers.getheader('content-length')))
            print qs
            st=StringIO.StringIO(qs)
            mode=1 # ignore
            header=data=None
            while True:
                line=st.readline()
                sline=line.strip()
                if sline in (boundary_start,boundary_end):
                    if mode>=3:
                        dtype, pddict = cgi.parse_header(header['content-disposition'])
                        ctype, pcdict = cgi.parse_header(header.get('content-type','text/plain'))
                        print dtype,pddict,ctype,pcdict,repr(data)
                        if dtype=='form-data':
                            if 'content-length' not in header:
                                if data[-2:]=='\r\n': data=data[:-2]
                                elif data[-1:]=='\n': data=data[:-1]
                            if 'filename' in pddict:
                                self.query.setdefault(pddict['name'],[]).append((pddict['filename'],ctype,pcdict.get('charset'),data))
                            else:
                                self.query.setdefault(pddict['name'],[]).append(data.decode(pcdict.get('charset','utf-8')))
                        else: pass
                    if sline==boundary_start:
                        mode=2
                        header={}
                        data=""
                    else: break
                elif mode==2:
                    if not sline:
                        if 'content-length' in header:
                            data=st.read(int(header['content-length']))
                            mode=4
                        else:
                            mode=3
                    else:
                        head, text=sline.split(':')
                        header[head.strip().lower()]=text.strip()
                elif mode==3:
                    data+=line
        elif ctype == 'application/x-www-form-urlencoded':
            qs=self.rfile.read(int(self.headers.getheader('content-length')))
            self._handle_query(qs, encoding = pdict.get('charset','utf-8'))
        self._dispatch()


class DynamicHTTPServer(HTTPServer):
    protocol_version = "HTTP/1.1"

    def __init__(self, server_address):
        HTTPServer.__init__(self, server_address,DynamicHTTPRequestHandler)
        self.filedb=[]
        
    def add_script(self, path_re, handler, multiparam=False):
        self.filedb.append((re.compile('^'+path_re+'$'),handler,multiparam))
        
    def get_handler(self, path):
        for path_re,handler,multiparam in self.filedb:
            if path_re.match(path):
                return handler, multiparam
        return None, False
        