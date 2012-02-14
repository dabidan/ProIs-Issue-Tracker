'''
Created on 14.02.2012

@author: user
'''
import datetime
from xml.etree import ElementTree as ET
from issuedb import issuebase, Configuration, XMLNS_bz, XMLNS_rdf, Session
import httprequest
from httprequest import RDFResponse, XMLResponse, RedirectLocation, TemplateResponse, encode_html,\
    MimeResponse, redirect_location
import re

def do_mylyn_index(request, Bugzilla_login=None, **kw):
    if Bugzilla_login:
        try:
            session=Session(request)
        except (KeyError, AssertionError):
            return "<html><body>Wrong login/password</body></html>"
    else:
        session=Session.get_session(request)
        if session is None: return "<html><head><title>Log in to Bugzilla</title></head><body>Not logged in!</body></html>"
    return "<html><body>MyLyn-Interface</body></html>"

def do_mylyn_config(request, ctype=None):
    #session=Session.get_session(request)
    #if session is None: return "<html><body>Not logged in!</body></html>"
    if ctype=='rdf':
        config=Configuration()
        return RDFResponse(config.to_xml(request.headers.getheader('host')))

def do_mylyn_buglist(request, **kw):
    session=Session.get_session(request)
    if session is None: return "<html><head><title>Log in to Bugzilla</title></head><body>Not logged in!</body></html>"
    print kw
    host=request.headers.getheader('host')
    buglist=ET.Element(XMLNS_rdf+'result',
            attrib={XMLNS_rdf+'about':host+request.path})
    installation=ET.SubElement(buglist, XMLNS_bz+'installation',
            attrib={XMLNS_rdf+'about':host})
    ET.SubElement(installation,XMLNS_bz+'query_timestamp').text=str(datetime.datetime.now())
    bugs=ET.SubElement(buglist,XMLNS_bz+'bugs')
    seq=ET.SubElement(bugs,XMLNS_rdf+'Seq')
    
    if 'bug_id' in kw:
        cvars=[int(x) for x in (','.join(kw['bug_id'])).split(',') if x]
        cond=['bug_id in (%s)'%(','.join('?'*len(cvars)))]
        if 'chfieldfrom' in kw:
            cvars.append(re.sub(r'[+-]\d+$','',kw['chfieldfrom']))
            cond.append('datetime(modification_date)>=datetime(?)')
        if 'chfieldto' in kw:
            cvars.append(re.sub(r'[+-]\d+$','',kw['chfieldto']))
            cond.append('datetime(modification_date)<=datetime(?)')
        for bug in issuebase.select_sql(' and '.join(cond),cvars):
            ET.SubElement(seq,XMLNS_rdf+'li').append(bug.to_short_xml(host))
    else:
        make_search(kw)
        for bug in issuebase.issues:
            ET.SubElement(seq,XMLNS_rdf+'li').append(bug.to_short_xml(host))
    return RDFResponse(buglist)

named_search_terms=['status_whiteboard','short_desc','long_desc','keywords']
email_lists=['assigned_to','cc','qa_contact','commenter','reporter']
exact_matches=['changedin','bug_status', 'priority', 'version', 'product',
              'bug_severity', 'op_sys', 'resolution', 'rep_platform'] 

def make_search(kw):
    expr={'value':{},'type':{},'field':{}}
    negate={}
    idx=-1
    for key,value in kw.iteritems():
        key=key.lower()
        m=re.match('^([a-z]+)(\d+)-(\d+)-(\d+)$',key)
        if m:
            if m.group(1) in expr:
                abc=int(m.group(2)),int(m.group(3)),int(m.group(4))
                if len(value)>1 or abc in expr[m.group(1)]: print "Duplicate Option",key,value
                expr[m.group(1)][abc]=value[-1]
            else:
                print "Unknown Option",key,value
        elif key in exact_matches:
            for i,v in enumerate(value):
                abc=(-1,exact_matches.index(key),i)
                expr['field'][abc]=key
                expr['value'][abc]=v
                expr['type'][abc]='exact'
        elif key in named_search_terms:
            abc=(-2,named_search_terms.index(key),0)
            expr['field'][abc]=key
            expr['value'][abc]=value[-1]
        elif key[:-5] in named_search_terms and key[-5:]=='_type':
            abc=(-2,named_search_terms.index(key[:-5]),0)
            expr['type'][abc]=value[-1]
        elif key[:5]=='email':
            m=re.match('^email([a-z_]*)(\d+)$')
            if not m: print "Email option unknown",key,value
            elif m.group(1) in email_lists:
                abc=(-3,int(m.group(2)),email_lists.index(m.group(1)))
                expr['type'][abc]=kw['emailtype'+m.group(2)][-1]
                expr['field'][abc]=m.group(1)
                expr['value'][abc]=kw['email'+m.group(2)][-1]
            elif m.group(1) not in ('',type):
                print "Email option unknown",key,value
        elif key[:6]=='negate':
            m=re.match('^negate(\d+)$')
            negate[int(m.group(1))]=int(value[-1])
        elif key in ('ctype','order'):
            pass
        else:
            print "Option unknown",key,value
    print expr

def do_mylyn_show_bug(request, ctype=None, id=None, excludefield=(), **kw):
    session=Session.get_session(request)
    if session is None: return "<html><head><title>Log in to Bugzilla</title></head><body>Not logged in!</body></html>"
    print kw,excludefield
    if True or ctype[-1]=='xml':
        result=ET.Element('bugzilla',version="4.3")
        for ii in id:
            issue=issuebase.issues[int(ii)]
            result.append(issue.to_xml(request.headers.getheader('host'),excludefield))
        return XMLResponse(result)
    return "xxx"

