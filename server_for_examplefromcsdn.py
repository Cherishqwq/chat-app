from socket import *
from sqlite3 import connect
import threading
from datetime import *
from user_info import newuser,vertify
 
# 记录系统时间
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'                     
 
# 设置IP地址和端口号(均为私有本地)


IP = '127.0.0.1'
PORT = 30000
dbname='user.db'
temp=['刘俊源_server','1234','yhy','临时','123456']



#!!自检数据库状态

user_list = []
socket_list = []
 
# 聊天记录存储至serverlog.txt文件中
try:
    with open('serverlog.txt', 'a+') as serverlog:                    
        curtime = datetime.now().strftime(ISOTIMEFORMAT)
        serverlog.write('\n-----------server startup '+str(curtime)+', recording-----------\n')
        print('\
  ______    ______    ____     __  ___    ____    _   __    ___      __ \n\
 /_  __/   / ____/   / __ \   /  |/  /   /  _/   / | / /   /   |    / / \n\
  / /     / __/     / /_/ /  / /|_/ /    / /    /  |/ /   / /| |   / /  \n\
 / /     / /___    / _  _/  / /  / /   _/ /    / /|  /   / ___ |  / /___\n\
/_/     /_____/   /_/ |_|  /_/  /_/   /___/   /_/ |_/   /_/  |_| /_____/\n')
        print("server startup")
except:
    print('ERROR!')
 
 
# 读取套接字连接
s = socket()
s.bind((IP, PORT))
s.listen()



# 接收Client端上线、离线、消息并发送
def read_client(s, nickname):
    try:
        info=s.recv(2048).decode('utf-8')  # 获取此套接字（用户）发送的消息
        if info=='\exit':                                                     # 一旦断开连接则记录log以及向其他套接字发送相关信息
            curtime = datetime.now().strftime(ISOTIMEFORMAT)        # 获取当前时间
            print(curtime)
            print(nickname + ' 离线')
            s.send(('endre').encode('utf-8'))
            s.close()
            with open('serverlog.txt', 'a+') as serverlog:          # log记录
                serverlog.write(str(curtime) + '  ' + nickname + ' 离线\n')
            socket_list.remove(s)
            user_list.remove(nickname)
            for client in socket_list:                              # 其他套接字通知（即通知其他聊天窗口）
                client.send(('#'+ nickname + ' 离线').encode('utf-8'))
            return ''
        return info
    except Exception as e:
        print(e)
  
#记录消息
def socket_target(s, nickname):                        
    try:
        s.send(  (  ','.join(user_list)   ).encode('utf-8'))               # 首次推送 将用户列表送给各个套接字，用逗号隔开
        while True:
            content = read_client(s, nickname)                      # 获取用户发送的消息
            if content == '':
                break
            else:
                curtime = datetime.now().strftime(ISOTIMEFORMAT)    # 系统时间打印
                print(curtime)
                print(nickname+'：“'+content+'”')


                with open('serverlog.txt', 'a+') as serverlog:      # log记录
                    serverlog.write(str(curtime) + '  ' + nickname + '： ' + content + '\n')
                for client in socket_list:                          # 其他套接字通知
                    client.send((nickname + ': '+ content).encode('utf-8'))
    except Exception as e:
        print(e)

#上线、昵称
while True:                                                     # 不断接受新的套接字进来，实现“多人”
    conn, addr = s.accept()                                     # 获取套接字与此套接字的地址(一个客户端)
    nickname = conn.recv(2048).decode('utf-8')                  # 接受昵称
    conn.send(('ok').encode('utf-8'))
    key=conn.recv(2048).decode('utf-8')
    liORsu=conn.recv(3).decode('utf-8')
    if liORsu =='sig':
        a=newuser(database_name=dbname,name=nickname,password=key,info='')
        conn.send(('ok').encode('utf-8'))
        print(nickname+'signs up.')
    checkclass=vertify(nickname,key)                               #验证用户
    flag=checkclass.vertify_user()
    if flag!=1:
        conn.send(('err1').encode('utf-8'))
        print("try to login:",nickname,",k=",key)
    else:
        conn.send(('ac1').encode('utf-8'))
        socket_list.append(conn) # 套接字列表更新
        if nickname in user_list:                                   # 昵称查重，相同则在后面加上数字
            i = 1
            while True:
                if nickname+str(i) in user_list:
                    i = i + 1
                else:
                    nickname = nickname + str(i)
                    break
    
        user_list.append(nickname)                                  # 用户列表更新，加入新用户（新的套接字）
        curtime = datetime.now().strftime(ISOTIMEFORMAT)
        print(curtime)
        print(nickname + ' 上线')



        with open('serverlog.txt', 'a+') as serverlog:              # log记录
            serverlog.write(str(curtime) + '  ' + nickname + ' 上线\n')
    
        for client in socket_list[0:len(socket_list)-1]:            # 其他套接字通知
            client.send(('#'+ nickname + ' 上线').encode('utf-8'))


            # 加入线程中跑，加入函数为socket_target，参数为conn,nickname
        threading.Thread(target=socket_target, args=(conn,nickname,)).start()




    '''TCP服务端：

    创建套接字，绑定套接字到本地IP与端口

    # socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.bind()

    开始监听连接 #s.listen()

    进入循环，不断接受客户端的连接请求 #s.accept()

    然后接收传来的数据，并发送给对方数据 #s.recv() , s.sendall()

    传输完毕后，关闭套接字 #s.close()


    ---------------------

    TCP客户端:

    创建套接字，连接远端地址

    # socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.connect()

    连接后发送数据和接收数据 # s.sendall(), s.recv()

    传输完毕后，关闭套接字 #s.close()'''