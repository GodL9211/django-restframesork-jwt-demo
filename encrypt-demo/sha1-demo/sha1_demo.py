#! -*-conding: UTF-8 -*-
# @公众号: 海哥python

import hashlib


def get_sha1(str):
    sha1 = hashlib.sha1()
    sha1.update(str.encode('utf-8'))
    return sha1.hexdigest()


if __name__ == '__main__':
    sha1_str = get_sha1("公众号： 海哥python")
    print(sha1_str)  # 例如：8d414091d3835990dec028e87b2dff2199fe3b77
