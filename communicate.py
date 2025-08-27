import threading
import wx
import re,pymysql
import time
import FriendsList
import socket
# 创建TCP Socket，类型为服务器之间的网络通信，流式Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 通过IP和端口号连接服务端Socket，类型为服务器之间的网络通信，流式Socket
host = socket.gethostname()  # 获取本地主机名
port = 5000
sock.connect((host, port))
# 向服务器发送连接请求
sock.send(b'1')
# 从服务器接收到的消息
print(sock.recv(1024).decode())


class Communicate(wx.Frame):
    def __init__(self,parent,name,userid,username):
        wx.Frame.__init__(self,parent,title='与'+name+"的对话",size=(1000,700))
        panel =wx.Panel(self)
        self.Center()
        pattern = r"\d{10}"  # 匹配连续的10位数字
        result = re.findall(pattern, name)
        final_result = result[0]
        sql = "SELECT * From message_table WHERE userID1 = '%s' AND userID2 = '%s' ORDER BY time asc"%(userid,final_result)
        # 设置文本框的内容
        self.id = userid
        self.FriendID = final_result
        name2 =re.sub(pattern,'',name)
        self.FriendName = name2.rstrip('()')
        '''self.communication=[]
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                if userid == row[0]:
                    word = '' %s
                                                   我： %s           '' % (row[3], row[1])
                    self.communication.append(word)
                else:
                    word2 = '' %s
                                                   %s： %s           '' % (row[3], name, row[1])
                    self.communication.append(word2)
        except:
            print('koko')
            print("Error:unable to fetch data")
            message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
            wx.MessageBox(message)
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        wx.ListBox(panel, -1, (10, 10), (540, 400), choices=self.communication, style=wx.LB_SINGLE, )
        '''
        self.chat1 = wx.TextCtrl(panel, -1, pos=(10,10), size= (540,400), style = wx.TE_MULTILINE)
        self.chat1.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.send = wx.TextCtrl(panel,pos=(10,420),size=(500,200),style=wx.TE_LEFT)
        self.send.SetBackgroundColour(wx.Colour("#00FFFF"))
        button = wx.Button(panel, label='发送', pos=(520, 450), size=(50, 80))
        button.Bind(wx.EVT_BUTTON,self.wxSend)
        button1 = wx.Button(panel, label='返回', pos=(520, 580), size=(50, 80))
        button1.Bind(wx.EVT_BUTTON,self.ClickBack)
        button.SetBackgroundColour(wx.Colour("#00FFFF"))
        button1.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.name = username
        sql = "SELECT userFriendID,userFriendName From user_friends WHERE userID = '%s'" % userid
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        friends = []
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                friend = row[1] + '(%s)' % row[0]
                friends.append(friend)
        except:
            print("Error:unable to fetch data")
            message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
            wx.MessageBox(message)
        sql1 = "SELECT userHostName From user_friends WHERE userID = '%s'" % userid
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        cursor.execute(sql1)
        result1 = cursor.fetchone()
        self.name = result1[0]
        db.close()
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.list = wx.ListBox(panel, -1, choices=friends, style=wx.LB_SINGLE, )
        self.list.SetBackgroundColour(wx.Colour("#00FFFF"))
        hbox.Add(self.list, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.chat1, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.send, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(button, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(button1, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        hbox.Add(vbox, proportion=1, flag=wx.EXPAND)
        self.Bind(wx.EVT_LISTBOX, self.on_combobox, self.list)
        panel.SetSizer(hbox)
        sock.send(self.name.encode('utf8'))
        self.recvThread = threading.Thread(target=self.recvThreadProcess)
        self.recvThread.setDaemon = True
        self.recvThread.start()
        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("LA(4).jpg")
        dc.DrawBitmap(bmp, 0, 0)
    def on_combobox(self, event):
        list = event.GetString()
        pattern = r"\d{10}"  # 匹配连续的10位数字
        result = re.findall(pattern, list)
        self.Destroy()
        app = wx.App()  # 创建一个wx.App实例
        frame = Communicate(parent=None,username=self.name ,name=list,userid=self.id)  # 实列化MyFrame
        frame.Show()  # 显示窗口
        app.MainLoop()  # 这个方法将程序的控制权转交给wxPython

    def wxSend(self,event):
        #向客户端发送消息
        mes = self.send.GetValue()
        if mes:
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.Msg = mes + "\t\t\t\t%s" % t
            sock.send(self.Msg.encode('utf8'))
            self.chat1.AppendText(self.name + ':' + self.Msg + '\n')
        '''self.chat1.WriteText(self.Msg)
        self.chat1.WriteText('\n')
        '''
        self.send.Clear()

    def recvThreadProcess(self):
        while True:
            try:
                rec_data = sock.recv(1024).decode('utf-8')
                if rec_data is not None:
                    #print('收到的消息:'+rec_data)
                    #print('\n朋友：'+self.FriendName)
                    #print(self.FriendName + ':'+rec_data+'\n')
                    self.chat1.AppendText(self.FriendName + ':'+rec_data+'\n')
            except ConnectionAbortedError:
                print("Sever closed this connection")
            except ConnectionResetError:
                print('Server is closed')

    '''def ClientMessage(self):
        t = threading.Thread(target=self.rec)
        t.setDaemon=True
        t.start()
        wx.CallLater(3,self.ClientMessage())
    '''
    '''
    def rec(self):
        rec_data = sock.recv(1024).decode('utf-8')
        if rec_data is not None :
            self.chat1.AppendText(self.FriendName+':')
            self.chat1.WriteText(rec_data)
            self.chat1.WriteText("\n")
    '''

    '''
    def clickSend(self,event):
        send_text = self.send.GetValue()
        t=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        sql = "INSERT into message_table values('%s','%s','%s','%s')"%(self.id,send_text,self.FriendID,t)
        try:
            cursor.execute(sql)
        except:
            print("Error:unable to insert data")
            message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
            wx.MessageBox(message)
        self.send.SetValue('')

    '''
    def ClickBack(self,event):
        self.Destroy()
        app = wx.App()
        Myfame = FriendsList.Friends(parent=None, userid=self.id)
        Myfame.Show()
        app.MainLoop()

class friList(wx.Frame):
    def __init__(self,parent,userid):
        wx.Frame.__init__(self, parent, title='好友列表', size=(500, 640))
        self.Center()
        panel = wx.Panel(self)
        self.id = userid
        sql = "SELECT userFriendID,userFriendName From user_friends WHERE userID = '%s'" % userid
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        friends = []
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                friend = row[1] + '(%s)' % row[0]
                friends.append(friend)
        except:
            print("Error:unable to fetch data")
            message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
            wx.MessageBox(message)
        sql1 = "SELECT userHostName From user_friends WHERE userID = '%s'" % userid
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        cursor.execute(sql1)
        result1 = cursor.fetchone()
        self.name = result1[0]
        db.close()
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.list = wx.ListBox(panel, -1, (10, 10), (400, 400), choices=friends, style=wx.LB_SINGLE, )
        self.Bind(wx.EVT_LISTBOX, self.on_combobox, self.list)


if __name__ == '__main__':
    app = wx.App()  # 创建一个wx.App实例
    frame = Communicate(parent=None,name='刘翔',userid="123")  # 实列化MyFrame
    frame.Show()  # 显示窗口
    app.MainLoop()  # 这个方法将程序的控制权转交给wxPython