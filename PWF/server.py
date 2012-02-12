'''
Created on 07.02.2012

@author: user
'''
import time
import httprequest
from httprequest import RDFResponse, XMLResponse, RedirectLocation, TemplateResponse, encode_html,\
    MimeResponse
import database
from database import dbfield, DBRecord, dbtable, Database
from xml.etree import ElementTree as ET
import hashlib
import base64
import os
import re
import datetime





XMLNS_rdf="{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
XMLNS_bz="{http://www.bugzilla.org/rdf#}"

class Configuration(object):
    status_open=['unconfirmed','confirmed','in progress']
    status_closed=['resolved','tested','rejected']
    resolution=['','fixed','invalid',"won't fix",'duplicate',"work's for me"]
    keyword=[]
    platform=['any']
    op_sys=['any']
    priority=['low','medium','high','critical']
    severity=['enhancement','trivial','minor','normal','fatal']
    
    def __init__(self):
        pass
    
    def to_xml(self, host):
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
        for prod in issuebase.projects:
            ET.SubElement(seq,XMLNS_rdf+'li').append(prod.to_xml(host))

        components=ET.SubElement(result,XMLNS_bz+'components')
        seq=ET.SubElement(components,XMLNS_rdf+'Seq')
        for prod in issuebase.projects:
            li=ET.SubElement(seq,XMLNS_rdf+'li')
            c=ET.SubElement(li,XMLNS_bz+'component', attrib={
                XMLNS_rdf+'about':host+'_mylyn/component.cgi?name=%s&product=%s'%('unspecified',prod.project_id)})
            ET.SubElement(c,XMLNS_bz+'name').text='<unspecified>'
        components=ET.SubElement(result,XMLNS_bz+'versions')
        seq=ET.SubElement(components,XMLNS_rdf+'Seq')
        for prod in issuebase.projects:
            li=ET.SubElement(seq,XMLNS_rdf+'li')
            c=ET.SubElement(li,XMLNS_bz+'version', attrib={
                XMLNS_rdf+'about':host+'_mylyn/version.cgi?name=%s&product=%s'%('unspecified',prod.project_id)})
            ET.SubElement(c,XMLNS_bz+'name').text='<unspecified>'
        return result

    def _make_list(self, name, list):
        result=ET.Element(XMLNS_bz+name)
        seq=ET.SubElement(result,XMLNS_rdf+'Seq')
        for elem in list:
            ET.SubElement(seq,XMLNS_rdf+'li').text=elem
        return result

class Issue(DBRecord):
    iid=dbfield('iid','INTEGER','PRIMARY KEY AUTOINCREMENT')
    project_id=dbfield('project_id','INTEGER')
    creator_id=dbfield('creator_id','INTEGER')
    creation_date=dbfield('creation_date','TEXT')
    modification_date=dbfield('modification_date','TEXT')
    assignee_id=dbfield('assigned_id','INTEGER')
    title=dbfield('title','TEXT')
    bug_status=dbfield('status','TEXT')
    resolution=dbfield('resolution','TEXT')
    bug_file_loc=dbfield('bug_file_loc','TEXT')
    status_whiteboard=dbfield('status_whiteboard','TEXT')
    priority=dbfield('priority','TEXT')
    bug_severity=dbfield('severity','TEXT')
    bug_file_loc=dbfield('bug_file_loc','TEXT')
    
    #comment=dbfield('comment','TEXT')

    def to_short_xml(self, host):
        result=ET.Element(XMLNS_bz+'product',
            attrib={XMLNS_rdf+'about':host+'show_bug.cgi?id=%s'%self.iid})
        ET.SubElement(result,XMLNS_bz+'id').text=str(self.iid)
        ET.SubElement(result,XMLNS_bz+'product').text=issuebase.projects[self.project_id].name
        ET.SubElement(result,XMLNS_bz+'component').text='<unspecified>'
        ET.SubElement(result,XMLNS_bz+'assigned_to').text=issuebase.users[self.assignee_id].name if self.assignee_id is not None else "unassigned"
        ET.SubElement(result,XMLNS_bz+'bug_status').text=self.bug_status or ''
        ET.SubElement(result,XMLNS_bz+'resolution').text=self.resolution or ''
        ET.SubElement(result,XMLNS_bz+'short_desc').text=self.title
        ET.SubElement(result,XMLNS_bz+'changeddate').text=self.creation_date
        return result

    def to_xml(self, host):
        result=ET.Element('bugzilla',version="4.3")
        bug=ET.SubElement(result, 'bug')
        ET.SubElement(bug,'bug_id').text=str(self.iid)
        ET.SubElement(bug, 'creation_ts').text=self.creation_date
        ET.SubElement(bug, 'delta_ts').text=self.modification_date
        ET.SubElement(bug, 'reporter').text=issuebase.users[self.creator_id].name
        if self.assignee_id is not None:
            ass=issuebase.users[self.assignee_id]
            ET.SubElement(bug, 'assigned_to', name=ass.name).text=ass.login
        ET.SubElement(bug, 'reporter_accessible').text='1'
        ET.SubElement(bug, 'cclist_accessible').text='1'
        ET.SubElement(bug, 'classification_id').text='1'
        ET.SubElement(bug, 'everconfirmed').text='1'
        ET.SubElement(bug, 'classification').text='unspecified'
        ET.SubElement(bug, 'product').text=issuebase.projects[self.project_id].name
        ET.SubElement(bug, 'component').text='<unspecified>'
        ET.SubElement(bug, 'version').text='<unspecified>'
        ET.SubElement(bug, 'rep_platform').text='any'
        ET.SubElement(bug, 'short_desc').text=self.title
        ET.SubElement(bug, 'op_sys').text='any'
        for elem in ('bug_status','resolution','bug_file_loc','status_whiteboard','priority','bug_severity'):
            txt=getattr(self,elem)
            if txt: ET.SubElement(bug, elem).text=txt
        for cmt in issuebase.comments.query_iter(issue_id=self.iid):
            bug.append(cmt.to_xml())
        return result
