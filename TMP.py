import sys
import pysnooper

sys.path.append("..")
from appJar import gui
import time
import threading
import traceback
import os
import json
from tkinter import *
import calendar
import datetime
from Converter import *


class userGui(object):
    def __init__(self):
        # self._app=self._create_gui()
        self._check_tablename = False
        self._check_productversion = False
        self._check_productname = False
        self._check_outputfolder = False
        self._data_h_job_steps=None
        self._data_h_order=None

        self._json_data = {
            "h_job_step路径": '',
            "h_order路径": '',
            "生成路径": '',
        }
        self._auto_data = {"run": 1}
        # 检查是否有config文件夹，没有则创建
        current_path = os.getcwd()
        check_path = os.path.join(current_path, 'config')
        if not os.path.exists(check_path):
            os.mkdir(check_path)
        self._config_path = os.path.join(check_path, 'config.json')
        self._config_auto = os.path.join(check_path, 'startparm.json')
        if os.path.exists(self._config_path):
            self.read_config()
        if not os.path.exists(self._config_auto):
            self.write_auto()

        self.config()

    def read_config(self):
        data = self.read_json(self._config_path)
        self._json_data = data
        if self._json_data["h_job_step路径"].find('h_job_steps.csv')>-1:
            self.app.setEntry('h_job_steps_user_fileentry',self._json_data["h_job_step路径"])
        if self._json_data['h_order路径'].find('h_job_steps.csv')>-1:
            self.app.setEntry('h_orders_user_fileentry', self._json_data["h_order路径"])
        if self._json_data["生成路径"]!='':
            self.app.setEntry('Export_Folder_user_fileentry',self._json_data["生成路径"])

    def read_json(self, path):
        with open(path, "r", encoding='utf-8') as f:
            # data=f.read().decode(encoding='gbk').encoding('utf-8')
            data = json.load(f)
            print(data)
            return data


    def write_config(self):
        self.write_json(self._config_path, self._json_data)
        print("加载入文件完成...")
        self.stop()

    def write_json(self, path, data):
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, sort_keys=True)

    def write_auto(self):
        self.write_json(self._config_auto, self._auto_data)

    def stop(self):
        self._app.stop()

    @property
    def app(self):
        return self._app

    def start(self):
        self._app.go(startWindow='login')

    # ---------------------------画面--------------------------
    def config(self):
        row=0
        col=0
        # ----------------------登陆画面-----------------------
        self._app = gui(startWindow="login", useTtk=True, showIcon=False)
        self._app.setPollTime(1000)
        self._app.setExpand('both')
        self._app.setSticky("news")
        self._app.startSubWindow('login')
        with self._app.labelFrame('欢迎使用SAK转换程序', sticky='ew'):
            # self._app.addLabel("title", "欢迎使用SAK转换程序!", row, col,2)  # Row 0, Column 0, Span 2

            self._app.startLabelFrame('h_job_steps', row + 1, col, 2,label='h_job_steps文件路径')
            self.add_user_widget_fileentry('h_job_steps',0,0)
            self._app.stopLabelFrame()

            self._app.startLabelFrame('h_order', row + 2, col,2, label='h_order文件路径')
            self.add_user_widget_fileentry('h_orders',0,0)
            self._app.stopLabelFrame()

            self._app.startLabelFrame('ExportFolder', row + 3, col,2, label='输出文件保存路径')
            ent = self._app.addDirectoryEntry('ExportFolder', 0, 0)
            # ent.bind("<FocusOut>", self.set_attachment_path)
            self._app.stopLabelFrame()

            self._app.startFrame('OptionBoxFrame',row + 4, col,2)
            self._app.addLabel("TableName", "TableName:", 0,0)
            # self._app.setLabelAlign("TableName", "nw")
            self._app.addOptionBox("TableName_OptionBox", [''], 0,1,1)
            self._app.addLabel("ProductName", "ProductName:", 1, 0,1)
            self._app.addOptionBox("ProductName_OptionBox", [''], 1, 1,1)
            self._app.addLabel("ProductVersion", "ProductVersion:", 2, 0,1)
            self._app.addOptionBox("ProductVersion_OptionBox", [''], 2, 1,1)
            self._app.stopFrame()
            # 起始日期
            self._app.startLabelFrame('StartDate',row + 5,col,label='起始日期')
            self.add_user_widget_datepick('StartDate',0,0,2)
            self._app.stopLabelFrame()
            # 借宿日期
            self._app.startLabelFrame('EndDate', row + 6, col, label='结束日期')
            self.add_user_widget_datepick('EndDate', 0, 0, 2)
            self._app.stopLabelFrame()

            self._app.addButtons(["转换", "取消"], self.press, row+7, col,2 ) # Row 3, Column 0, Span 2
            self._app.setStopFunction(self.stop)

        self._app.stopSubWindow()

    def add_user_widget_fileentry(self, title, row=None, column=0, colspan=0, rowspan=0):
        self._app.startFrame(title,row,column,colspan,rowspan)
        ent=self._app.addEntry(title+'_user_fileentry',0,0)
        ent.config(state='disabled')
        self._app.addNamedButton('File',title+'_user_fileentry',self.open_file_dialog,0,1)
        self._app.stopFrame()
    def open_file_dialog(self,title):

        # 检查文件是否正确
        check_path=''
        if title.find('h_job_steps')>-1 or title.find('h_orders')>-1:
            check_path=title.split('_user_fileentry')[0]+'.csv'

        if check_path !='':
            dir=self._app.openBox(title)

            if dir.find(check_path)>-1:

                if check_path=='h_job_steps.csv':
                    self._data_h_job_steps=read_SAK_file(dir)
                    if self._data_h_job_steps is not None:
                        self._app.setEntry(title, dir)
                    else:
                        self._app.warningBox('警告','文件内容不匹配')
                elif check_path=='h_orders.csv':
                    self._data_h_order=read_SAK_file(dir)
                    if self._data_h_order is not None:
                        self._app.setEntry(title, dir)
                        self._app.changeOptionBox('TableName_OptionBox',self._data_h_order['AreaId'].drop_duplicates())
                        self._app.changeOptionBox('ProductName_OptionBox',self._data_h_order['ProductName'].drop_duplicates())
                        self._app.changeOptionBox('ProductVersion_OptionBox',self._data_h_order['ProductVersion'].drop_duplicates())
                    else:
                        self._app.warningBox('警告', '文件内容不匹配')
            else:
                self._app.warningBox('警告',f'请选择文件{check_path}')

    def add_user_widget_datepick(self, name, row=None, column=0, colspan=0, rowspan=0):
        ''' adds a date picker at the specified position '''
        self._app.widgetManager.verify(self._app.Widgets.DatePicker, name)
        # initial DatePicker has these dates
        days = range(1, 32)
        self.MONTH_NAMES = list(range(1,13))
        years = range(2000, 3020)
        # create a frame, and add the widgets
        frame = self._app.startFrame(name, row, column, colspan, rowspan)
        self._app.setExpand("none")
        self._app.addLabel(name + "_DP_DayLabel", "日:", 0, 4)
        self._app.setLabelAlign(name + "_DP_DayLabel", "w")
        self._app.addOptionBox(name + "_DP_DayOptionBox", days, 0, 5)
        self._app.addLabel(name + "_DP_MonthLabel", "月:", 0, 2)
        self._app.setLabelAlign(name + "_DP_MonthLabel", "w")
        self._app.addOptionBox(name + "_DP_MonthOptionBox", self.MONTH_NAMES, 0, 3)
        self._app.addLabel(name + "_DP_YearLabel", "年:", 0, 0)
        self._app.setLabelAlign(name + "_DP_YearLabel", "w")
        self._app.addOptionBox(name + "_DP_YearOptionBox", years, 0, 1)
        self._app.setOptionBoxChangeFunction(
            name + "_DP_MonthOptionBox",
            self._updateDatePicker)
        self._app.setOptionBoxChangeFunction(
            name + "_DP_YearOptionBox",
            self._updateDatePicker)
        self._app.stopFrame()
        frame.isContainer = False
        self._app.widgetManager.add(self._app.Widgets.DatePicker, name, frame)
    def get_user_widget_DatePicker(self, title):
        self._app.widgetManager.get(self._app.Widgets.DatePicker, title)
        day = int(self._app.getOptionBox(title + "_DP_DayOptionBox"))
        month = int(self._app.getOptionBox(title + "_DP_MonthOptionBox"))
        year = int(self._app.getOptionBox(title + "_DP_YearOptionBox"))
        date = datetime.datetime(year, month, day)
        return date
    def _updateDatePicker(self,title):
        if title.find("_DP_MonthOptionBox") > -1:
            title = title.split("_DP_MonthOptionBox")[0]
        elif title.find("_DP_YearOptionBox") > -1:
            title = title.split("_DP_YearOptionBox")[0]
        else:
            self._app.warn("Can't update days in DatePicker:%s", title)
            return

        day = self._app.getOptionBox(title + "_DP_DayOptionBox")
        month = int(self._app.getOptionBox(title + "_DP_MonthOptionBox"))
        year = int(self._app.getOptionBox(title + "_DP_YearOptionBox"))
        days = range(1, calendar.monthrange(year, month)[1] + 1)
        self._app.changeOptionBox(title + "_DP_DayOptionBox", days)

        # keep previous day if possible
        # with PauseLogger():
        #     self.setOptionBox(title + "_DP_DayOptionBox", day, callFunction=False)

        box = self._app.widgetManager.get(self._app.Widgets.OptionBox, title + "_DP_DayOptionBox")
        if hasattr(box, 'function'):
            box.function()
    def set_user_widget_DatePicker(self, title, date="today"):
        self._app.widgetManager.get(self._app.Widgets.DatePicker, title)
        if date == "today":
            date = datetime.date.today()
        self._app.setOptionBox(title + "_DP_YearOptionBox", str(date.year))
        self._app.setOptionBox(title + "_DP_MonthOptionBox", date.month - 1)
        self._app.setOptionBox(title + "_DP_DayOptionBox", date.day - 1)
    def file_box_stop(self):
        self._app.hideSubWindow('filebox')


    def show(self, msg):
        self._app.setTextArea("log", msg + '\n')

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if isinstance(value, bool):
            self._action = value
        else:
            print('action type must be boolean')

    def press(self, btn):
        if btn == "yes":
            v = self._app.getEntry('driver存放路径')
            if not os.path.exists(v):
                self._app.warningBox('警告', "文件路径不存在")

            else:
                tmp = os.path.split(v)
                print(tmp)
                if tmp[1] != 'IEDriverServer.exe':
                    self._app.warningBox('警告', "请选择IEDriverServer")
                else:
                    self._json_data["iedriver路径"] = self._app.getEntry('driver存放路径')
                    self._app.hideSubWindow('filebox')

        if btn == "清空":
            w = self._app.getEntry("通讯费存储路径")
            self._app.setTextArea("log", w + '\n')
        if btn == "取消":
            self.write_config()
        if btn == "转换":
            entries = self._app.getAllEntries()
            StartTime=self.get_user_widget_DatePicker('StartDate')
            EndTime=self.get_user_widget_DatePicker('EndDate')
            if StartTime>EndTime:
                self._app.warningBox('警告','结束日期不能小于起始日期')
                self.set_user_widget_DatePicker('StartDate')
                self.set_user_widget_DatePicker('EndDate')
                return
            if all(entries.values()):
                # print(self._data_h_job_steps['StartTime'])
                self._ProductName_Value=self._app.getOptionBox('ProductName_OptionBox')
                self._ProductVersion_Value=self._app.getOptionBox('ProductVersion_OptionBox')
                self._TableName_Value=self._app.getOptionBox('TableName_OptionBox')
                df=get_Completed_Product_Data(self._ProductName_Value,self._ProductVersion_Value,
                                   self._TableName_Value,StartTime,EndTime,self._data_h_order)
                if df is None:
                    self._app.warningBox('警告','未查找到匹配数据！')
                else:
                    tmp=self._data_h_job_steps[(self._data_h_job_steps['ProductName']==self._ProductName_Value)&
                                                (self._data_h_job_steps['AreaId']==self._TableName_Value)&
                                                (self._data_h_job_steps['ProductVersion']==self._ProductVersion_Value)]
                    rst=get_h_steps_complete_tracedata(df,tmp)
                    if rst is not None:
                        print(rst[(rst['TraceData']!='')]['TraceData'])
            else:
                self._app.warningBox('警告','文件路径不能为空')
                return




if __name__ == "__main__":
    app = userGui()
    app.start()







