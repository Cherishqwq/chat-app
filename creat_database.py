import sqlite3



# 若无该数据库，则创建Sqlite数据库并打开
# 若有，则直接打开数据库
conn = sqlite3.connect('user.db')
# 获取该数据库的游标
cursor = conn.cursor()

# 执行一条SQL语句，创建user表:
cursor.execute('CREATE TABLE userinfobasic(Name TEXT, keyh TEXT, Info TEXT, INFOx TEXT, Details1 TEXT,Details2 TEXT,Details3 TEXT,Details4 TEXT,Details5 TEXT,Details6 TEXT, Details7 TEXT,  Details8 TEXT,Details9 TEXT,Details10 TEXT)')


# 关闭Cursor:
cursor.close()

# 提交事务:
conn.commit()

# 关闭Connection:
conn.close()