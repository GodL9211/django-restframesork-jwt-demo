#! -*-conding=: UTF-8 -*-
# 2022/11/1 13:52
import os
import paramiko
from conf import *

# 实例化一个trans对象# 实例化一个transport对象
transport = paramiko.Transport((SSH_HOST, SSH_PORT))
# 建立连接
transport.connect(username=USERNAME, password=PASSWORD)
# 实例化一个 sftp对象,指定连接的通道
sftp = paramiko.SFTPClient.from_transport(transport)

# conf_tmp.py 上传至服务器 /tmp/conf_tmp.py
sftp.put('conf_tmp.py', '/tmp/conf_tmp.py')
# 将LinuxFile.txt 下载到本地 fromlinux.txt文件中
sftp.get('/tmp/conf_tmp.py', os.getcwd() + "/conf_tmp2.py")
transport.close()

if __name__ == '__main__':
    pass
