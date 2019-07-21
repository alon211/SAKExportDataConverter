import xml.sax

class dbHandle(xml.sax.ContentHandler):
    def __init__(self):
        self._Type=''
        self._HostName=''
        self._UserName=''
        self._PassWord=''
        self._DBName=''
        self._ServerName=''
        self._TimeOut=''
        self.CurrentData=''
    def startElement(self,tag,attributes):
        self.CurrentData=tag
        if self.CurrentData=='Common':
            self._Type=attributes['Type']
            self._HostName=attributes['HostName']
            self._UserName=attributes['UserName']
            self._PassWord=attributes['PassWord']
            self._DBName=attributes['DBName']
            self._ServerName=attributes['ServerName']
            self._TimeOut=attributes['TimeOut']




    def endElement(self,tag):
        self.CurrentData=''
    def characters(self,content):
        # if content=='Common':
        pass
    @property
    def Type(self):
        return self._Type
    @property
    def DBName(self):
        return self._DBName
    @property
    def PassWord(self):
        return self._PassWord
    @property
    def ServerName(self):
        return self._ServerName
    @property
    def TimeOut(self):
        return self._TimeOut
    @property
    def UserName(self):
        return self._UserName
    @property
    def HostName(self):
        return self._HostName


# parser=xml.sax.make_parser()
# # turn off namepsaces
# parser.setFeature(xml.sax.handler.feature_namespaces, 0)
# # 重写
# instance_dbHandle = dbHandle()
# parser.setContentHandler(instance_dbHandle)
#
# parser.parse('dbconnect.xml')
# print(instance_dbHandle.DBName)