"""<bugzilla version="4.3"
          <keywords></keywords>
          <target_milestone>World 2.0</target_milestone>
          <cc>sepp.renfer</cc>
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
              <data encoding="base64">dGVzdGluZyB0ZXN0aW5nIDEyMyENCg==</data>
          </attachment>
    </bug>
</bugzilla>"""


class Comment(DBRecord):
    cid=dbfield('cid','INTEGER','PRIMARY KEY AUTOINCREMENT')
    issue_id=dbfield('issue_id','INTEGER')
    is_private=dbfield('is_private','INTEGER')
    creator_id=dbfield('creator_id','INTEGER')
    creation_date=dbfield('creation_date','TEXT')
    text=dbfield('text','TEXT')

    def to_xml(self):
        result=ET.Element('long_desc', isprivate=str(self.is_private))
        ET.SubElement(result,'commentid').text=str(self.cid)
        # <attachid>982</attachid>
        if self.creator_id is not None:
            cc=issuebase.users[self.creator_id]
            ET.SubElement(result,'who',name=cc.name).text=cc.login
        ET.SubElement(result,'bug_when').text=self.creation_date
        ET.SubElement(result,'thetext').text=self.text
        return result

class Project(DBRecord):
    pid=dbfield('pid','INTEGER','PRIMARY KEY AUTOINCREMENT')
    project_id=dbfield('project_id','TEXT','UNIQUE')
    name=dbfield('project_name','TEXT')
    description=dbfield('project_description','TEXT')
    icon=dbfield('project_icon','BLOB')
    creator=dbfield('creator','TEXT')
    creation_date=dbfield('creation_date','TEXT')

    def to_xml(self, host):
        result=ET.Element(XMLNS_bz+'product',
            attrib={XMLNS_rdf+'about':host+'_mylyn/product.cgi?name='+self.project_id})
        ET.SubElement(result,XMLNS_bz+'name').text=self.name
        ET.SubElement(result,XMLNS_bz+'allows_unconfirmed').text='1'
        components=ET.SubElement(result,XMLNS_bz+'components')
        seq=ET.SubElement(components,XMLNS_rdf+'Seq')
        ET.SubElement(seq,XMLNS_rdf+'li',resource=host+'_mylyn/component.cgi?name=%s&product=%s'%('unspecified',self.project_id))
        versions=ET.SubElement(result,XMLNS_bz+'versions')
        seq=ET.SubElement(versions,XMLNS_rdf+'Seq')
        ET.SubElement(seq,XMLNS_rdf+'li',resource=host+'_mylyn/version.cgi?name=%s&product=%s'%('unspecified',self.project_id))
        milestone=ET.SubElement(result,XMLNS_bz+'target_milestones')
        seq=ET.SubElement(milestone,XMLNS_rdf+'Seq')
        ET.SubElement(seq,XMLNS_rdf+'li',resource=host+'_mylyn/milestone.cgi?name=%s&product=%s'%('unspecified',self.project_id))
        return result


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
    projects=dbtable('Projects',Project)
    issues=dbtable('Issues',Issue)
    comments=dbtable('Comments',Comment)
    

