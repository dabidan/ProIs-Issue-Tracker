'''
Created on 07.02.2012

@author: user
'''
import string,cgi,time
import re
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri

from xml.etree import ElementTree as ET
import StringIO





XMLNS_rdf="{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
XMLNS_bz="{http://www.bugzilla.org/rdf#}"

host="http://localhost:5080/"


class Product(object):
    name="Test-Produkt"
    allows_unconfirmed='1'
    components=['main','utils']
    versions=['0.9']
    milestone=['goal']
    
    def __init__(self):
        pass
    
    def to_xml(self):
        result=ET.Element(XMLNS_bz+'product',
            attrib={XMLNS_rdf+'about':host+'product.cgi?name='+self.name})
        ET.SubElement(result,XMLNS_bz+'name').text=self.name
        ET.SubElement(result,XMLNS_bz+'allows_unconfirmed').text=self.allows_unconfirmed
        components=ET.SubElement(result,XMLNS_bz+'components')
        seq=ET.SubElement(components,XMLNS_rdf+'Seq')
        for comp in self.components:
            ET.SubElement(seq,XMLNS_rdf+'li',resource=host+'component.cgi?name=%s&product=%s'%(comp,self.name))
        versions=ET.SubElement(result,XMLNS_bz+'versions')
        seq=ET.SubElement(versions,XMLNS_rdf+'Seq')
        for comp in self.versions:
            ET.SubElement(seq,XMLNS_rdf+'li',resource=host+'version.cgi?name=%s&product=%s'%(comp,self.name))
        milestone=ET.SubElement(result,XMLNS_bz+'target_milestones')
        seq=ET.SubElement(milestone,XMLNS_rdf+'Seq')
        for comp in self.milestone:
            ET.SubElement(seq,XMLNS_rdf+'li',resource=host+'milestone.cgi?name=%s&product=%s'%(comp,self.name))
        return result

class Configuration(object):
    
    status_open=['unconfirmed','confirmed','in progress']
    status_closed=['resolved','tested','rejected']
    resolution=['','fixed','invalid',"won't fix",'duplicate',"work's for me"]
    keyword=['new','funny','mystery']
    platform=['PC','any']
    op_sys=['','Linux','Windows']
    priority=['low','medium','high','critical']
    severity=['enhancement','trivial','minor','normal','fatal']
    
    products=[Product()]
    
    def __init__(self):
        pass
    
    def to_xml(self):
        result=ET.Element(XMLNS_rdf+'RDF')
        installation=ET.SubElement(result, XMLNS_bz+'installation',
            attrib={XMLNS_rdf+'about':host})
        ET.SubElement(installation,XMLNS_bz+'install_version').text='4.3'
        ET.SubElement(installation,XMLNS_bz+'maintainer').text='ich@hier.de'
        installation.append(self._make_list('status', self.status_open+self.status_closed))
        installation.append(self._make_list('status_open', self.status_closed))
        installation.append(self._make_list('status_closed', self.status_open))
        for name in ('resolution','keyword','platform','op_sys','priority','severity'):
            installation.append(self._make_list(name, getattr(self,name)))

        products=ET.SubElement(result,XMLNS_bz+'products')
        seq=ET.SubElement(products,XMLNS_rdf+'Seq')
        for prod in self.products:
            ET.SubElement(seq,XMLNS_rdf+'li').append(prod.to_xml())

        components=ET.SubElement(result,XMLNS_bz+'components')
        seq=ET.SubElement(components,XMLNS_rdf+'Seq')
        for prod in self.products:
            for comp in prod.components:
                li=ET.SubElement(seq,XMLNS_rdf+'li')
                c=ET.SubElement(li,XMLNS_bz+'component', attrib={
                    XMLNS_rdf+'about':host+'component.cgi?name=%s&product=%s'%(comp,prod.name)})
                ET.SubElement(c,XMLNS_bz+'name').text=comp
        return result

    def _make_list(self, name, list):
        result=ET.Element(XMLNS_bz+name)
        seq=ET.SubElement(result,XMLNS_rdf+'Seq')
        for elem in list:
            ET.SubElement(seq,XMLNS_rdf+'li').text=elem
        return result

