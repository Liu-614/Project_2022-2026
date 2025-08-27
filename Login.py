import wx  # 导入wxpython
import Register, FriendsList
import pymysql
# wx.Frame是所有的框架的父类，当创建字类的时候应该应该要调用父类的构造器wx.Frame.__init__()
class MyFrame(wx.Frame):
    '''parent:框架的父窗口，如果是顶级窗口那么值为None
       id:当值为-1时，让wxpython自动生成一个id号
       title：里面的内容为窗口的标题
       size:为窗口的大小，前面一位为长度，后面因为为宽度
       '''

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='登录页面', size=(500, 300))
        self.Center()
        panel = wx.Panel(self)
        # 当使用文本的时候使用StaticText(),pos是距离左上角的长度，一般等于一个元组
        title = wx.StaticText(panel, label='账号和密码', pos=(180, 10))
        title.SetBackgroundColour(wx.Colour("#00FF00"))
        # 设置文本的字体
        font = wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL, faceName='楷体')
        # 把标题的字设置为上面的字体
        title.SetFont(font)
        self.user_label = wx.StaticText(panel, label='账 号:', pos=(100, 50), size=(50, 20))
        self.user_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        # 当需要输入框时，需要用TextCtrl,style是设置输入的字体为什么格式，例如wx,TE_LEFT:输入的字体靠左
        self.text_label = wx.TextCtrl(panel, pos=(140, 50), size=(190, 20), style=wx.TE_LEFT)
        self.text_label.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.user_password = wx.StaticText(panel, label='密 码:', pos=(100, 100), size=(50, 20))
        self.user_password.SetBackgroundColour(wx.Colour("#00FFFF"))
        # wx.TE_PASSWORD:不显示输入的字体
        self.password = wx.TextCtrl(panel, pos=(140, 100), size=(190, 20), style=wx.TE_PASSWORD)
        self.password.SetBackgroundColour(wx.Colour("#00FFFF"))
        # 当设置按钮时用Button方法
        button0 = wx.Button(panel, label='注册', pos=(80, 160), size=(50, 30))
        self.Bind(wx.EVT_BUTTON,self.OnclickRegister,button0)
        button0.SetBackgroundColour(wx.Colour("#00FFFF"))
        button1 = wx.Button(panel, label='登录', pos=(200, 160), size=(50, 30))
        # 当按下这个按钮时将会做出相应的反应，这里是调用 OnclickCancel()函数
        button1.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.Bind(wx.EVT_BUTTON, self.OnclickSubmit,button1)
        button2 = wx.Button(panel, label='退出', pos=(320, 160), size=(50, 30))
        button2.SetBackgroundColour(wx.Colour("#00FFFF"))
        self.Bind(wx.EVT_BUTTON, self.OnclickExit,button2)
        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("LA(1).jpg")
        dc.DrawBitmap(bmp, 0, 0)


    def OnclickSubmit(self, event):
        message = ''
        userid = self.text_label.GetValue()
        password = self.password.GetValue()
        db = pymysql.connect(host= 'localhost',user= 'root', password= '123456',db= 'wexin',charset= 'utf8', autocommit= True)
        cursor = db.cursor()
        sql = "SELECT * FROM login_table"
        if userid == '' or password == '':
            message = '账号和密码不能为空'
            wx.MessageBox(message)  # 弹出提示框
            return
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            flag=False
            for row in result:
                if row[0] == userid and row[1] == password:
                    message = '登录成功'
                    wx.MessageBox(message)  # 弹出提示框
                    self.Destroy()
                    app = wx.App()
                    List = FriendsList.Friends(parent=None, userid=userid)
                    List.Show()
                    app.MainLoop()
                    flag=True
                    break
            if not flag:
                message = '账号或密码错误！'
                wx.MessageBox(message)
        except:
            print("Error:unable to fetch data")
            message = ',,Ծ‸Ծ,,服务器出现了问题！,,Ծ‸Ծ,,'
            wx.MessageBox(message)
        db.close()

    def OnclickExit(self, event):
        wx.Exit()

    def OnclickRegister(self, event):
        self.Destroy()
        app = wx.App()
        frame2 = Register.Reg(None)
        frame2.Show()
        app.MainLoop()



if __name__ == '__main__':
    app = wx.App()  # 创建一个wx.App实例
    frame = MyFrame(parent=None)  # 实列化MyFrame
    frame.Show()  # 显示窗口
    app.MainLoop()  # 这个方法将程序的控制权转交给wxPython