issuebase=IssueBase('test.db')
#issuebase.drop_all()
#issuebase.cursor().execute("drop table Issues")
issuebase.create_tables()

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
        else:
            request.set_cookies['Bugzilla_login']=''
            request.set_cookies['Bugzilla_logincookie']=''
        return result


def do_mylyn_index(request, Bugzilla_login=None, **kw):
    if Bugzilla_login:
        try:
            session=Session(request)
        except (KeyError, AssertionError):
            return "<html><body>Wrong login/password</body></html>"
    else:
        session=Session.get_session(request)
        if session is None: return "<html><body>Not logged in!</body></html>"
    return "<html><body>MyLyn-Interface</body></html>"

def do_mylyn_config(request, ctype=None):
    #session=Session.get_session(request)
    #if session is None: return "<html><body>Not logged in!</body></html>"
    if ctype=='rdf':
        config=Configuration()
        return RDFResponse(config.to_xml(request.headers.getheader('host')))

def do_mylyn_buglist(request, **kw):
    #session=Session.get_session(request)
    #if session is None: return "<html><body>Not logged in!</body></html>"
    print kw
    host=request.headers.getheader('host')
    buglist=ET.Element(XMLNS_rdf+'result',
            attrib={XMLNS_rdf+'about':host+request.path})
    installation=ET.SubElement(buglist, XMLNS_bz+'installation',
            attrib={XMLNS_rdf+'about':host})
    ET.SubElement(installation,XMLNS_bz+'query_timestamp').text=str(datetime.datetime.now())
    bugs=ET.SubElement(buglist,XMLNS_bz+'bugs')
    seq=ET.SubElement(bugs,XMLNS_rdf+'Seq')
    for bug in issuebase.issues:
        ET.SubElement(seq,XMLNS_rdf+'li').append(bug.to_short_xml(host))
    return RDFResponse(buglist)

def do_mylyn_show_bug(request, ctype=None, id=None, **kw):
    #session=Session.get_session(request)
    #if session is None: return "<html><body>Not logged in!</body></html>"
    print kw
    if ctype=='xml':
        issue=issuebase.issues[int(id)]
        return XMLResponse(issue.to_xml(request.headers.getheader('host')))
    return "xxx"

def do_mylyn_process_bug(request, **kw):
    session=Session.get_session(request)
    print session
    #if session is None: return "<html><body>Not logged in!</body></html>"
    if kw['bug_id']!=kw['id']: raise "Internal Error"
    iid=int(kw['id'])
    iss=issuebase.issues[iid]
    iss.modification_date=str(datetime.datetime.now()).split('.')[0]
    ass=issuebase.users.query_one(login=kw['assigned_to'])
    if ass is not None:
        iss.assignee_id=ass.uid
    pro=issuebase.projects.query_one(name=kw['product'])
    if pro is not None:
        iss.project_id=pro.pid
    if kw.get('short_desc'):
        iss.title = kw['short_desc']
    for elem in ('bug_status','resolution','bug_file_loc','status_whiteboard','priority','bug_severity'):
        if elem in kw:
            setattr(iss,elem,kw[elem])
    iss.commit()
    
    if 'new_comment' in kw:
        cmt=issuebase.comments.new()
        cmt.issue_id=iss._rowid
        cmt.is_private=0
        cmt.creator_id=session.user.uid if session else None
        cmt.creation_date=str(datetime.datetime.now()).split('.')[0]
        cmt.text=kw['new_comment']
        cmt.commit()
        
    print kw
    for elem in (
        # used
        'bug_id','id','assigned_to','product','short_desc','new_comment',
        'bug_status','resolution','bug_file_loc','status_whiteboard','priority','bug_severity',
        # ignored
        'classification_id','classification','rep_platform','cclist_accessible',
        'reporter_accessible','form_name','op_sys','version','keywords','blocked',
        'everconfirmed','delta_ts','dependson','assigned_to_name','component',
        ):
        if elem in kw: kw.pop(elem)    
    print kw
    
    issue=issuebase.issues[iid]
    return XMLResponse(issue.to_xml(request.headers.getheader('host')))
