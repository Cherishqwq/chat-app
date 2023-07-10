#账户与密码


import hashlib
import sqlite3

dbname='user.db'

class newuser:
    #！id系统（参考wx
    #没有去重
    def __init__(self,database_name, name, password, info): #变量传入为bytes格式 encodeutf8不好使
        self.database=dbname
        self.name=str(name)
        self.password=password
        self.info=str(info)
        self.add_user()
          
    def saveuser(self):
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO userinfobasic(Name,keyh, info) VALUES ('{self.name}', '{self.passwordhash}', '{self.info}')")
        cursor.close() # 关闭Cursor:
        conn.commit()# 提交事务:
        conn.close()# 关闭Connection:

    #添加到文件中
    def add_user(self): #str putin
        self.passwordhash = self.adduser_encode() 
        ###
        self.saveuser()

    #创建
    def adduser_encode(self): 
        password_hash = hashlib.md5(self.password.encode())
        password_hash=password_hash.hexdigest() #hexdigest是十六进制数据字符串值
        return password_hash
    

#验证
class vertify:
    def __init__(self,username,password):
        self.username = str(username)
        self.password=hashlib.md5(str(password).encode()).hexdigest()

        
    def vertify_user(self): 
        conn = sqlite3.connect(dbname)
        cursor= conn.cursor() 
        try:
            cursor.execute("select * from userinfobasic WHERE Name = '%s' "%(self.username))              
            person = cursor.fetchone()# 抓住一条数据

            if person==None:
                #print('查询失败')
                flag= -1
            else:
                if person[1] == self.password:
                    flag=1
                else:
                    flag=0
        except Exception as e:
            print(e)#打印异常信息
            flag= -1
        finally:
            conn.commit()
            conn.close()# 关闭Connection:
            return flag

            


class delete:
    def __init__(self,username,password):
        self.username = str(username)
        self.password=password
      
        
    def delete_user(self): 
        check=vertify(self.username,self.password)
        flag=check.vertify_user()
        conn = sqlite3.connect(dbname)
        if flag:
            cursor= conn.cursor() 
            cursor.execute("DELETE FROM userinfobasic WHERE Name = '%s' "%(self.username))  
            ans= "completed." 
        else:
            ans= "application rejected."

        conn.commit()
        conn.close()# 关闭Connection:
        return ans

        
    

class edit:
    def __init__(self):
        pass
    def x(self):
        conn = sqlite3.connect(dbname)
        cursor= conn.cursor() 
        cursor.execute('UPDATE userinfobasic SET name = "Rogers" where id = 2') 
        conn.commit()
        conn.close()# 关闭Connection:




'''
import bcrypt
import hashlib
import json
import sqlite3

dbname='user.db'

def saveuser(database_name, name, keyh, info):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO userinfobasic(Name,keyh, info) VALUES ('{name}', '{keyh}', '{info}')")
    cursor.close() # 关闭Cursor:
    conn.commit()# 提交事务:
    conn.close()# 关闭Connection:

#创建
def newuser_encode(username, password): 
    # 把账号名和密码转换成字节串 
    username_bytes = username.encode("utf-8")
    password_bytes = password.encode("utf-8") 
    # 对账号名和密码进行哈希处理，并返回字节串 
    #username_hash = bcrypt.hashpw(username_bytes, bcrypt.gensalt()) 
    username_hash=username
    password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()) 
    # 返回哈希后的账号名和密码 
    return username_hash, password_hash
#！没有查重

#验证
def verify_user(username, password): 
    # 把账号名和密码转换成字节串 
    username_bytes = username.encode("utf-8") 
    password_bytes = password.encode("utf-8") 
    # 从文件中读取json数据，并转换成字典 
    with open("users.json", "r") as f: 
        users = json.load(f) 
        # 判断账号名是否存在于字典中 
        if username_bytes not in users: 
            return False 
            # 获取字典中对应的哈希值，并转换成字节串 
        username_hash = users[username_bytes].encode("utf-8") 
        password_hash = users[password_hash].encode("utf-8") 
        # 对比账号名和密码是否与哈希值匹配，并返回布尔值 
        return bcrypt.checkpw(username_bytes, username_hash) and bcrypt.checkpw(password_bytes, password_hash)

#添加到文件中
def add_user(username, password,inf): #str putin
    # 调用创建用户的函数，获取哈希后的账号名和密码 
    username_hash, password_hash = newuser_encode(username, password) 
    # 从文件中读取json数据，并转换成字典 
    with open("users.json", "r") as f: 
        users = json.load(f) # 把哈希后的账号名和密码添加到字典中 新json文件空，非字典格式会报错
        u=username_hash#.decode("utf-8")#u=int.from_bytes(username_hash, 'big')
        print(u)
        #users[username_hash] = password_hash 
    #print(users)
    # 把字典转换成json数据，并写入到文件中 
    with open("users.json", "w") as f: 
        json.dump(users, f)#字典-str-json
    print(str(password_hash))
    saveuser(database_name=dbname,name=username,keyh=password,info=inf)


#删除已有用户从文件中
def delete_user(username, password): 
    # 调用验证用户的函数，判断账号名和密码是否正确 
    if not verify_user(username, password): 
        return False 
    # 把账号名转换成字节串 
    username_bytes = username.encode("utf-8") 
    # 从文件中读取json数据，并转换成字典 
    with open("users.json", "r") as f: 
        users = json.load(f) 
        # 判断账号名是否存在于字典中 
        if username_bytes not in users: 
            return False 
        # 从字典中删除对应的键值对 
        del users[username_bytes] 
        # 把字典转换成json数据，并写入到文件中 
        with open("users.json", "w") as f: 
            json.dump(users, f) # 返回成功的标志 
        return True
    
add_user(username='TERMINAL',password='123',inf='adm')
'''