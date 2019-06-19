from socket import *
from multiprocessing import Process
from item.operation_db import *
import signal, sys
from time import sleep

HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)
db = Database('dict')


def do_register(c, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name, passwd):
        c.send(b"Ok")
    else:
        c.send(b"Fail")


def do_login(c, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name, passwd):
        c.send(b"Ok")
    else:
        c.send(b"Fail")


# 查单词
def do_query(c, data):
    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]
    mean = db.check＿word(word)
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        msg = "%s:%s" % (word, mean)
        c.send(msg.encode())
        # 插入记录
        db.insert_history(name, word)


# 查找历史记录
def do_check_hist(c, data):
    name = data.split(" ")[1]
    r = db.history(name)
    if not r:
        c.send(b"Fail")
    else:
        c.send(b"Ok")
    for i in r:
        msg = "%s   %-16s   %s" % i
        sleep(0.1)
        c.send(msg.encode())
    sleep(0.1)
    c.send(b"##")


# 接收客户端请求
def request(c):
    # 生成游标
    db.create_cursor()
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), "发送消息:", data)
        # 判断请求类型
        if not data or data[0] == "E":
            sys.exit()
        elif data[0] == "R":  # 1
            do_register(c, data)
        elif data[0] == "L":
            do_login(c, data)
        elif data[0] == "Q":
            do_query(c, data)
        elif data[0] == "H":
            do_check_hist(c, data)


# 搭建网络
def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(3)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # 循环接收客户端连接
    while True:
        try:
            confd, addr = sockfd.accept()
            print("有客户端连接", addr)
        except KeyboardInterrupt:
            sockfd.close()
            db.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue
        p = Process(target=request, args=(confd,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
