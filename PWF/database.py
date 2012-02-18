'''
Created on 10.02.2012

@author: user
'''
import sqlite3


class dbfield(object):
    __FIELD_INDEX=0
    def __init__(self, field_name, data_type, *constraints):
        self.field_name=field_name
        self.data_type=data_type
        self.constraints=constraints
        dbfield.__FIELD_INDEX+=1
        self.field_index=dbfield.__FIELD_INDEX
        
    def __get__(self, obj, cls):
        try:
            return obj._dbrecord[self.field_name]
        except KeyError:
            obj._dbrecord[self.field_name]=result=obj.get_field(self.field_name)
            return result
        
    def __set__(self, obj, val):
        obj._dbrecord[self.field_name]=val
        obj._dbchanged.add(self.field_name)

    def get_column_definition(self):
        return ' '.join((self.field_name,self.data_type)+self.constraints)

class DBRecord(object):
    def __init__(self, db, table_name, rowid=None, record=None):
        self._rowid=rowid
        self._dbrecord={} if record is None else record
        self._dbchanged=set()
        self._db=db
        self._table_name=table_name
        
    def commit(self):
        if self._dbchanged:
            names=list(self._dbchanged)
            values=[self._dbrecord[n] for n in names]
            c = self._db.cursor()
            if self._rowid is None:
                c.execute("insert into %s (%s) values (%s)"%(self._table_name,','.join(names),','.join(['?']*len(values))),values)
                self._rowid=c.lastrowid
            else:
                c.execute("update %s set %s where _rowid_=%i"%(self._table_name,','.join(['%s=?'%name for name in names]),self._rowid),values)
            self._dbchanged=set()
            self._db.commit()
            c.close()
            
    def delete(self):
        if self._rowid is None: return
        c= self._db.cursor()
        c.execute("delete from ? where _rowid_=?",(self._table_name,self._rowid))
        self._rowid=None
        self._db.commit()
            
    def get_field(self, fieldname):
        c = self._db.cursor()
        c.execute("select %s from %s where _rowid_=%i"%(fieldname,self._table_name,self._rowid))
        row=c.fetchone()
        return row[0]

class RowGetter(object):
    def __init__(self, db, table_name, record_type):
        self._db=db
        self.table_name=table_name
        self.record_type=record_type
    
    def new(self, **kw):
        record = self.record_type(self._db,self.table_name)
        for key,val in kw.iteritems():
            fld = self.record_type.__dict__.get(key)
            if hasattr(fld,'get_column_definition'):
                setattr(record,key,val)
            else:
                raise ValueError('field %s not defined.'%key)
        return record

    def __get_fieldnames(self):
        return [fld.field_name for fld in self.record_type.__dict__.itervalues() if hasattr(fld,'get_column_definition') and fld.data_type!='BLOB']
    
    def __select_sql(self, conditions, cond_vars):
        c=self._db.cursor()
        fields=self.__get_fieldnames()
        c.execute("select _rowid_, %s from %s where %s"%(','.join(fields),self.table_name,conditions),cond_vars)
        row=c.fetchone()
        c.close()
        if row:
            record=self.record_type(self._db,self.table_name,row[0],dict(zip(fields,row[1:])))
        else:
            raise IndexError('no entry found')
        return record
        
    def __getitem__(self, index):
        return self.__select_sql('_rowid_=?',[index])

    def query_one(self, **kw):
        fields=[]
        cvars=[]
        for key,value in kw.iteritems():
            fld=self.record_type.__dict__[key]
            if hasattr(fld,'get_column_definition'):
                fields.append(fld.field_name)
                cvars.append(value)
            else:
                raise KeyError('Field %s not defined.'%key)
        try:
            return self.__select_sql(' and '.join(['%s=?'%fld for fld in fields]), cvars)
        except: return None

    def query_iter(self, **kw):
        fields=[]
        cvars=[]
        for key,value in kw.iteritems():
            fld=self.record_type.__dict__[key]
            if hasattr(fld,'get_column_definition'):
                fields.append(fld.field_name)
                cvars.append(value)
            else:
                raise KeyError('Field %s not defined.'%key)
        conditions=' and '.join(['%s=?'%fld for fld in fields])
        c=self._db.cursor()
        fields=self.__get_fieldnames()
        c.execute("select _rowid_, %s from %s where %s"%(','.join(fields),self.table_name,conditions),cvars)
        while True:
            row=c.fetchone()
            if row is None: break
            record=self.record_type(self._db,self.table_name,row[0],dict(zip(fields,row[1:])))
            yield record
        c.close()

    def select_sql(self, conditions, cond_vars):
        c=self._db.cursor()
        fields=self.__get_fieldnames()
        c.execute("select _rowid_, %s from %s where %s"%(','.join(fields),self.table_name,conditions),cond_vars)
        while True:
            row=c.fetchone()
            if row is None: break
            record=self.record_type(self._db,self.table_name,row[0],dict(zip(fields,row[1:])))
            yield record
        c.close()

    def __iter__(self):
        c=self._db.cursor()
        fields=self.__get_fieldnames()
        c.execute("select _rowid_, %s from %s"%(','.join(fields),self.table_name))
        while True:
            row=c.fetchone()
            if row is None: break
            record=self.record_type(self._db,self.table_name,row[0],dict(zip(fields,row[1:])))
            yield record
        c.close()
        

class dbtable(object):
    def __init__(self, table_name, record_type):
        self.table_name=table_name
        self.record_type=record_type
        
    def __get__(self, obj, cls):
        return RowGetter(obj, self.table_name, self.record_type)
        
    def get_table_definition(self):
        fields=[fld for fld in self.record_type.__dict__.itervalues() if hasattr(fld,'get_column_definition')]
        fields.sort(cmp=lambda a,b: cmp(a.field_index,b.field_index))
        return "create table %s (%s)"%(self.table_name, ','.join([fld.get_column_definition() for fld in fields]))
    
class Database(object):
    def __init__(self, dbname):
        self.dbname=dbname
        self.db=sqlite3.connect(dbname)
        
    def commit(self):
        return self.db.commit()
        
    def cursor(self):
        return self.db.cursor()

    def close(self):
        self.db.close()

    def create_tables(self):
        c=self.cursor()
        for tab in self.__class__.__dict__.itervalues():
            if not hasattr(tab,'get_table_definition'):
                continue
            try:
                c.execute(tab.get_table_definition())
            except: print "Creation of %s failed."%tab.table_name
        self.commit()

    def drop_all(self):
        c=self.cursor()
        for tab in self.__class__.__dict__.itervalues():
            if not hasattr(tab,'get_table_definition'):
                continue
            c.execute("drop table %s"%tab.table_name)
        self.commit()
        

if __name__=='__main__':
    class User(DBRecord):
        uid=dbfield('user_id','INTEGER','PRIMARY KEY AUTOINCREMENT')
        login=dbfield('user_login','TEXT','UNIQUE')
        passwd=dbfield('user_passwd','TEXT')
        name=dbfield('user_name','TEXT')
        email=dbfield('user_email','TEXT')
        flags=dbfield('user_flags','TEXT')
    
    
    class IssueBase(Database):
        users=dbtable('Users',User)
        
    
    ib=IssueBase('test.db')
    #ib.drop_all()
    #ib.create_tables()
    #uu=ib.users.new()
    #uu.name='ich'
    #uu.passwd='geheim'
    #uu.commit()
    uu=ib.users.query_one(login='abc2')
    print uu.uid,uu.login,uu.passwd, uu.email
    uu=ib.users.new(login='abc',passwd='xxz',email='here@nowhere.com')
    print uu.login
    uu.commit()
    print uu._rowid