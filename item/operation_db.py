"""
提供服务端的所有数据库操作
"""
import pymysql
import hashlib

SALT = "#&AID"  # 盐


class Database:
    def __init__(self, database, host="localhost",
                 port=3306,
                 user="root",
                 password="123456",
                 charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.database = database
        self.connect_db()  # 连接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.password,
                                  database=self.database,
                                  charset=self.charset
                                  )

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 注册操作
    def register(self, name, passwd):
        sql = "select * from user where username='%s'" % name
        self.cur.execute(sql)
        # 若有结果说明有name
        r = self.cur.fetchone()
        if r:
            return False
        # 密码加密处理
        hash = hashlib.md5((passwd + SALT).encode())
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        sql = "insert into user (username,password) values(%s,%s)"
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self, name, passwd):
        hash = hashlib.md5((passwd + SALT).encode())
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        sql = "select * from user where username=%s and password=%s"
        self.cur.execute(sql, [name, passwd])
        r = self.cur.fetchone()
        print(r)
        if r:
            return True
        else:
            return False

    def check＿word(self, word):
        sql = "select mean from words where word='%s'" % (word)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    def insert_history(self, name, word):
        sql = "insert into hist (username,word) values(%s,%s)"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def history(self, name):
        sql = "select username,word,time from hist" \
              " where username='%s'" \
              " order by time desc limit 10" % (name)
        self.cur.execute(sql)
        return self.cur.fetchall()

    # 关闭数据库
    def close(self):
        self.db.close()