def do_mylyn_process_bug(request, **kw):
    session=Session.get_session(request)
    if session is None: return "<html><head><title>Log in to Bugzilla</title></head><body>Not logged in!</body></html>"
    if kw['bug_id']!=kw['id']: raise "Internal Error"
    iid=int(kw['id'])
    iss=issuebase.issues[iid]
    iss.modification_date=str(datetime.datetime.now()).split('.')[0]
    ass=issuebase.users.query_one(login=kw.get('assigned_to'))
    if ass is not None:
        iss.assignee_id=ass.uid
    pro=issuebase.projects.query_one(name=kw.get('product'))
    if pro is not None:
        iss.project_id=pro.pid
    if kw.get('short_desc'):
        iss.title = kw['short_desc']
    for elem in ('bug_status','resolution','bug_file_loc','status_whiteboard','priority','bug_severity'):
        if elem in kw:
            setattr(iss,elem,kw[elem])
    iss.commit()
    
    if 'new_comment' in kw and kw['new_comment'].strip():
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
    return """<html><head><title>Bug %s processed</title></head></html>"""%iid
    #return "<html><body>%s ok</body></html>"%iid

def do_mylyn_post_bug(request, **kw):
    session=Session.get_session(request)
    if session is None: return "<html><head><title>Log in to Bugzilla</title></head><body>Not logged in!</body></html>"
    print kw
    iss=issuebase.issues.new()
    iss.creator_id=session.user.uid if session else None
    iss.creation_date=str(datetime.datetime.now()).split('.')[0]
    iss.modification_date=str(datetime.datetime.now()).split('.')[0]
    ass=issuebase.users.query_one(login=kw.get('assigned_to'))
    if ass is not None:
        iss.assignee_id=ass.uid
    pro=issuebase.projects.query_one(name=kw.get('product'))
    if pro is not None:
        iss.project_id=pro.pid
    if kw.get('short_desc'):
        iss.title = kw['short_desc']
    for elem in ('bug_status','resolution','bug_file_loc','status_whiteboard','priority','bug_severity'):
        if elem in kw:
            setattr(iss,elem,kw[elem])
    iss.commit()
    
    if 'new_comment' in kw and kw['new_comment'].strip():
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
    return """<html><head><title>Bug %s processed</title></head></html>"""%iss._rowid
    #return "<html><body>%s ok</body></html>"%iid

def do_mylyn_attachment(request, Bugzilla_login=None, action=None,**kw):
    if Bugzilla_login:
        try:
            session=Session(request)
        except (KeyError, AssertionError):
            return "<html><body>Wrong login/password</body></html>"
    else:
        session=Session.get_session(request)

    print session,action,kw
    if action=='insert':
        if session is None: return "<html><head><title>Log in to Bugzilla</title></head><body>Not logged in!</body></html>"
        cmt=issuebase.attachments.new()
        cmt.issue_id=int(kw['bugid'])
        cmt.is_patch=int(kw.get('ispatch',0))
        cmt.is_obsolete=int(kw.get('isobsolete',0))
        cmt.creator_id=session.user.uid if session else None
        cmt.creation_date=str(datetime.datetime.now()).split('.')[0]
        cmt.modifier_id=session.user.uid if session else None
        cmt.modification_date=str(datetime.datetime.now()).split('.')[0]
        cmt.description=kw.get('description')
        cmt.comment=kw.get('comment')
        cmt.mimetype=kw.get('contenttypeentry',kw.get('data')[1])
        cmt.filename=kw.get('data')[0]
        cmt.data=buffer(kw.get('data')[3])
        cmt.commit()
    elif action=='update':
        if session is None: return "<html><head><title>Log in to Bugzilla</title></head><body>Not logged in!</body></html>"
        cmt=issuebase.attachments[int(kw['id'])]
        cmt.modifier_id=session.user.uid if session else None
        cmt.modification_date=str(datetime.datetime.now()).split('.')[0]
        if 'ispatch' in kw: cmt.is_patch=int(kw['ispatch'])
        if 'isobsolete' in kw: cmt.is_obsolete=int(kw['isobsolete'])
        if 'description' in kw: cmt.is_description=kw['description']
        if 'comment' in kw: cmt.comment=kw['comment']
        if 'contenttypeentry' in kw: cmt.mimetype=kw['contenttypeentry']
        if 'filename' in kw: cmt.filenamekw['filename']
        cmt.commit()
    else:
        cmt=issuebase.attachments[int(kw['id'])]
        request.add_headers['Content-disposition']='inline; filename="%s"'%cmt.filename
        return MimeResponse(str(cmt.data),cmt.mimetype)
    return """<html><head><title>Bug %s processed</title></head></html>"""%int(kw['bugid'])

def init_mylyn(server, path):
    server.add_script(path, lambda **kw: redirect_location(path+'/index.cgi'))
    server.add_script(path+'/(index\.cgi)?', do_mylyn_index, multiparam=False)
    server.add_script(path+'/relogin\.cgi', do_mylyn_index, multiparam=False)
    server.add_script(path+'/config\.cgi', do_mylyn_config, multiparam=False)
    server.add_script(path+'/buglist\.cgi', do_mylyn_buglist, multiparam=True)
    server.add_script(path+'/show_bug\.cgi', do_mylyn_show_bug, multiparam=True)
    server.add_script(path+'/post_bug\.cgi', do_mylyn_post_bug, multiparam=False)
    server.add_script(path+'/process_bug\.cgi', do_mylyn_process_bug, multiparam=False)
    server.add_script(path+'/attachment\.cgi', do_mylyn_attachment, multiparam=False)
    server.add_script(path+'/.*', lambda: None, multiparam=False)
    # raise error for anythinh else in _mylyn
