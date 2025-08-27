import wx
import Login
import pymysql
class Reg(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='注册页面', size=(500, 500))
        self.Center()
        panel = wx.Panel(self)
        # 当使用文本的时候使用StaticText(),pos是距离左上角的 长度，一般等于一个元组
        title = wx.StaticText(panel, label='注册', pos=(180, 10))
        # 设置文本的字体
        font = wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL, faceName='楷体')
        # 把标题的字设置为上面的字体
        title.SetFont(font)
        self.user_name = wx.StaticText(panel, label='昵称', pos=(100, 50), size=(50, 20))
        self.user_name.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.name_label = wx.TextCtrl(panel, pos=(140, 50), size=(190, 20), style=wx.TE_LEFT)
        self.name_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.user_label = wx.StaticText(panel, label='账号', pos=(100, 100), size=(50, 20))
        self.user_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        # 当需要输入框时，需要用TextCtrl,style是设置输入的字体为什么格式，例如wx,TE_LEFT:输入的字体靠左
        self.text_label = wx.TextCtrl(panel, pos=(140, 100), size=(190, 20), style=wx.TE_LEFT)
        self.text_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.user_password = wx.StaticText(panel, label='密码', pos=(100, 150), size=(50, 20))
        self.user_password.SetBackgroundColour(wx.Colour("#00FFFF"))
        # wx.TE_PASSWORD:不显示输入的字体
        self.password = wx.TextCtrl(panel, pos=(140, 150), size=(190, 20), style=wx.TE_PASSWORD)
        self.password.SetBackgroundColour(wx.Colour("#00FFFF"))
        # 当设置按钮时用Button方法
        self.user_password1 = wx.StaticText(panel, label='确认密码', pos=(90, 200), size=(50, 20))
        self.user_password1.SetBackgroundColour(wx.Colour("#00FFFF"))
        # wx.TE_PASSWORD:不显示输入的字体
        self.password1 = wx.TextCtrl(panel, pos=(140, 200), size=(190, 20), style=wx.TE_PASSWORD)
        self.password1.SetBackgroundColour(wx.Colour("#00FFFF"))
        # 当设置按钮时用Button方法
        self.user_phone = wx.StaticText(panel, label='手机号', pos=(100, 250), size=(50, 20))
        self.user_phone.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.phone_label = wx.TextCtrl(panel, pos=(140, 250), size=(190, 20), style=wx.TE_LEFT)
        self.phone_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.user_age = wx.StaticText(panel, label='年龄', pos=(100, 300), size=(50, 20))
        self.user_age.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.age_label = wx.TextCtrl(panel, pos=(140, 300), size=(190, 20), style=wx.TE_LEFT)
        self.age_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.user_sex = wx.StaticText(panel, label='性别', pos=(100, 350), size=(50, 20))
        self.user_sex.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.sex_label = wx.TextCtrl(panel, pos=(140, 350), size=(190, 20), style=wx.TE_LEFT)
        self.sex_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        button2 = wx.Button(panel, label='确认', pos=(120, 400), size=(50, 30))
        button2.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
        button3 = wx.Button(panel, label='返回', pos=(320, 400), size=(50, 30))
        button3.Bind(wx.EVT_BUTTON, self.OnclickBack)
        button2.SetBackgroundColour(wx.Colour("#00FFFF"))
        button3.SetBackgroundColour(wx.Colour("#00FFFF"))

        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("LA(2).jpg")
        dc.DrawBitmap(bmp, 0, 0)


    def OnclickSubmit(self,event):
        mes = ''
        flag = True
        username = self.name_label.GetValue()
        userAccount = self.text_label.GetValue()
        userPassword = self.password.GetValue()
        userPassword1 = self.password1.GetValue()
        userPhone = self.phone_label.GetValue()
        userAge = self.age_label.GetValue()
        userSex = self.sex_label.GetValue()
        if username== '' or userAccount == '' or userPassword == ''or userPhone =='':
            mes = '昵称、账号、密码或手机号不能为空!'
            flag = False
            wx.MessageBox(mes)
            return
        if userAge== '' or userSex == '' :
            mes = '性别或年龄不能为空!'
            flag = False
            wx.MessageBox(mes)
            return
        if userAge!= '':
            for i in userAge:
                if not i.isdigit():
                    mes = '年龄错误！'
                    wx.MessageBox(mes)
                    return
        if len(userPhone) != 11 :
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
        if (userSex != '男' or userSex =='女') and (userSex == '男' or userSex !='女'):
            mes = '性别错误！'
            flag = False
            wx.MessageBox(mes)
            return
        if userPassword != userPassword1:
            mes = '两次输入密码不同!'
            flag = False
            wx.MessageBox(mes)
            return
        if len(userAccount) != 10:
            mes = '账号必须为10位数'
            flag = False
            wx.MessageBox(mes)
            return
        else:
            if not userAccount.isdigit():
                mes = '账号不能有字母!'
                flag = False
                wx.MessageBox(mes)
                return
        if flag:
            db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                                 autocommit=True)
            cursor = db.cursor()
            sql = "SELECT userID From user_table WHERE userID = '%s'"%userAccount
            cursor.execute(sql)
            result = cursor.fetchall()
            if  result:
                mes = '账号已存在!'
                flag=False
                wx.MessageBox(mes)
                return
        if flag:
            db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8',
                                 autocommit=True)
            cursor = db.cursor()
            sql1 = "insert into user_table values('%s','%s','%s',%d,'%s')"%(username,userAccount,userPhone,int(userAge),userSex)
            sql2 = "insert into login_table values('%s','%s')"%(userAccount,userPassword)
            try:
                cursor.execute(sql1)
                cursor.execute(sql2)
            except:
                print("Error:unable to insert data")
                message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
                wx.MessageBox(message)
            db.close()
            mes = '注册成功！'
            wx.MessageBox(mes)

    def OnclickBack(self,event):
        self.Destroy()
        app = wx.App()
        Myfame = Login.MyFrame(None)
        Myfame.Show()
        app.MainLoop()