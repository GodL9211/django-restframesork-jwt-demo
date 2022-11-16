#! -*-conding=: UTF-8 -*-
# 2022/11/8 17:45
# !/usr/bin/python
"""
keepalive server
“心跳”程序的服务端（监听心跳）代码
Server端建立一个socket，然后绑定到一个（IP，port）对里，然后开启监听，准备好接收来自客户端（另一方）的请求。
其中和客户端通信的方法有send(), sendall(), accept(), recv()等
"""
import socket
import sys
import json
from threading import *

BUF_SIZE = 4096

HOST = socket.gethostname()
print(HOST)
PORT = 7870
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print("Error creating socket: %s" % e)
    sys.exit()
try:
    server.bind((HOST, PORT))
except socket.error:
    print("Bind failed!")
    sys.exit()
print("Socket bind complete")

server.listen(10)
print("Socket now listening")


def clientthread(coon):
    coon.send("Welcome to the server!".encode("utf-8"))
    while True:
        try:
            request_buffer = coon.recv(BUF_SIZE)
            # print(request_buffer[0:8])
            # print(request_buffer[-8:])
            data_loaded = json.loads(request_buffer[8: -8])
            print("ip: " + str(data_loaded['ip']) + " |status: " + data_loaded['status'] + " |pid: " + str(
                data_loaded['pid']))
            print("-" * 30)
            coon.sendall("hello, I love you!".encode("utf-8"))    # set the client :setblock(0)is ok!
        except socket.error:
            break
    coon.close()


if __name__ == '__main__':
    while True:
        coon, addr = server.accept()
        print("Connected with %s: %s " % (addr[0], str(addr[1])))
        Thread(target=clientthread, args=(coon,)).start()

    server.close()
