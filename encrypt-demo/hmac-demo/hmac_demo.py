#! -*-conding: UTF-8 -*-
# @公众号: 海哥python
import hashlib
import hmac


def get_hmac(str, key):
    """
    hmac加密
    :param str:
    :param key:
    :return:
    """
    h = hmac.new(key=key.encode('utf-8'), msg=str.encode('utf-8'), digestmod=hashlib.sha1)
    return h.hexdigest()


if __name__ == '__main__':
    hmac_str = get_hmac('公众号', '海哥python')
    print(hmac_str)
