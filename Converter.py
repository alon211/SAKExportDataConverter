import win32com.client as win32
import sys
import numpy as np
import pandas as pd
sys.path.append('../')
import datetime
from usermodules import file_operate

# filelist=file_operate.get_files_by_extension(r'E:\myproject\智能工作台','xls')
# print(filelist)
# excel=win32.gencache.EnsureDispatch('Excel.Application')
# wb=excel.Workbooks.Open(filelist[0])
# excel.Visible=True
# ws=wb.Worksheets('记录表')
# data=ws.Range('A1:G44').Value
# data=np.array(data)
# data.astype('str')
# print(data)
# np.savetxt('1.txt',data,fmt='%s',delimiter=',')
# excel.Application.Quit()

###########读取固定格式配置#########################
# data=np.loadtxt('2.txt',dtype='str',delimiter=',')
# print(data)

###################################################
def read_SAK_file(path):
    validate=False
    value=None
    try:
        data=pd.read_csv(path,header=0,na_values=np.NaN,encoding='utf-8',dtype='str',keep_default_na=False)
    except Exception as e:
        return None
    check_h_orders_columns = np.array(['CompanyId', 'FactoryId', 'AreaId', 'OrderType', 'OrderName',
                              'OrderCode', 'ProductName', 'ProductCode', 'ProductModel',
                              'ProductStandardTime', 'JobTableName', 'PlanCount', 'CompletedCount',
                              'NgStepCount', 'WorkTime', 'Result', 'StartTime', 'EndTime', 'UserCode',
                              'UserName', 'Information', 'TorqueData', 'RotationTimeData',
                              'RotationAngleData', 'TraceData', 'ScrewSpecData', 'ProductVersion',
                              'BomSetName', 'BomSetCode', 'BomSetVersion', 'ProductInformation',
                              'CustomInformation', 'JobId', 'CommentData', 'PartsData'])
    check_h_job_steps_columns=np.array(['CompanyId', 'FactoryId', 'AreaId', 'ProductName', 'ProductCode',
       'ProductModel', 'JobId', 'JobTableName', 'StepNo', 'StepType', 'Result',
       'NgStepCount', 'StartTime', 'EndTime', 'WorkTime', 'StandardTime',
       'UserCode', 'UserName', 'Information', 'ProductVersion', 'BomSetName',
       'BomSetCode', 'BomSetVersion', 'CustomInformation', 'ScrewSpecData',
       'CommentData', 'TorqueData', 'RotationTimeData', 'RotationAngleData',
       'TraceData', 'PartsData'])
    filename=''
    if path.find('h_orders.csv')>-1:
        filename='h_orders.csv'
    if path.find('h_job_steps.csv')>-1:
        filename = 'h_job_steps.csv'
    if filename=='h_job_steps.csv':
        validate=(data.columns==check_h_job_steps_columns).all()
    elif filename=='h_orders.csv':
        validate = (data.columns == check_h_orders_columns).all()
        if validate:
            data = data[data['Result'] == '2']
    if validate:
        data['StartTime']=pd.to_datetime(data['StartTime'], format='%Y-%m-%d')
        data['EndTime']=pd.to_datetime(data['EndTime'], format='%Y-%m-%d')
        value=data
        return value
    else:
        return None
def get_Completed_Product_Data(ProductName:str,ProductVersion:str,TableName:str,StartDate:datetime.datetime,EndDate:datetime.datetime,data:pd.DataFrame):


    # 通过h_orders筛选出当日期范围内的所有完成订单，返回范围内的时间序列
    df=data[(data['ProductName']==ProductName)&
            (data['AreaId']==TableName)&
            (data['ProductVersion']==ProductVersion)&
            (data['StartTime']>=StartDate)&
            (data['StartTime']<=EndDate)
    ]
    if df.empty:
        return None
    else:
        return df
def get_h_steps_complete_tracedata(h_orders_complete_data:pd.DataFrame,h_steps_data:pd.DataFrame):
    # 从get_Completed_Product_Data获取到的所有完成产品数据然后查找h_job_steps里的对应的列数据
    '''

    :param h_orders_complete_data:
    :param h_steps_data:
    :return:
    '''
    rst=h_steps_data.drop(index=h_steps_data.index)
    for index,row in h_orders_complete_data.iterrows():
        tmp=h_steps_data[(h_steps_data['StartTime']>=row['StartTime'])&
                     (h_steps_data['EndTime']<=row['EndTime'])
        ]
        rst=pd.concat((rst,tmp))
    return rst
# AreaId ProductName ProductVersion StepNo StartTime EndTime
# 创建一个对话框：内容包含 作业台名称 作业程序版本 选择开始日期 结束日期 输出文档路径 输入文档路径(h_job_steps.csv h_order.csv)
# 先从h_order中确认完成产品的版本号，开始时间，结束时间


# data=pd.read_csv(r'E:\myproject\智能工作台\h_orders.csv',header=0,na_values='NULL',encoding='utf-8',dtype='str')
# check_columns=np.array(['CompanyId', 'FactoryId', 'AreaId', 'OrderType', 'OrderName',
#        'OrderCode', 'ProductName', 'ProductCode', 'ProductModel',
#        'ProductStandardTime', 'JobTableName', 'PlanCount', 'CompletedCount',
#        'NgStepCount', 'WorkTime', 'Result', 'StartTime', 'EndTime', 'UserCode',
#        'UserName', 'Information', 'TorqueData', 'RotationTimeData',
#        'RotationAngleData', 'TraceData', 'ScrewSpecData', 'ProductVersion',
#        'BomSetName', 'BomSetCode', 'BomSetVersion', 'ProductInformation',
#        'CustomInformation', 'JobId', 'CommentData', 'PartsData'])
# print(check_columns)
# print((data.columns==check_columns).all())
# #先筛选出完成的产品 result=2完成 =9未完成
# data=data[data['Result']=='2']
# # 先将作业台名称 作业程序版本 筛选出来
# df=data[(data['ProductName']=='四方监控屏111') & (data['ProductVersion']=='4') ]
# if df.empty:
#     print('完成产品中没有该产品版本号或者产品名称')
#     sys.exit(0)
# # 筛选出在日期范围内的数据索引号
# df_dt=pd.to_datetime(df['StartTime'],format='%Y-%m-%d')
# Select_StartTime=pd.to_datetime('2019-6-10')
# Select_EndTime=pd.to_datetime('2019-7-10')
# index=(df_dt[(Select_EndTime>df_dt) & (Select_StartTime<df_dt)].index)
# df=df.loc[index]
#
# data=pd.read_csv(r'E:\myproject\智能工作台\1.csv',header=0,na_values='NULL',encoding='utf-8',dtype='str')
# # 先将作业台名称 作业程序版本 筛选出来
# df=data[(data['ProductName']=='四方监控屏111') & (data['ProductVersion']=='4') ]
# # 筛选出在日期范围内的数据索引号
# df_dt=pd.to_datetime(df['StartTime'],format='%Y-%m-%d')
# Select_StartTime=pd.to_datetime('2019-6-10')
# Select_EndTime=pd.to_datetime('2019-7-10')
# index=(df_dt[(Select_EndTime>df_dt) & (Select_StartTime<df_dt)].index)
# df=df.loc[index]
#
# #筛选出产品序列号
# print(df[df['StepNo']=='1'].head(1)['TraceData'].iloc[0])
#
# print(df[df['BomSetCode']=='701050000477100'])