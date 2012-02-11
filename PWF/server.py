'''
Created on 07.02.2012

@author: user
'''
import time
import httprequest
from httprequest import RDFResponse, XMLResponse, RedirectLocation
import database
from database import dbfield, DBRecord, dbtable, Database
from xml.etree import ElementTree as ET
import hashlib
import base64
import random
import os
import re





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

class Project(DBRecord):
    pid=dbfield('pid','INTEGER','PRIMARY KEY AUTOINCREMENT')
    project_id=dbfield('project_id','TEXT','UNIQUE')
    name=dbfield('project_name','TEXT')
    description=dbfield('project_description','TEXT')
    creator=dbfield('creator','TEXT')
    creatorion_date=dbfield('creation_date','TEXT')

class User(DBRecord):
    uid=dbfield('user_id','INTEGER','PRIMARY KEY AUTOINCREMENT')
    login=dbfield('user_login','TEXT','UNIQUE')
    passwd=dbfield('user_passwd','TEXT')
    name=dbfield('user_name','TEXT')
    email=dbfield('user_email','TEXT')
    flags=dbfield('user_flags','TEXT')

    @staticmethod
    def mkpasswd(passwd, salt=None):
        if salt is None: salt=os.urandom(8)
        x=hashlib.sha256(passwd+salt)
        return base64.b64encode(salt+x.digest())
    
    def checkpasswd(self, passwd):
        pwd=base64.b64decode(self.passwd)
        return self.passwd==self.mkpasswd(passwd, salt=pwd[:8])

class IssueBase(Database):
    users=dbtable('Users',User)
    

issuebase=IssueBase('test.db')

class Session(object):
    sessions={}
    
    def __init__(self, request):
        login=request.query.get('Bugzilla_login')[-1]
        passwd=request.query.get('Bugzilla_password')[-1]
        user=issuebase.users.query_one(login=login)
        if user is None: raise KeyError("Login not found")
        if not user.checkpasswd(passwd): raise AssertionError("Password wrong")
        while True:
            cookie=base64.b64encode(os.urandom(6))
            if self is self.sessions.setdefault(cookie,self):
                break
        self.expire=time.time()+3600
        self.user=user
        request.set_cookies['Bugzilla_login']='yes'
        request.set_cookies['Bugzilla_logincookie']=cookie
    
    @classmethod
    def get_session(cls, request):
        tt=time.time()
        for cookie,session in cls.sessions.items():
            if session.expire<tt: del cls.sessions[cookie]
        result=cls.sessions.get(request.cookies.get('Bugzilla_logincookie'))
        if result is not None:
            result.expire=tt+3600
        return result


def do_index(request, Bugzilla_login=None, **kw):
    if Bugzilla_login:
        try:
            session=Session(request)
        except (KeyError, AssertionError):
            return "<html><body>Wrong login/password</body></html>"
    else:
        session=Session.get_session(request)
        if session is None: return "<html><body>Not logged in!</body></html>"
    return "<html><body>MyLyn-Interface</body></html>"

def do_config(request, ctype=None):
    session=Session.get_session(request)
    if session is None: return "<html><body>Not logged in!</body></html>"

    if ctype=='rdf':
        config=Configuration()
        return RDFResponse(config.to_xml())

def do_buglist(request, **kw):
    session=Session.get_session(request)
    if session is None: return "<html><body>Not logged in!</body></html>"

    print kw
    config=BugList()
    return RDFResponse(config.to_xml())

def do_show_bug(request, ctype=None, **kw):
    session=Session.get_session(request)
    if session is None: return "<html><body>Not logged in!</body></html>"

    print kw
    if ctype=='xml':
        config=BugList()
        return XMLResponse(config.bugs[0].show_xml())
    return "xxx"

def do_process_bug(request, **kw):
    session=Session.get_session(request)
    if session is None: return "<html><body>Not logged in!</body></html>"

    print kw
    pass
        
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

def do_login(request, login=None, Bugzilla_login=None, Bugzilla_password=None, realname=None, email=None, **kw):
    error=None;script=None
    if login=='Register':
        try:
            u=issuebase.users.new(login=Bugzilla_login, passwd=User.mkpasswd(Bugzilla_password), name=realname, email=email)
            u.commit()
            login='login'
        except:
            error="""<div class="alert alert-error">Username already used! Choose another one</div>"""
            script="""
            $('#demo').collapse('toggle')
            $('#Bugzilla_login').parent().parent().addClass('error')
            $('#Bugzilla_login').after('<span class="help-inline">Try another</span>')
            $('#Bugzilla_login').val(%r)
            $('#Bugzilla_password').val(%r)
            $('#realname').val(%r)
            $('#email').val(%r)
            """%(Bugzilla_login,Bugzilla_password,realname,email)
    if login=='login':
        try:
            session=Session(request)
            raise RedirectLocation('/index.html')
        except (KeyError, AssertionError), e:
            print e
            pass
        error="""<div class="alert alert-error">Invalid login or password!</div>"""
    w=open('templates/login.html')
    response=w.read()
    if error:
        response=re.sub(r'<!-- insert message -->',error,response)
    if script:
        response=re.sub(r'/\* insert script \*/',script,response)
    return response

def main():
    server = httprequest.DynamicHTTPServer(('', 5080))
    server.add_script('/_mylyn(/index\.cgi|/)?', do_index, multiparam=False)
    server.add_script('/_mylyn/relogin\.cgi', do_index, multiparam=False)
    server.add_script('/_mylyn/config\.cgi', do_config, multiparam=False)
    server.add_script('/_mylyn/buglist\.cgi', do_buglist, multiparam=False)
    server.add_script('/_mylyn/show_bug\.cgi', do_show_bug, multiparam=False)
    server.add_script('/_mylyn/process_bug\.cgi', do_process_bug, multiparam=False)
    server.add_script('/_mylyn/.*', lambda: None, multiparam=False)
    # raise error for anythinh else in _mylyn
    
    server.add_script('/login\.html',do_login)
    server.add_script('/.*',httprequest.FileHandler('htdocs'))
    
    try:
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
