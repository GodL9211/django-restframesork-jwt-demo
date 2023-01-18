#! -*-conding=: UTF-8 -*-
# 2023/1/18 10:50
import paramiko
import sys
import subprocess

#
# we instantiate a new object referencing paramiko's SSHClient class
#
vm = paramiko.SSHClient()
vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
password = input("input passwd: ")
print(1111111111111)
vm.connect('127.0.0.1', port=10022, username='lianhaifeng', password=password)
#
vmtransport = vm.get_transport()
dest_addr = ('192.168.18.132', 22)  # edited#
local_addr = ('127.0.0.1', 10022)  # edited#
vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)

jhost = paramiko.SSHClient()
jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# jhost.load_host_keys('/home/osmanl/.ssh/known_hosts') #disabled#
jhost.connect('192.168.18.132', username='lianhaifeng', password=password, sock=vmchannel)

stdin, stdout, stderr = jhost.exec_command("ls /opt")  # edited#

print(stdout.read().decode())  # edited#

jhost.close()
vm.close()

