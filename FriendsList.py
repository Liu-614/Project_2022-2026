import wx
import pymysql, Login
import communicate
import re
class Friends(wx.Frame):
    def __init__(self,parent,userid):
        wx.Frame.__init__(self, parent, title='好友列表',size=(500,640))
        self.Center()
        panel = wx.Panel(self)
        self.id=userid
        sql = "SELECT userFriendID,userFriendName From user_friends WHERE userID = '%s'"%userid
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        friends = []
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                friend = row[1] +'(%s)' % row[0]
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
        self.box=wx.BoxSizer(wx.HORIZONTAL)
        self.list = wx.ListBox(panel, -1 ,(10,10),(400,400),choices=friends,style=wx.LB_SINGLE,)
        self.list.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.Bind(wx.EVT_LISTBOX,self.on_combobox,self.list)
        self.button0 = wx.Button(panel, label='删除好友', pos=(80, 480), size=(80, 50))
        self.button0.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.Bind(wx.EVT_BUTTON, self.FriendDelete, self.button0)
        self.button1 = wx.Button(panel, label='添加好友', pos=(320, 480), size=(80, 50))
        self.button1.SetBackgroundColour(wx.Colour("#00FFFF"))
        # 当按下这个按钮时将会做出相应的反应，这里是调用 OnclickCancel()函数
        self.Bind(wx.EVT_BUTTON, self.FriendAdd, self.button1)
        self.button2 = wx.Button(panel, label='退出登录', pos=(200, 540), size=(80, 50))
        self.button2.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.Bind(wx.EVT_BUTTON, self.ExitBack,self.button2)
        self.button3 = wx.Button(panel, label='修改信息', pos=(200, 480), size=(80, 50))
        self.button3.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.Bind(wx.EVT_BUTTON, self.Modify_information,self.button3)
        self.id=userid

        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("LA(3).jpg")
        dc.DrawBitmap(bmp, 0, 0)

    def on_combobox(self, event):
        list = event.GetString()
        pattern = r"\d{10}"  # 匹配连续的10位数字
        result = re.findall(pattern, list)
        self.Destroy()
        app = wx.App()  # 创建一个wx.App实例
        frame = communicate.Communicate(parent=None,username=self.name ,name=list,userid=self.id)  # 实列化MyFrame
        frame.Show()  # 显示窗口
        app.MainLoop()  # 这个方法将程序的控制权转交给wxPython
    def FriendDelete(self,event):
        self.Destroy()
        app = wx.App()  # 创建一个wx.App实例
        frame = FriendOperate(parent=None,Operate='删除',userid1=self.id)  # 实列化MyFrame
        frame.Show()  # 显示窗口
        app.MainLoop()  # 这个方法将程序的控制权转交给wxPython

    def FriendAdd(self,event):
        self.Destroy()
        app = wx.App()  # 创建一个wx.App实例
        frame = FriendOperate(parent=None, Operate='添加', userid1=self.id)  # 实列化MyFrame
        frame.Show()  # 显示窗口
        app.MainLoop()  # 这个方法将程序的控制权转交给wxPython

    def ExitBack(self,event):
        self.Destroy()
        app = wx.App()  # 创建一个wx.App实例
        frame = Login.MyFrame(parent=None)  # 实列化MyFrame
        frame.Show()  # 显示窗口
        app.MainLoop()  # 这个方法将程序的控制权转交给wxPython

    def Modify_information(self,event):
        self.Destroy()
        app = wx.App()  # 创建一个wx.App实例
        frame = Modify_information(parent=None,userid=self.id)  # 实列化MyFrame
        frame.Show()  # 显示窗口
        app.MainLoop()  # 这个方法将程序的控制权转交给wxPython

class FriendOperate(wx.Frame):
    def __init__(self,parent,Operate,userid1):
        wx.Frame.__init__(self,parent,title = Operate+'好友',size=(400,300))
        panel = wx.Panel(self)
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        sql = "SELECT username From user_table WHERE userID = %s"%userid1
        cursor.execute(sql)
        result = cursor.fetchone()
        self.name = result[0]
        db.close()
        self.user_label = wx.StaticText(panel, label='请输入id', pos=(30, 50), size=(50, 20))
        # 当需要输入框时，需要用TextCtrl,style是设置输入的字体为什么格式，例如wx,TE_LEFT:输入的字体靠左
        self.text_label = wx.TextCtrl(panel, pos=(100, 50), size=(190, 20), style=wx.TE_LEFT)
        button0 = wx.Button(panel, label='确认', pos=(100, 150), size=(50, 30))
        button1 = wx.Button(panel, label='返回', pos=(200, 150), size=(50, 30))
        button1.Bind(wx.EVT_BUTTON, self.ClickBack)
        if Operate == '删除':
            self.Bind(wx.EVT_BUTTON, self.FriendDelete, button0)
        else:
            self.Bind(wx.EVT_BUTTON, self.FriendAdd, button0)
        self.id=userid1
    def FriendDelete(self,event):
        userid = self.text_label.GetValue()
        sql = "SELECT userFriendID From user_friends WHERE userFriendID = '%s'"%userid
        sql1 = "DElETE From user_friends WHERE userFriendID = '%s'" % userid
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if not result:
                mes = '该账号没有在你的好友中...'
                wx.MessageBox(mes)
            else:
                cursor.execute(sql1)
                message = '操作成功！'
                wx.MessageBox(message)
        except:
            print("Error:unable to fetch data")
            message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
            wx.MessageBox(message)

    def FriendAdd(self,event):
        userid2 = self.text_label.GetValue()
        sql = "SELECT userName,userID From user_table WHERE userid = '%s'" % userid2
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                             autocommit=True)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        try:
            if not result:
                mes = '该账号不存在！'
                wx.MessageBox(mes)
                return
            else:
                print(self.id, self.name, result[1], result[0])
                sql1 = "insert into user_friends values('%s','%s','%s','%s')" % (
                self.id, self.name, result[1], result[0])
                cursor.execute(sql1)
                mes = '操作成功'
                wx.MessageBox(mes)
        except:
            print("Error:unable to fetch data")
            message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
            wx.MessageBox(message)

        db.close()
    def ClickBack(self,event):
        self.Destroy()
        app = wx.App()  # 创建一个wx.App实例
        frame = Friends(parent=None,userid=self.id)  # 实列化MyFrame
        frame.Show()  # 显示窗口
        app.MainLoop()  # 这个方法将程序的控制权转交给wxPython

