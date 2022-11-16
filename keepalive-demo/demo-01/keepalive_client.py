#! -*-conding=: UTF-8 -*-
# 2022/11/8 17:53
"""
心跳发起端代码
Client端建立socket，进行对服务器的连接，（可选的设置阻塞（同异步）方式等），连接上服务器后，进行数据的交互，sendall(), recv()等。
自定义请求报文
"""
import os
import socket
import sys
import time
import json

host = socket.gethostname()  # maybe change
port = 7870
BUF_SIZE = 4096


try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print("Error creating socket: %s" % e)
    sys.exit()

try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print("Hostname couldn't be resolved. Exciting")

    sys.exit()

try:
    client.connect((remote_ip, port))
    client.setblocking(False)  # set the socket is not blocking
    print("Socket connected to %s on ip %s" % (host, remote_ip))
except socket.gaierror as e:  # address related error
    print("connected to server error%s" % e)
    sys.exit()


# beat_count = 0

def send_heart_beat():
    """
    发送心跳
    """
    while True:
        # beat_count += 1 #heart_beat time

        host_name = socket.gethostname()
        # data_to_server = "ip: "+str(socket.gethostbyname(host_name))+",    stats: alive,   "+"pid: "+str(os.getpid())
        data_to_server = {'ip': socket.gethostbyname(host_name), 'status': 'alive', 'pid': os.getpid()}
        data_dumped = '<?begn?>' + json.dumps(data_to_server, ensure_ascii=False) + '<?endn?>'
        try:
            client.sendall(data_dumped.encode("utf-8"))
            print('I - ', os.getpid(), '- am alive.')
        except socket.error:
            print("Send failed!!")
            sys.exit()

        time.sleep(1)
    client.close()


if __name__ == '__main__':
    send_heart_beat()
