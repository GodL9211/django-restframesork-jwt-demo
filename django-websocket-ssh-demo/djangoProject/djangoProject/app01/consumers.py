#! -*-conding=: UTF-8 -*-
# 2023/5/4 14:43

import json
import paramiko
from threading import Thread

from channels.generic.websocket import WebsocketConsumer


class SSHConsumer(WebsocketConsumer):
    def connect(self):
        print("--------hello--------------")
        print(self.scope)
        query_params = self.scope['url_route']['kwargs']
        host = query_params['host']
        username = query_params['username']
        password = query_params['password']

        self.accept()
        # paramiko 建立连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=host, port=22, username=username, password=password, timeout=8)
        except Exception as e:
            message = json.dumps({'flag': 'error', 'message': str(e)})
            self.send(message)
            return False

        # 打开一个ssh通道并建立连接
        transport = ssh.get_transport()
        self.ssh_channel = transport.open_session()
        self.ssh_channel.get_pty(term='xterm')
        self.ssh_channel.invoke_shell()
        recv = self.ssh_channel.recv(1024).decode('utf-8')
        message = json.dumps({'flag': 'success', 'message': recv})
        self.send(message)

    def disconnect(self, close_code):
        self.ssh.close()

    def receive(self, text_data=None):
        text_data = json.loads(text_data)
        # run_shell(data=text_data.get('data', ''))
        # 向远程服务器发送命令
        print(text_data.get('data', ''))
        Thread(target=self.ssh_channel.send,args=[text_data.get('data', '')]).start()
        # self.ssh_channel.send(text_data.get('data', ''))
        def recv_from_host():
            # 从远程服务器接收命令，返回给前端
            while not self.ssh_channel.exit_status_ready():
                data = self.ssh_channel.recv(1024).decode('utf-8', 'ignore')
                if len(data) != 0:
                    message = {'flag': 'success', 'message': data}
                    self.send(json.dumps(message))
                else:
                    break

        Thread(target=recv_from_host).start()
