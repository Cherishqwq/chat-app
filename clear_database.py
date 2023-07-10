import sqlite3

# 若无该数据库，则创建Sqlite数据库并打开
# 若有，则直接打开数据库
if input()=='1':
    conn = sqlite3.connect('user.db')

    cursor = conn.cursor()# 获取该数据库的游标

    # 执行一条SQL语句，创建user表:
    cursor.execute('DROP table if exists userinfobasic')


    cursor.close()# 关闭Cursor:
    conn.commit()# 提交事务:

    # 关闭Connection:
    conn.close()
else:
    print("end.")