#! -*-conding=: UTF-8 -*-
# 2022/11/1 11:37
from pathlib import Path

SSH_HOST = "192.168.8.109"
SSH_PORT = 22
USERNAME = "sj"
PASSWORD = "admin123"

current_path = Path.cwd()


def get_private_key_file():
    private_key_file_path = current_path / 'id_rsa'
    print("密钥目录为:%s" % private_key_file_path)
    return str(private_key_file_path)


if __name__ == '__main__':
    pass
