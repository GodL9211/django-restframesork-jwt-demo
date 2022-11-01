#! -*-conding=: UTF-8 -*-
# 2022/11/1 14:03
import os

import paramiko

from conf import *

private_key = paramiko.RSAKey.from_private_key_file(get_private_key_file())
transport = paramiko.Transport((SSH_HOST, SSH_PORT))
transport.connect(username=USERNAME, password=PASSWORD)
sftp = paramiko.SFTPClient.from_transport(transport)

# conf_tmp.py 上传至服务器 /tmp/conf_tmp.py
sftp.put('conf_tmp.py', '/tmp/conf_tmp.py')
# 将LinuxFile.txt 下载到本地 fromlinux.txt文件中
sftp.get('/tmp/conf_tmp.py', os.getcwd() + "/conf_tmp2.py")
transport.close()


if __name__ == '__main__':
    pass