class Modify_information(wx.Frame):
    def __init__(self, parent, userid):
        wx.Frame.__init__(self, parent, title='修改页面', size=(500, 400))
        self.Center()
        panel = wx.Panel(self)
        # 当使用文本的时候使用StaticText(),pos是距离左上角的 长度，一般等于一个元组
        title = wx.StaticText(panel, label='修改个人信息', pos=(180, 10))
        # 设置文本的字体
        font = wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL, faceName='楷体')
        # 把标题的字设置为上面的字体
        title.SetFont(font)
        self.user_name = wx.StaticText(panel, label='昵称', pos=(100, 50), size=(50, 20))
        self.user_name.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.name_label = wx.TextCtrl(panel, pos=(140, 50), size=(190, 20), style=wx.TE_LEFT)
        self.name_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.user_password = wx.StaticText(panel, label='密码', pos=(100, 100), size=(50, 20))
        self.user_password.SetBackgroundColour(wx.Colour("#00FFFF"))
        # wx.TE_PASSWORD:不显示输入的字体
        self.password = wx.TextCtrl(panel, pos=(140, 100), size=(190, 20), style=wx.TE_PASSWORD)
        self.password.SetBackgroundColour(wx.Colour("#00FFFF"))
        # 当设置按钮时用Button方法
        self.user_password1 = wx.StaticText(panel, label='确认密码', pos=(90, 150), size=(50, 20))
        self.user_password1.SetBackgroundColour(wx.Colour("#00FFFF"))
        # wx.TE_PASSWORD:不显示输入的字体
        self.password1 = wx.TextCtrl(panel, pos=(140, 150), size=(190, 20), style=wx.TE_PASSWORD)
        self.password1.SetBackgroundColour(wx.Colour("#00FFFF"))
        # 当设置按钮时用Button方法
        self.user_phone = wx.StaticText(panel, label='手机号', pos=(100, 200), size=(50, 20))
        self.user_phone.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.phone_label = wx.TextCtrl(panel, pos=(140, 200), size=(190, 20), style=wx.TE_LEFT)
        self.phone_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.user_age = wx.StaticText(panel, label='年龄', pos=(100, 250), size=(50, 20))
        self.user_age.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.age_label = wx.TextCtrl(panel, pos=(140, 250), size=(190, 20), style=wx.TE_LEFT)
        self.age_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        button2 = wx.Button(panel, label='确认', pos=(120, 300), size=(50, 30))
        button2.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
        button3 = wx.Button(panel, label='返回', pos=(320, 300), size=(50, 30))
        button3.Bind(wx.EVT_BUTTON, self.ClickBack)
        button2.SetBackgroundColour(wx.Colour("#00FFFF"))
        button3.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.id = userid
        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def OnclickSubmit(self,event):
        mes = ''
        flag = True
        username = self.name_label.GetValue()
        userPassword = self.password.GetValue()
        userPassword1 = self.password1.GetValue()
        userPhone = self.phone_label.GetValue()
        userAge = self.age_label.GetValue()
        if username == '' or userPassword == '' or userPhone == '':
            mes = '昵称、密码或手机号不能为空!'
            flag = False
            wx.MessageBox(mes)
            return
        if userAge == '':
            mes = '年龄不能为空!'
            flag = False
            wx.MessageBox(mes)
            return
        if userAge != '':
            for i in userAge:
                if not i.isdigit():
                    mes = '年龄错误！'
                    wx.MessageBox(mes)
                    return
        if len(userPhone) != 11:
            mes = '手机号必须为11位！'
            flag = False
            wx.MessageBox(mes)
            return
        else:
            for i in userPhone:
                if not i.isdigit():
                    mes = '手机号错误！'
                    flag = False
                    wx.MessageBox(mes)
                    return
        if userPassword != userPassword1:
            mes = '两次输入密码不同!'
            flag = False
            wx.MessageBox(mes)
            return
        if flag:
            db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                                 autocommit=True)
            cursor = db.cursor()
            sql = "UPDATE login_table SET userPassword = '%s' WHERE userID = '%s'" %(userPassword,self.id)
            sql1 = "UPDATE user_table SET username = '%s', userPhone = '%s', userAge = '%s' WHERE userID = '%s'" % (username,userPhone,userAge,self.id)
            try:
                cursor.execute(sql)
                cursor.execute(sql1)
            except:
                print("Error:unable to insert data")
                message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
                wx.MessageBox(message)
            db.close()
            mes = '修改成功！'
        wx.MessageBox(mes)

    def ClickBack(self,event):
        self.Destroy()
        app = wx.App()
        Myfame = Friends(parent=None, userid=self.id)
        Myfame.Show()
        app.MainLoop()

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("LA(5).jpg")
        dc.DrawBitmap(bmp, 0, 0)

if __name__ == '__main__':
    app = wx.App()  # 创建一个wx.App实例
    frame = Friends(parent=None,userid='123')  # 实列化MyFrame
    frame.Show()  # 显示窗口
    app.MainLoop()  # 这个方法将程序的控制权转交给wxPython