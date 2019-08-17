import pyodbc
import os
import pysnooper
import traceback
import sys
cur_path,file=os.path.split(os.path.realpath(sys.argv[0])) 
class db():
    def __init__(self, *args):
        self._cnxn=None
        self._cursor=None
    @property
    def cnxn(self):
        return self._cnxn
    @cnxn.setter
    def cnxn(self,value):
        if isinstance(value, pyodbc.Connection):
            self._cnxn = value
        else:
            print('cnxn type must be Connection')
    @property
    def cursor(self):
        return self._cursor
    @cursor.setter
    def cursor(self,value):
        if isinstance(value, pyodbc.Cursor):
            self._cursor = value
        else:
            print('cursor type must be Cursor')
    @pysnooper.snoop(os.path.join(cur_path,'db.log'),depth=2)
    def connect_db(self):
        try:
            with pyodbc.connect('DRIVER={SQL Server\};SERVER=DESKTOP-AR24T88\SAK;DATABASE=SMT_Manage;UID=sa;PWD=111',timeout=5)  as cnxn:
            # with pyodbc.connect('DRIVER={SQL Server\};SERVER=172.30.125.221;DATABASE=SMT_Manage;UID=sa;PWD=0123456789',timeout=1) as cnxn:
                self.cnxn=cnxn
            # self.cnxn=pyodbc.connect('DRIVER={SQL Server\};SERVER=DESKTOP-AR24T88\SAK;DATABASE=SMT_Manage;UID=sa;PWD=111',timeout=5) 
                self.cursor=self.cnxn.cursor()
            return True
        except Exception as e:
            a=traceback.format_exc(limit=1)
            print(a)
            return False
    @pysnooper.snoop(os.path.join(cur_path,'db.log'),depth=2)
    def get_PCBA_ver(self,codeNo:str):
        try:
            code=codeNo[:10]
            row=codeNo[10:12]
            sql = f"select * from dbo.orderlist where 订单号='{code}' and 行号='{row}'"
            self.cursor.execute(sql)
            rs=self.cursor.fetchall()
            return rs[0].PCBA版本
        except Exception as e:
            a=traceback.format_exc(limit=1)
            print(a)
            return None
        