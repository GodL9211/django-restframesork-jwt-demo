#! -*-conding: UTF-8 -*-
# @公众号: 海哥python

import hashlib


def get_md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    md5_str = get_md5("公众号：海哥python")
    print(md5_str)  # 如： 0e20fe9db14a8ce7cf95b87a9f40a4c9
