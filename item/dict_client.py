"""
dict 客户端
功能：
根据用户输入，发送请求，得到结果
结构：　　一级界面－>登录    注册    退出
        二级界面－>查单词    历史记录    注销
"""
from socket import *
from getpass import getpass
import signal, sys

ADDR = ("127.0.0.1", 8000)
# 功能函数都需要套接字,定义为全局变量
sockfd = socket()
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockfd.connect(ADDR)


def do_register():
    while True:
        name = input("请输入姓名:")
        password_1 = getpass("请输入密码:")
        password_2 = getpass("请再次输入密码:")

        if (' ' in name) or (' ' in password_1):
            print("用户名和密码不能有空格")
            continue
        if password_1 != password_2:
            print("两次密码不一致,请重新输入")
            continue
        msg = "R %s %s" % (name, password_1)
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()
        if data == "Ok":
            print("注册成功")
        else:
            print("注册失败")
        return


# 登陆成功
def do_login():
    # 搭建客户端网络
    while True:
        name = input("请输入姓名:")
        password = getpass("请输入密码:")
        msg = "L %s %s" % (name, password)
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()
        if data == "Ok":
            print("登录成功")
            login(name)
        else:
            print("用户或密码输入错误,请重新输入")
        return


# 查单词
def do_query(name):
    while True:
        words = input("请输入要查询的单词")
        if words == "##":
            break
        msg = "Q %s %s" % (name, words)
        sockfd.send(msg.encode())
        # 直接发送查询结果
        data = sockfd.recv(4096).decode()
        print(data)


# 查找历史记录
def do_check_history(name):
    msg = "H %s" % name
    sockfd.send(msg.encode())
    data = sockfd.recv(128)
    if data.decode() == "Ok":
        while True:
            data = sockfd.recv(1024).decode()
            if data == "##":
                break
            else:
                print(data)
    else:
        print("没有历史记录")


def login(name):
    while True:
        print("""
                ==============Welcome==============
                 1. 查单词　　2. 历史记录　　　3. 注销
                """)
        cmd = input("输入选项:")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_check_history(name)
        elif cmd == "3":
            pass
        else:
            print("请输入正确选项")


def main():
    while True:
        print("""
        ==============Welcome================
         1. 注册　　　　　2. 登录　　　　　3. 退出
        """)
        cmd = input("输入选项:")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            sockfd.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")


if __name__ == '__main__':
    main()
