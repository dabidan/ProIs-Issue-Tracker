'''
Created on 07.02.2012

@author: user
'''
import time
import httprequest
from httprequest import RDFResponse, XMLResponse, RedirectLocation, TemplateResponse, encode_html,\
    MimeResponse
from xml.etree import ElementTree as ET
import base64
import os
import re
import datetime
from issuedb import issuebase, Configuration, XMLNS_bz, XMLNS_rdf, Session, User
import database
from mylyn import init_mylyn







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
      </li>"""%(prj.project_id,prj.project_id,encode_html(prj.name),encode_html(prj.description.split('\n')[0]))
    values['list']=list
    return TemplateResponse('templates/list.html',values)

def do_login(request, hint=None, login=None, Bugzilla_login=None, Bugzilla_password=None, realname=None, email=None, **kw):
    values={}
    if hint=='1':
        values['message']="""<div class="alert">To create a new project you need to login.</div><input type="hidden" name="goto" value="/newproject.html">"""
    elif hint=='2':
        values['message']="""<div class="alert">To submit a new issue you need to login.</div><input type="hidden" name="goto" value="/projects/%s/newissue.html">"""%kw.get('project','')
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
            raise RedirectLocation(kw.get('goto','/index.html'))
        except (KeyError, AssertionError), e:
            print e
            pass
        values['message']="""<div class="alert alert-error">Invalid login or password!</div><input type="hidden" name="goto" value="%s">"""%kw.get('goto','/index.html')
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
                print re.sub('[^0-9]*','',kw['icon_nr']),kw['icon_nr']
                prj.icon=re.sub('[^0-9]*','',kw['icon_nr'])
                prj.commit()
            except Exception, e:
                print type(e),e
            raise RedirectLocation('/index.html')
        values['script']=script
    values['imglist']=','.join([str(att.aid) for att in issuebase.attachments.query_iter(issue_id=-1)])
    return TemplateResponse('templates/newproject.html',values)

def do_upload(request, **kw):
    session=Session.get_session(request)
    if session is None: 
        raise RedirectLocation('/login.html')
    print kw['icon'][:3],len(kw['icon'][3])
    if kw['icon'][3]:
        att=issuebase.attachments.new()
        att.issue_id=-1
        att.creator_id=session.user.uid if session else None
        att.creation_date=str(datetime.datetime.now()).split('.')[0]
        att.modifier_id=session.user.uid if session else None
        att.modification_date=str(datetime.datetime.now()).split('.')[0]
        att.mimetype=kw.get('contenttypeentry',kw.get('icon')[1])
        att.filename=kw.get('icon')[0]
        att.data=buffer(kw.get('icon')[3])
        att.commit()
        print att._rowid
        return MimeResponse(str(att._rowid),'text/plain')

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
    dd=prj.description.split('\n')
    values['project_description']='<p><b>%s</b></p><p>%s</p>'%(encode_html(dd[0]),'</p><p>'.join(map(encode_html,dd[1:])))
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
        <div><b><a href="/issues/%i/%s">%s</a></b>%s
        <p class="subinfo">by %s at %s</p>
        </td></tr>"""%(issue.iid,issue.iid,shorttitle,issue.title,
            "<span class='pull-right label label-warning'>new</span>" if issue.bug_status=="unconfirmed" else "",
            creator,issue.creation_date)    
    values['issues']=ilist
    return TemplateResponse('templates/project_issues.html',values)

def do_project_newissue(request,submit=None, **kw):
    pid=request.normpath.split('/')[2]
    session=Session.get_session(request)
    if session is None: 
        raise RedirectLocation('/login.html?hint=2&project=%s'%pid)
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
                iss.assignee_id=prj.creator_id
                iss.bug_severity=kw.get('severity','normal')
                iss.priority=kw.get('priority','medium')
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
    att=issuebase.attachments[prj.icon] if prj.icon else None
    if att:
        return MimeResponse(str(att.data),att.mimetype)
    else:
        raise RedirectLocation('/default2.png')

def do_project_browse(request,**kw):
    pid=request.normpath.split('/')[2]
    session=Session.get_session(request)
    if session is None: 
        raise RedirectLocation('/login.html?hint=2&project=%s'%pid)
    prj=issuebase.projects.query_one(project_id=pid)
    values={'user': '%s <a href="/logout.html">(logout)</a>'%encode_html(session.user.name)}
    values['project_id']=prj.project_id
    values['project_name']=prj.name
    values['project_description']=prj.description
    values['title']=kw.get('title','')
    values['comment']=kw.get('comment','')
    return TemplateResponse('templates/project_browse.html',values)

def do_issue(request,**kw):
    iid=request.normpath.split('/')[2]
    session=Session.get_session(request)
    if session:
        values={'user': '%s <a href="/logout.html">(logout)</a>'%encode_html(session.user.name)}
    else:
        values={'user': 'anonymous <a href="/login.html">(login)</a>'}
    iss=issuebase.issues[int(iid)]
    prj=issuebase.projects[iss.project_id]
    values['project_id']=prj.project_id
    values['project_name']=prj.name
    values['project_description']=prj.description
    values['iid']=iid
    values['title']=iss.title
    values['s_'+(iss.bug_severity or 'normal')]='selected="selected"'
    values['s_'+(iss.priority or 'medium')]='selected="selected"'
    return TemplateResponse('templates/project_issue.html',values)

def do_logout(request,**kw):
    request.set_cookies['Bugzilla_login']=''
    request.set_cookies['Bugzilla_logincookie']=''
    raise RedirectLocation('/index.html')


def main():
    server = httprequest.DynamicHTTPServer(('', 5080))
    init_mylyn(server, '/mylyn')
    
    server.add_script('/(index\.html)?',do_list)
    server.add_script('/login\.html',do_login)
    server.add_script('/logout\.html',do_logout)
    server.add_script('/newproject\.html',do_newproject)
    server.add_script('/upload\.cgi',do_upload)

    server.add_script('/projects/[^/]+(/|/index\.html)?',do_project_summary)
    server.add_script('/projects/[^/]+/issues.html',do_project_issues)
    server.add_script('/projects/[^/]+/newissue.html',do_project_newissue)
    server.add_script('/projects/[^/]+/browse.html',do_project_browse)
    server.add_script('/projects/[^/]+/icon.jpg',do_project_icon)
    
    server.add_script('/issues/.*',do_issue)
    
    server.add_script('/.*',httprequest.FileHandler('htdocs'))
    
    try:
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
