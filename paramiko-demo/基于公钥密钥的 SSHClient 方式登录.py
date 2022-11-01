#! -*-conding=: UTF-8 -*-
# 2022/11/1 11:46


import paramiko

from conf import *


private_key = paramiko.RSAKey.from_private_key_file(get_private_key_file())
# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname=SSH_HOST, port=SSH_PORT, username=USERNAME, pkey=private_key)
# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
# 获取命令结果
res, err = stdout.read(), stderr.read()
result = res if res else err
print(result.decode())
# 关闭连接
ssh.close()

if __name__ == '__main__':
    """
    /mnt/f/study/paramiko-demo/id_rsa
    新目录为:/mnt/f/study/paramiko-demo/id_rsa
    文件系统           1K-块     已用      可用 已用% 挂载点
    udev             7961912        0   7961912    0% /dev
    tmpfs            1603452     2004   1601448    1% /run
    /dev/sda3      102626232 26911156  70455812   28% /
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
