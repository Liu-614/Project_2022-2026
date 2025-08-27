
# 基于Python的在线互动聊天系统的设计与实现
## 项目背景

本项目为“程序设计综合实践”课程实践项目，旨在开发一个简洁高效的在线互动聊天系统，为用户提供实时通信、好友管理、个人信息修改等功能。系统基于Python和wxPython开发，使用MySQL进行数据存储，支持多用户在线聊天，具备良好的用户体验和系统稳定性。

## 技术栈
- **编程语言**：Python
- **GUI框架**：wxPython
- **数据库**：MySQL 8.0
- **网络通信**：Socket、Threading
- **开发工具**：PyCharm、IntelliJ IDEA
- **操作系统**：Windows 11
---
## 系统功能模块
### 1. 用户注册与登录
- **注册功能**：用户填写昵称、账号、密码、手机号、年龄、性别等信息，系统进行合法性校验并存储至数据库。
- **登录功能**：用户通过账号和密码登录系统，支持安全退出。
#### 代码示例：用户注册功能
```python
class Reg(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='注册页面', size=(500, 500))
        self.Center()
        panel = wx.Panel(self)
        # 创建界面控件
        self.user_name = wx.StaticText(panel, label='昵称', pos=(100, 50), size=(50, 20))
        self.name_label = wx.TextCtrl(panel, pos=(140, 50), size=(190, 20), style=wx.TE_LEFT)
        # 其他控件初始化...
        button2 = wx.Button(panel, label='确认', pos=(120, 400), size=(50, 30))
        button2.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
        # 其他按钮和事件绑定...
    def OnclickSubmit(self, event):
        username = self.name_label.GetValue()
        userAccount = self.text_label.GetValue()
        # 其他输入获取...
        if not username or not userAccount:
            wx.MessageBox("昵称、账号不能为空!")
            return
        # 数据库连接与数据插入
        db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8')
        cursor = db.cursor()
        sql = "INSERT INTO user_table VALUES('%s','%s','%s',%d,'%s')" % (username, userAccount, userPhone, int(userAge), userSex)
        cursor.execute(sql)
        db.commit()
        wx.MessageBox("注册成功!")
```
### 2. 好友管理
- **添加好友**：用户通过输入好友ID发送添加请求，系统验证后更新好友列表。
- **删除好友**：用户选择好友进行删除操作，系统同步更新数据库。
#### 代码示例：添加好友功能
```python
def FriendAdd(self, event):
    userid2 = self.text_label.GetValue()
    sql = "SELECT userName, userID FROM user_table WHERE userID = '%s'" % userid2
    db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    if not result:
        wx.MessageBox("该账号不存在！")
        return
    sql1 = "INSERT INTO user_friends VALUES('%s','%s','%s','%s')" % (self.id, self.name, result[1], result[0])
    cursor.execute(sql1)
    db.commit()
    wx.MessageBox("添加成功!")
```
### 3. 实时聊天
- **消息发送**：用户选择好友后进入聊天界面，输入消息并发送。
- **消息接收**：系统通过Socket通信实现消息的实时接收和显示。
#### 代码示例：消息发送与接收
```python
def wxSend(self, event):
    mes = self.send.GetValue()
    if mes:
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.Msg = mes + "\t\t\t\t%s" % t
        sock.send(self.Msg.encode('utf8'))
        self.chat1.AppendText(self.name + ':' + self.Msg + '\n')
        self.send.Clear()
def recvThreadProcess(self):
    while True:
        try:
            rec_data = sock.recv(1024).decode('utf-8')
            if rec_data:
                self.chat1.AppendText(self.FriendName + ':' + rec_data + '\n')
        except ConnectionAbortedError:
            print("Server closed this connection")
```
### 4. 个人信息修改
- **信息更新**：用户可修改昵称、密码、手机号、年龄等个人信息，系统进行合法性校验并更新数据库。
#### 代码示例：修改个人信息
```python
def OnclickSubmit(self, event):
    username = self.name_label.GetValue()
    userPhone = self.phone_label.GetValue()
    # 其他输入获取...
    if not username or not userPhone:
        wx.MessageBox("昵称、手机号不能为空!")
        return
    db = pymysql.connect(host='localhost', user='root', password='123456', db='wexin', charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE user_table SET username='%s', userPhone='%s' WHERE userID='%s'" % (username, userPhone, self.id)
    cursor.execute(sql)
    db.commit()
    wx.MessageBox("修改成功!")
```
---
## 数据库设计
### 数据库E-R图
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/41317c5e01f7453a8d0aeee131e54819.png#pic_center)