class BugEntry(object):
    id='124'
    product='Test-Produkt'
    short_desc='Keine Fehler'
    creation_ts='2007-12-03 06:25:00 -0800'
    
    def __init__(self):
        pass
    
    def to_xml(self):
        result=ET.Element(XMLNS_bz+'product',
            attrib={XMLNS_rdf+'about':host+'show_bug.cgi?id='+self.id})
        ET.SubElement(result,XMLNS_bz+'id').text=self.id
        ET.SubElement(result,XMLNS_bz+'product').text=self.product
        ET.SubElement(result,XMLNS_bz+'short_desc').text=self.short_desc
        return result

        """<bz:bug rdf:about="http://localhost:5080/show_bug.cgi?id=6155">
          <bz:id nc:parseType="Integer">6155</bz:id>
          <bz:product>WorldControl</bz:product>
          <bz:component>EconomicControl</bz:component>
          <bz:assigned_to>tara</bz:assigned_to>
          <bz:bug_status>UNCONFIRMED</bz:bug_status>
          <bz:resolution></bz:resolution>
          <bz:short_desc>Test bug attachment</bz:short_desc>
          <bz:changeddate>2011-07-02</bz:changeddate>
        </bz:bug>"""

    def show_xml(self):
        result=ET.Element('bugzilla',version="4.3")
        bug=ET.SubElement(result, 'bug')
        ET.SubElement(bug,'bug_id').text=self.id
        ET.SubElement(bug, 'creation_ts').text=self.creation_ts
        ET.SubElement(bug, 'reporter_accessible').text='1'
        ET.SubElement(bug, 'cclist_accessible').text='1'
        ET.SubElement(bug, 'classification_id').text='1'
        ET.SubElement(bug, 'classification').text='sdad'
        ET.SubElement(bug, 'product').text=self.product
        ET.SubElement(bug, 'short_desc').text=self.short_desc
        return result
"""<bugzilla version="4.3"
          <creation_ts>2007-12-03 06:25:00 -0800</creation_ts>
          <short_desc>Test bug attachment</short_desc>
          <delta_ts>2011-07-02 12:13:13 -0700</delta_ts>
          <reporter_accessible>1</reporter_accessible>
          <cclist_accessible>1</cclist_accessible>
          <classification_id>2</classification_id>
          <classification>Mercury</classification>
          <product>WorldControl</product>
          <component>EconomicControl</component>
          <version>1.0</version>
          <rep_platform>PC</rep_platform>
          <op_sys>Windows XP</op_sys>
          <bug_status>UNCONFIRMED</bug_status>
          <resolution></resolution>
          
          
          <bug_file_loc></bug_file_loc>
          <status_whiteboard></status_whiteboard>
          <keywords></keywords>
          <priority>P2</priority>
          <bug_severity>normal</bug_severity>
          <target_milestone>World 2.0</target_milestone>
          
          
          <everconfirmed>0</everconfirmed>
          <reporter>alen</reporter>
          <assigned_to name="Tara Hernandez">tara</assigned_to>
          <cc>sepp.renfer</cc>
          <long_desc isprivate="0">
            <commentid>11119</commentid>
            <who name="">alen</who>
            <bug_when>2007-12-03 06:25:45 -0800</bug_when>
            <thetext>test123

http://www.croteam.com</thetext>
          </long_desc>
          <long_desc isprivate="0">
            <commentid>11120</commentid>
              <attachid>982</attachid>
            <who name="">alen</who>
            <bug_when>2007-12-03 06:28:23 -0800</bug_when>
            <thetext>Created attachment 982
blah</thetext>
          </long_desc>
          <long_desc isprivate="0">
            <commentid>22575</commentid>
            <who name="">sepp.renfer</who>
            <bug_when>2011-07-02 12:13:13 -0700</bug_when>
            <thetext>sadasd</thetext>
          </long_desc>
      
          <attachment
              isobsolete="0"
              ispatch="0"
              isprivate="0"
          >
            <attachid>982</attachid>
            <date>2007-12-03 06:28:00 -0800</date>
            <delta_ts>2007-12-03 06:28:23 -0800</delta_ts>
            <desc>blah</desc>
            <filename>testatt.txt</filename>
            <type>text/plain</type>
            <size>22</size>
            <attacher>alen</attacher>
            
              <data encoding="base64">dGVzdGluZyB0ZXN0aW5nIDEyMyENCg==
</data>

          </attachment>
    </bug>
</bugzilla>"""

class BugList(object):
    url='buglist.cgi?query=xyz'
    bugs=[BugEntry()]
    
    def __init__(self):
        pass
    
    def to_xml(self):
        result=ET.Element(XMLNS_rdf+'result',
            attrib={XMLNS_rdf+'about':host+self.url})
        installation=ET.SubElement(result, XMLNS_bz+'installation',
            attrib={XMLNS_rdf+'about':host})
        ET.SubElement(installation,XMLNS_bz+'query_timestamp').text=str(time.localtime())
        bugs=ET.SubElement(result,XMLNS_bz+'bugs')
        seq=ET.SubElement(bugs,XMLNS_rdf+'Seq')
        for bug in self.bugs:
            ET.SubElement(seq,XMLNS_rdf+'li').append(bug.to_xml())
        
        return result

    def _make_list(self, name, list):
        result=ET.Element(XMLNS_bz+name)
        seq=ET.SubElement(result,XMLNS_rdf+'Seq')
        for elem in list:
            ET.SubElement(seq,XMLNS_rdf+'li').text=elem
        return result



