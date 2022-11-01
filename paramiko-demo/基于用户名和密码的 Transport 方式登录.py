#! -*-conding=: UTF-8 -*-
# 2022/11/1 11:37
"""
  基于SSHClient是传统的连接服务器、执行命令、关闭的一个操作，
  有时候需要登录上服务器执行多个操作，比如执行命令、上传/下载文件，上面方法则无法实现，可以通过如下方式来操作
"""
from conf import *

# SSHClient 封装 Transport
import paramiko

# 实例化一个transport对象
transport = paramiko.Transport((SSH_HOST, SSH_PORT))
# 建立连接
transport.connect(username=USERNAME, password=PASSWORD)
# 将sshclient的对象的transport指定为以上的transport
ssh = paramiko.SSHClient()
ssh._transport = transport
# 执行命令，和传统方法一样
stdin, stdout, stderr = ssh.exec_command('df')
print(stdout.read().decode())
# 关闭连接
transport.close()

if __name__ == '__main__':
    """
    文件系统           1K-块     已用      可用 已用% 挂载点
    udev             7961912        0   7961912    0% /dev
    tmpfs            1603452     2004   1601448    1% /run
    /dev/sda3      102626232 26911232  70455736   28% /
    tmpfs            8017240        0   8017240    0% /dev/shm
    tmpfs               5120        4      5116    1% /run/lock
    tmpfs            8017240        0   8017240    0% /sys/fs/cgroup
    /dev/sda2         996780   479560    448408   52% /boot
    /dev/sda1         523248     3412    519836    1% /boot/efi
    /dev/sda5      733394112  8802372 687263868    2% /data
    tmpfs            1603448        8   1603440    1% /run/user/114
    tmpfs            1603448        8   1603440    1% /run/user/1000
    """
    pass
