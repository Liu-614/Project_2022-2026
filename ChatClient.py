import socket
import threading

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
username = input('input your username:')
# 向服务器端发送聊天用户名
sock.send(username.encode())
# 向服务器端发送消息的处理逻辑
def sendThreadProcess():
    while True:
        try:
            myMsg = input('me:')
            sock.send(myMsg.encode())
        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed')
#向服务器端接收消息的处理逻辑
def recvThreadProcess():
    while True:
        try:
            otherMsg = sock.recv(1024)
            if otherMsg:
                print(otherMsg.decode())
            else:
                print("Error! Error code: 500")
        except ConnectionAbortedError:
            print("Sever closed this connection")
        except ConnectionResetError:
            print('Server is closed')
# 创建发送和接收消息的子线程
sendThread = threading.Thread(target=sendThreadProcess)
recvThread = threading.Thread(target=recvThreadProcess)
threads = [sendThread, recvThread]
for t in threads:
    t.setDaemon=True
    t.start()
t.join()