#    return "<html><body>ok</body></html>"
        
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


def do_list(request,**kw):
    session=Session.get_session(request)
    if session:
        values={'user': '%s <a href="/logout.html">(logout)</a>'%encode_html(session.user.name)}
    else:
        values={'user': 'anonymous <a href="/login.html">(login)</a>'}

    list=""    
    for prj in issuebase.projects:
        list+="""<li class="span4">
      <a class="thumbnail" href="/projects/%s/">
      <table><tr><td valign="top"><img src="/projects/%s/icon.jpg" width='64' height='64' alt=""></td><td style="padding-left:5px;color:black">
      <h5>%s</h5>
      <p>%s</p>
      </td></tr></table></a>
      </li>"""%(prj.project_id,prj.project_id,encode_html(prj.name),encode_html(prj.description))
    values['list']=list
    return TemplateResponse('templates/list.html',values)

def do_login(request, hint=None, login=None, Bugzilla_login=None, Bugzilla_password=None, realname=None, email=None, **kw):
    values={}
    if hint=='1':
        values['message']="""<div class="alert">To create a new project you need to login.</div>"""
    if login=='Register':
        try:
            u=issuebase.users.new(login=Bugzilla_login, passwd=User.mkpasswd(Bugzilla_password), name=realname, email=email)
            u.commit()
            login='login'
        except:
            values['message']="""<div class="alert alert-error">Username already used! Choose another one</div>"""
            values['Bugzilla_login']=Bugzilla_login
            values['Bugzilla_password']=Bugzilla_password
            values['realname']=realname
            values['email']=email
            values['script']="""
            $('#demo').collapse('toggle')
            $('#Bugzilla_login').parent().parent().addClass('error')
            $('#Bugzilla_login').after('<span class="help-inline">Try another</span>')
            """
    if login=='login':
        try:
            session=Session(request)
            raise RedirectLocation('/index.html')
        except (KeyError, AssertionError), e:
            print e
            pass
        values['message']="""<div class="alert alert-error">Invalid login or password!</div>"""
        values['Bugzilla_login']=Bugzilla_login
    return TemplateResponse('templates/login.html',values)

def do_newproject(request, create=None, **kw):
    session=Session.get_session(request)
    if session is None: 
        raise RedirectLocation('/login.html?hint=1')
    print create,kw.keys()
    values={'user':session.user.name,'pid':kw.get('pid',''),'name':kw.get('name',''),'descr':kw.get('descr','')}
    if create=='create':
        script=""
        if not re.match(r"^[A-Za-z0-9_]+$",kw['pid']):
            script+="""
            $('#pid').parent().parent().addClass('error')
            $('#pid').after('<span class="help-inline">only letters and numbers allowed</span>')
            """
        elif issuebase.projects.query_one(project_id=kw['pid']):
            script+="""
            $('#pid').parent().parent().addClass('error')
            $('#pid').after('<span class="help-inline">project with this id already exists</span>')
            """
        if  not kw['name']:
            script+="""
            $('#name').parent().parent().addClass('error')
            $('#name').after('<span class="help-inline">no name given</span>')
            """
        if not script:
            try: 
                prj=issuebase.projects.new()
                prj.creator=session.user.uid
                prj.creation_date=str(datetime.datetime.now()).split('.')[0]
                prj.project_id=kw['pid']
                prj.name=kw['name']
                prj.description=kw['descr']
                prj.icon=buffer(kw['icon'])
                prj.commit()
            except Exception, e:
                print type(e),e
            raise RedirectLocation('/index.html')
        values['script']=script
    return TemplateResponse('templates/newproject.html',values)

def do_project_summary(request,**kw):
    session=Session.get_session(request)
    if session:
        values={'user': '%s <a href="/logout.html">(logout)</a>'%encode_html(session.user.name)}
    else:
        values={'user': 'anonymous <a href="/login.html">(login)</a>'}
    pid=request.normpath.split('/')[2]
    prj=issuebase.projects.query_one(project_id=pid)
    values['project_id']=prj.project_id
    values['project_name']=prj.name
    values['project_description']=prj.description
    return TemplateResponse('templates/project_summary.html',values)

