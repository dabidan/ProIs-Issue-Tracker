'''
Created on 14.02.2012

@author: user
'''
import os
from xml.etree import ElementTree as ET
import hashlib
import base64
import time

import database
from database import dbfield, DBRecord, dbtable, Database

XMLNS_rdf="{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
XMLNS_bz="{http://www.bugzilla.org/rdf#}"

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

    def to_xml(self, host, excludefields=()):
        bug=ET.Element('bug')
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
        for att in issuebase.attachments.query_iter(issue_id=self.iid):
            bug.append(att.to_xml('attachmentdata' in excludefields))
        return bug
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
        else:
            ET.SubElement(result,'who',name='unknown').text='unknown'
        ET.SubElement(result,'bug_when').text=self.creation_date
        ET.SubElement(result,'thetext').text=self.text
        return result

class Attachment(DBRecord):
    aid=dbfield('aid','INTEGER','PRIMARY KEY AUTOINCREMENT')
    issue_id=dbfield('issue_id','INTEGER')
    is_patch=dbfield('is_patch','INTEGER')
    is_obsolete=dbfield('is_obsolete','INTEGER')
    creator_id=dbfield('creator_id','INTEGER')
    creation_date=dbfield('creation_date','TEXT')
    modifier_id=dbfield('modifier_id','INTEGER')
    modification_date=dbfield('modification_date','TEXT')
    description=dbfield('description','TEXT')
    comment=dbfield('comment','TEXT')
    mimetype=dbfield('mimetype','TEXT')
    filename=dbfield('filename','TEXT')
    data=dbfield('data','BLOB')

    def to_xml(self, exclude):
        result=ET.Element('attachment', isprivate='0',ispatch=str(self.is_patch),isobsolete=str(self.is_obsolete))
        ET.SubElement(result,'attachid').text=str(self.aid)
        if self.creator_id is not None:
            cc=issuebase.users[self.creator_id]
            ET.SubElement(result,'attacher').text=cc.login
        else:
            ET.SubElement(result,'attacher').text='unknown'
        ET.SubElement(result,'date').text=self.creation_date
        ET.SubElement(result,'delta_ts').text=self.modification_date
        ET.SubElement(result,'desc').text=self.description
        ET.SubElement(result,'filename').text=self.filename
        ET.SubElement(result,'type').text=self.mimetype
        ET.SubElement(result,'size').text=str(len(self.data))
        if not exclude:
            ET.SubElement(result,'data',encoding="base64").text=base64.b64encode(str(self.data))
        return result

class Notify(DBRecord):
    nid=dbfield('nid','INTEGER','PRIMARY KEY AUTOINCREMENT')
    issue_id=dbfield('issue_id','INTEGER')
    user_id=dbfield('user_id','INTEGER')

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
        x=hashlib.sha256(passwd.encode('utf-8')+salt)
        return base64.b64encode(salt+x.digest())
    
    def checkpasswd(self, passwd):
        pwd=base64.b64decode(self.passwd)
        return self.passwd==self.mkpasswd(passwd, salt=pwd[:8])

class IssueBase(Database):
    users=dbtable('Users',User)
    projects=dbtable('Projects',Project)
    issues=dbtable('Issues',Issue)
    comments=dbtable('Comments',Comment)
    attachments=dbtable('Attachments',Attachment)
    notify=dbtable('Notify',Notify)
    

issuebase=IssueBase('test.db')
#issuebase.drop_all()
#issuebase.cursor().execute("drop table Attachments")
issuebase.create_tables()
