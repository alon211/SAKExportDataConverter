import pymssql
import pyodbc
import sys
sys.path.append('..')
from xml解析.dbxml_handle import *

parser=xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
# 重写
instance_dbHandle = dbHandle()
parser.setContentHandler(instance_dbHandle)

parser.parse(r'E:\myproject\智能工作台\xml解析\dbconnect.xml')

# conn=pymssql.connect(host=instance_dbHandle.HostName,#IP地址无法连接，服务器名称可以连接
#                      user=instance_dbHandle.UserName,
#                      password=instance_dbHandle.PassWord,
#                      database=instance_dbHandle.DBName,
#                      timeout=int(instance_dbHandle.TimeOut)
#                      )
# # 查看连接是否成功
# cursor = conn.cursor()
# sql = 'select * from dbo.h_orders'
# cursor.execute(sql)
# # 用一个rs变量获取数据
# rs = cursor.fetchall()
#
# print(rs)
cnxn=pyodbc.connect('DRIVER={SQL Server\};SERVER=DELL-PC;DATABASE=SAK_DataTable;UID=sa;PWD=111')

cursor=cnxn.cursor()
sql = 'select * from dbo.h_orders'
cursor.execute(sql)
rs= cursor.fetchall()
print(type(rs[0].AreaId))
