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

def encode_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

class RedirectLocation(Exception):
    def __init__(self, location):
        self.location=location

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
        template=temp.read()
        temp.close()
        return re.sub(r'{([A-Za-z0-9_]+)}',lambda x: self.values.get(x.group(1),''),template)

class MimeResponse(object):
    def __init__(self, string, mime='text/html'):
        self.string=string
        self.mime=mime
    def __str__(self):
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
        self.query = cgi.parse_qs(query, keep_blank_values=True)

    def _handle_cookies(self):
        self.cookies={}
        for cooks in self.headers.getheaders('cookie'):
            for cook in cooks.split(';'):
                key,val = map(str.strip,cook.split('=',1))
                self.cookies[key]=val

    def _dispatch(self, query={}):
        self.set_cookies={}
        self._handle_cookies()
        self._split_path()
        for key, val in query.iteritems():
            if key in self.query:
                self.query.extend(val)
            else:
                self.query[key]=val
        
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
            print e
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_GET(self):
        self._dispatch()
     
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            query=cgi.parse_multipart(self.rfile, pdict)
        else:
            qs=self.rfile.read(int(self.headers.getheader('content-length')))
            query = cgi.parse_qs(qs, keep_blank_values=True)
        self._dispatch(query)


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
        