### 主要数据表
1. **用户登录表（UserLogin）**
   | 字段名     | 类型   | 是否为空 | 描述               |
   |------------|--------|----------|--------------------|
   | Account    | String | 否       | 用户账号（主键）   |
   | Password   | String | 否       | 用户密码           |
2. **用户基本信息表（UserInfo）**
   | 字段名     | 类型    | 是否为空 | 描述               |
   |------------|---------|----------|--------------------|
   | Account    | String  | 否       | 用户账号（外键）   |
   | Nickname   | String  | 否       | 用户昵称           |
   | PhoneNumber| String  | 是       | 手机号             |
   | Age        | Integer | 是       | 年龄               |
   | Gender     | String  | 是       | 性别               |
3. **好友表（Friends）**
   | 字段名    | 类型   | 是否为空 | 描述                     |
   |-----------|--------|----------|--------------------------|
   | Account1  | String | 否       | 用户1账号（外键）        |
   | Account2  | String | 否       | 用户2账号（外键）        |
   | SelfName  | String | 否       | 用户1昵称                |
   | FriendName| String | 否       | 用户2昵称                |
4. **消息表（MessageTable）**
   | 字段名       | 类型     | 是否为空 | 描述                     |
   |--------------|----------|----------|--------------------------|
   | SenderID     | String   | 否       | 发送者ID（外键）         |
   | ReceiverID   | String   | 否       | 接收者ID（外键）         |
   | SenderName   | String   | 否       | 发送者昵称               |
   | ReceiverName | String   | 否       | 接收者昵称               |
   | Message      | String   | 否       | 消息内容                 |
   | Time         | DateTime | 否       | 消息发送时间             |
---
## 系统测试
### 测试范围
- **页面显示**：检测所有页面是否正确显示。
- **页面跳转**：验证页面间跳转逻辑是否正确。
- **功能测试**：包括登录、注册、好友管理、聊天、个人信息修改等模块的功能验证。
### 测试用例
#### 登录功能测试
| 输入/动作                     | 期望的输出/响应               |
|-------------------------------|-------------------------------|
| 输入正确的账号和密码          | 提示“登录成功”，跳转至好友列表 |
| 输入错误的账号或密码          | 提示“账号或密码错误”          |
| 不输入账号或密码，点击登录    | 提示“账号或密码不能为空”      |
#### 注册功能测试
| 输入/动作                     | 期望的输出/响应               |
|-------------------------------|-------------------------------|
| 输入完整且合法的信息          | 提示“注册成功”                |
| 输入已存在的账号              | 提示“账号已存在”              |
| 输入不合法的手机号或密码      | 提示相应错误信息              |
---
## 心得体会

通过本次项目，我深入掌握了Python GUI编程、数据库设计及网络通信的实现方法。在开发过程中，我遇到了诸如界面布局优化、数据库连接稳定性、消息实时传输等问题，通过查阅资料和反复调试，逐步解决了这些挑战。我深刻体会到需求分析和系统设计在项目开发中的重要性，同时也提升了团队协作和问题解决能力。未来，我将继续优化系统功能，如增加语音、视频聊天等模块，为用户提供更丰富的交互体验。

