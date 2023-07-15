from tkinter import *
from datetime import *
from socket import *
#from user_info import userop
import threading
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
 
IPpublic='163.53.247.57'
portpublic=52169
#公网IP 若为TCP协议可以cmd PING  注意公私端口区别  #私：127.0.0.1：30000
version='0.0.3  '


ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'         # 时间格式声明
s = socket()                                # 套接字
# 登录窗口
def Login_gui_run():                                            
    root = Tk()
    root.title("welcome_v."+version)          # 窗口标题
    frm = Frame(root)
    root.geometry('400x300')  
    nickname = StringVar()# 昵称变量
    password = StringVar()  
    s.connect((IPpublic,portpublic))                                     # 建立连接  公网IP 若为TCP协议可以cmd PING  注意公私端口区别  #私：127.0.0.1：30000

    ###登录
    def login_in():                                             
        name = nickname.get()                                   # 长度是考虑用户列表那边能否完整显示
        if not name:
            tkinter.messagebox.showwarning('Warning', message='Enter your name please.')
        elif len(name)>13:
            tkinter.messagebox.showwarning('Warning', message='max length=13.')
        else:                                  
            key = password.get()                                   
            if not key:
                tkinter.messagebox.showwarning('Warning', message='Enter your key please.')
            elif len(key)>30:
                password.set('')
            else:
                                    
                s.send(name.encode('utf-8'))# 传递用户昵称
                if s.recv(2).decode('utf-8') != 'ok':
                    tkinter.messagebox.showwarning('Warning', message='connection err.')
                    root.destroy()
                s.send(key.encode('utf-8'))
                s.send('log'.encode('utf-8'))
                if s.recv(4).decode('utf-8') == 'err1':
                    tkinter.messagebox.showwarning('Warning', message='password err.')
                    root.destroy() 
                else:
                    root.destroy() 
                    Chat_gui_run()                                      # 打开聊天窗口 
                    
    def sign_up():
        name = nickname.get()                                   # 长度是考虑用户列表那边能否完整显示
        if not name:
            tkinter.messagebox.showwarning('Warning', message='Enter your name please.')
        elif len(name)>13:
            tkinter.messagebox.showwarning('Warning', message='max length=13.')
        else:                                  
            key = password.get()                                   
            if not key:
                tkinter.messagebox.showwarning('Warning', message='Enter your key please.')
            elif len(key)>30:
                password.set('')
                
            else:
                #s.connect((IPpublic,portpublic))                     # 建立连接  公网IP 若为TCP协议可以cmd PING  注意公私端口区别  #私：127.0.0.1：30000
                s.send(name.encode('utf-8'))# 传递用户昵称
                if s.recv(2).decode('utf-8') != 'ok':
                    tkinter.messagebox.showwarning('Warning', message='connection err.')
                    root.destroy()
                s.send(key.encode('utf-8'))
                s.send('sig'.encode('utf-8'))
                if s.recv(2).decode('utf-8')=='ok':
                    tkinter.messagebox.showwarning('Warning', message='Sign up completed.√')
                    root.destroy()
                    s.recv(3).decode('utf-8')
                    Chat_gui_run()
                        
 
    # 按钮、输入提示标签、输入框

    Label(root, text='username🆔', font=('Verdana',11)).place(x=25, y=80, height=50, width=90)
    Entry(root, textvariable = nickname, font=('等线', 11)).place(x=135, y=90, height=30, width=200)

    Label(root, text='password🔑', font=('Verdana',11)).place(x=25, y=120, height=50, width=90)
    Entry(root, textvariable = password, font=('Fangsong', 11),show='-').place(x=135, y=130, height=30, width=200)
    
    Label(root, text='Notice: The maxium number of online users is *20*.', font=('Verdana',8),fg='dimgray').place(x=1, y=175, height=50, width=398)
    Button(root, text = ">", font=('Verdana', 12),bg='aqua',fg='black',command = login_in, width = 8, height = 1).place(x=150, y=230, width=100, height=35)

    Button(root, text = "sign up",relief='flat', font=('Verdana', 8),fg='thistle',activeforeground='white',command = sign_up, width = 8, height = 1).place(x=175, y=270, width=50, height=19)
    
    root.mainloop()
 

  

# 聊天窗口
def Chat_gui_run():         
    window = Tk()
    window.maxsize(800, 400)                                # 设置相同的最大最小尺寸，将窗口大小固定
    window.minsize(800, 400)
 
    var1 = StringVar()
    user_list = []
    user_list = s.recv(2048).decode('utf-8').split(',')     # 从服务器端获取当前用户列表
    user_list.insert(0, '------online user------')
 
 
    nickname = user_list[len(user_list)-1]                  # 获取正式昵称，经过了服务器端的查重修改
    window.title("chat:"+nickname)                  
    var1.set(user_list)                                     # 用户列表文本设置
    # var1.set([1,2,3,5])
    listbox1 = Listbox(window, listvariable=var1)           # 用户列表，使用Listbox组件
    listbox1.place(x=510, y=0, width=140, height=300)
 
 
    listbox = ScrolledText(window)                          # 聊天信息窗口，使用ScrolledText组件制作
    listbox.place(x=5, y=0, width=500, height=300)
 
 
    # 接收服务器发来的消息并显示到聊天信息窗口上，与此同时监控用户列表更新
    def read_server(s):
        while True:
            content = s.recv(2048).decode('utf-8')                      # 接收服务器端发来的消息
            curtime = datetime.now().strftime(ISOTIMEFORMAT)            # 获取当前系统时间
            listbox.insert(tkinter.END, curtime)                        # 聊天信息窗口显示（打印）
            listbox.insert(tkinter.END, '\n'+content+'\n\n')
            listbox.see(tkinter.END)                                    # ScrolledText组件方法，自动定位到结尾，否则只有消息在涨，窗口拖动条不动
            listbox.update()                                            # 更新聊天信息窗口，显示新的信息
 
 
            # 用户列表更新，判断新的信息是否为系统消息，暂时没有想到更好的解决方案
            if content[0]=='#':
                if content[content.find(' ')+1 : content.find(' ')+3]=='进入':
                    user_list.append(content[5:content.find(' ')])
                    var1.set(user_list)
                if content[content.find(' ')+1 : content.find(' ')+3]=='离开':
                    user_list.remove(content[5:content.find(' ')])
                    var1.set(user_list)

            if content[0:4]=='endre':
                s.close()
                break
 
    t=threading.Thread(target = read_server, args = (s,))
    t.start()
 
 
    var2 = StringVar()                                      # 聊天输入口
    var2.set('')                                    
    entryInput = Entry(window, width = 140, textvariable=var2)
    entryInput.place(x=5, y=305, width = 600, height = 95)
 
 
    # 发送按钮触发的函数，即发送信息
    def sendtext():
        line = var2.get()
        s.send(line.encode('utf-8'))
        var2.set('')                                        # 发送完毕清空聊天输入口
 
    #发送按钮
    sendButton = Button(window, text = '>', font=('Fangsong', 22), bg = 'aqua',bd=3, command=sendtext)     
    sendButton.place(x=500, y=305, width = 150, height = 95)
    

    def window_destory():
        if tkinter.messagebox.askyesno("关闭确认","确认要离线吗？"):
            s.send('\exit'.encode('utf-8'))
            window.destroy()            
    window.protocol('WM_DELETE_WINDOW', window_destory)


    window.mainloop()
    
 
Login_gui_run()