class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        m=re.match(r"(.*?)/([^/?]*)(\?.*)?$",self.path)
        print m.groups()
        xpath=m.group(1)
        xfilename=m.group(2) or 'index.cgi'
        xquery=(m.group(3) or '?')[1:]
        try:
            if xfilename.endswith(".html"):
                f = open(curdir + sep + xpath+'/'+xfilename) #self.path has /test.html
#note that this potentially makes every file on your computer readable by the internet

                self.send_response(200)
                self.send_header('Content-type',        'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if xfilename.endswith(".cgi"):   #our dynamic content
                query = cgi.parse_qs(xquery or '', keep_blank_values=True)
                self._dispatch(xfilename, query)
                return
                
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
        except int: #AttributeError:
            print "Not found:",xfilename
            print query
     

    def do_POST(self):
        m=re.match(r"(.*?)/([^/?]*)(\?.*)?$",self.path)
        print m.groups()
        xpath=m.group(1)
        xfilename=m.group(2) or 'index.cgi'
        xquery=m.group(3)
        
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            else:
                qs=self.rfile.read(int(self.headers.getheader('content-length')))
                query = cgi.parse_qs(qs, keep_blank_values=True)
            self._dispatch(xfilename, query)
        except AttributeError, e:
            print "POST", query
            print e

    def _dispatch(self, xfilename,query):
        self.cookies={}
        for cooks in self.headers.getheaders('cookie'):
            for cook in cooks.split(';'):
                key,val = map(str.strip,cook.split('=',1))
                self.cookies[key]=val
        print "Cookies:",self.cookies
        self.set_cookies={}
        self.content_type='text/html'
        response=getattr(self,'do_%s'%xfilename[:-4])(**query)
        self.send_response(200)
        self.send_header("Content-type", self.content_type)
        self.send_header("Content-length", str(len(response)))
        for cookie,value in self.set_cookies.iteritems():
            self.send_header('Set-Cookie', '%s=%s'%(cookie,value))
        self.end_headers()
        self.wfile.write(response)
        # shut down the connection
        self.wfile.flush()
        self.connection.shutdown(1)


    def do_index(self, **kw):
        print kw
        self.set_cookies['Bugzilla_login']='34'
        self.set_cookies['Bugzilla_logincookie']='xyz'
        self.content_type='text/html'
        return "<html><body>MyLyn-Interface</body></html>"
        #f=open('land/index.cgi')
        #self.wfile.write(f.read())
        #f.close()

    def do_config(self, ctype=None):
        if ctype==['rdf']:
            self.content_type='application/rdf+xml'
            config=Configuration()
            s=StringIO.StringIO()
            ET.ElementTree(element=config.to_xml()).write(s)
            return s.getvalue()

    def do_buglist(self, **kw):
        print kw
        self.content_type='application/rdf+xml'
        config=BugList()
        s=StringIO.StringIO()
        ET.ElementTree(element=config.to_xml()).write(s)
        return s.getvalue()
        #f=open('buglist.rdf')
        #self.wfile.write(f.read())
        #f.close()

    def do_show_bug(self, **kw):
        print kw
        if kw.get('ctype')==['xml']:
            self.content_type='application/xml'
            config=BugList()
            s=StringIO.StringIO()
            ET.ElementTree(element=config.bugs[0].show_xml()).write(s)
            return s.getvalue()
        return "xxx"
        #f=open('show_bug.cgi?id=6155&ctype=xml')
        #self.wfile.write(f.read())
        #f.close()

    def do_relogin(self, **kw):
        self.do_index(**kw);return
        print kw
        self.send_response(200)
        self.send_header('Content-type',        'text/html')
        self.end_headers()
        self.wfile.write("hey, today is the" + str(time.localtime()[7]))
        self.wfile.write(" day in the year " + str(time.localtime()[0]))

    def do_process_bug(self, **kw):
        guut
        
{'addselfcc': ['1'], 'classification_id': ['1'], 
'reporter_accessible': ['1'], 'set_default_assignee': ['1'], 
'classification': ['cl'], 
'status_whiteboard': ['ja da war mal was!\t\t'], 
'bug_file_loc': ['uu'], 'rep_platform': ['PC'], 'dup_id': [''], 
'new_comment': ['Neuer Komet'], 'keywords': ['funny, mystery'], 
'id': ['124'], 'blocked': ['bl'], 
'cclist_accessible': ['1'], 'bug_status': ['ASSIGNED'], 
'short_desc': ['Keine Fehler'], 'priority': ['medium'],
 'version': [''], 'newcc': ['du'], 'product': ['Test-Produkt'], 
 'bug_severity': ['trivial'], 'qa_contact': ['dabi2'], 
 'see_also': [''], 'longdesclength': ['1'], 'component': ['main'], 
 'bug_id': ['124'], 'dependson': ['dp'], 'comment': ['Neuer Komet'], 
 'op_sys': ['Linux'], 'alias': [''], 'assigned_to': ['dabi'], 
 'form_name': ['process_bug'], 'resolution': [''], 
 'resolutionInput': ['fixed']}


def main():
    try:
        server = HTTPServer(('', 5080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
