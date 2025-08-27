import socket
import threading


# 创建TCP Socket， 类型为服务器之间网络通信，流式Socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()  # 获取本地主机名
port = 5000
mySocket.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
# 绑定服务端的IP和端口
mySocket.bind((host,port))
# 开始监听TCP传入连接，并设置操作系统可以挂起最大连接数量
mySocket.listen(5)
print('Server was started by ', socket.gethostbyname('localhost'),'now is listening...')
# 创建字典，用于存储客户端的连接
mydict = dict()
# 创建列表，用于存储客户端的连接
mylist = list()
# 把聊天信息发送给除自己以外的所有人
def chatMsgToOthers(exceptMe, chatMsg):
    for c in mylist:
        if c.fileno() != exceptMe:
            try:
                # 向客户端发送消息
                c.send(chatMsg.encode('utf8'))
            except:
                print("Error! Error code: 500")

def subThreadProcess(myConnection, connNum):
    # 接收客户端
    username = myConnection.recv(1024).decode('utf8')
    mydict[myConnection.fileno()]= username
    mylist.append(myConnection)
    print('client connect number:',connNum, 'has nickname :',username)
    #chatMsgToOthers(connNum,'* 系统提示：'+ username + '已经进入聊天室，赶快和TA打招呼吧 *')
    while True :
        try:
            # 接收客户端消息
            recvedMsg =  myConnection.recv(1024).decode('utf8')
            if recvedMsg:
                print(mydict[connNum], ':',recvedMsg)
                chatMsgToOthers(connNum,recvedMsg)
        except(OSError,ConnectionError):
            try:
                mylist.remove(myConnection)
            except:
                print("Error! Error code: 500")
            print(mydict[connNum],'was exit, ',len(mylist), 'person left!')
            chatMsgToOthers(connNum, '* 系统提示：'+ mydict[connNum]+ '已经离开聊天室 *')
            myConnection.close()
            return
while True :
    # 接受TCP连接并返回(connection, address) ，其中connection是新的Socket对象，可以用来接收和发送数据，address是连接客户端的地址
    connection, address = mySocket.accept()
    print('Accept a new connection', connection.getsockname(), connection.fileno())
    try:
        # 接收客户端消息
        buf = connection.recv(1024).decode('utf8')
        if buf == '1':
            # 向客户端发送消息
            connection.send(b'connection success, welcome to chat room!')
            # 为当前连接创建一个新的子线程来保持通信
            myThread = threading.Thread(target=subThreadProcess, args=(connection, connection.fileno()))
            myThread.setDaemon=True
            myThread.start()
        else:
            # 向客户端发送消息
            connection.send(b'connection fall, please go out !')
            connection.close()
    except:
        print("Error! Error code: 500")