def do_project_issues(request,**kw):
    session=Session.get_session(request)
    if session:
        values={'user': '%s <a href="/logout.html">(logout)</a>'%encode_html(session.user.name)}
    else:
        values={'user': 'anonymous <a href="/login.html">(login)</a>'}
    pid=request.normpath.split('/')[2]
    prj=issuebase.projects.query_one(project_id=pid)
    values['project_id']=prj.project_id
    values['project_name']=prj.name
    values['project_description']=prj.description
    ilist=""
    for issue in issuebase.issues.query_iter(project_id=prj.pid):
        if issue.creator_id is not None:
            creator=issuebase.users[issue.creator_id].name
        else:
            creator="unknown"
        shorttitle=re.sub('[^A-Za-z0-9\s/]','',issue.title)
        shorttitle=re.sub('\s+','_',shorttitle)
        ilist+="""<tr><td class="number">#%i</td><td class="info">
        <div><b><a href="/issues/%i/%s/">%s</a></b>
        <p class="subinfo">by %s at %s</p>
        </td></tr>"""%(issue.iid,issue.iid,shorttitle,issue.title,creator,issue.creation_date)    
    values['issues']=ilist
    return TemplateResponse('templates/project_issues.html',values)

def do_project_newissue(request,submit=None, **kw):
    session=Session.get_session(request)
    if session is None: 
        raise RedirectLocation('/login.html?hint=1')
    pid=request.normpath.split('/')[2]
    prj=issuebase.projects.query_one(project_id=pid)
    values={'user': '%s <a href="/logout.html">(logout)</a>'%encode_html(session.user.name)}
    values['project_id']=prj.project_id
    values['project_name']=prj.name
    values['project_description']=prj.description
    values['title']=kw.get('title','')
    values['comment']=kw.get('comment','')
    if submit=='submit':
        script=""
        if  not kw.get('title'):
            script+="""
            $('#title').parent().parent().addClass('error')
            $('#title').after('<span class="help-inline">no title given</span>')
            """
        if not script:
            try: 
                iss=issuebase.issues.new()
                iss.creator_id=session.user.uid
                iss.creation_date=str(datetime.datetime.now()).split('.')[0]
                iss.modification_date=str(datetime.datetime.now()).split('.')[0]
                iss.project_id=prj.pid
                iss.title=kw['title']
                iss.bug_status="unconfirmed"
                iss.assignee_id=None
                iss.commit()
                if kw['comment']:
                    cmt=issuebase.comments.new()
                    cmt.issue_id=iss._rowid
                    cmt.is_private=0
                    cmt.creator_id=session.user.uid
                    cmt.creation_date=str(datetime.datetime.now()).split('.')[0]
                    cmt.text=kw['comment']
                    cmt.commit()
            except Exception, e:
                print type(e),e
            raise RedirectLocation('/projects/%s/issues.html'%prj.project_id)
        values['script']=script
    return TemplateResponse('templates/project_newissue.html',values)

def do_project_icon(request,**kw):
    pid=request.normpath.split('/')[2]
    print pid
    prj=issuebase.projects.query_one(project_id=pid)
    return MimeResponse(str(prj.icon),'image/jpeg')


def main():
    server = httprequest.DynamicHTTPServer(('', 5080))
    server.add_script('/_mylyn(/index\.cgi|/)?', do_mylyn_index, multiparam=False)
    server.add_script('/_mylyn/relogin\.cgi', do_mylyn_index, multiparam=False)
    server.add_script('/_mylyn/config\.cgi', do_mylyn_config, multiparam=False)
    server.add_script('/_mylyn/buglist\.cgi', do_mylyn_buglist, multiparam=False)
    server.add_script('/_mylyn/show_bug\.cgi', do_mylyn_show_bug, multiparam=False)
    server.add_script('/_mylyn/process_bug\.cgi', do_mylyn_process_bug, multiparam=False)
    server.add_script('/_mylyn/.*', lambda: None, multiparam=False)
    # raise error for anythinh else in _mylyn
    
    server.add_script('/(index\.html)?',do_list)
    server.add_script('/login\.html',do_login)
    server.add_script('/newproject\.html',do_newproject)

    server.add_script('/projects/[^/]+(/|/index\.html)?',do_project_summary)
    server.add_script('/projects/[^/]+/issues.html',do_project_issues)
    server.add_script('/projects/[^/]+/newissue.html',do_project_newissue)
    server.add_script('/projects/[^/]+/icon.jpg',do_project_icon)
    
    
    server.add_script('/.*',httprequest.FileHandler('htdocs'))
    
    try:
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
