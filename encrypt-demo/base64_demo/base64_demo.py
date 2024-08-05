#! -*-conding: UTF-8 -*-
# @公众号: 海哥python
import base64

if __name__ == '__main__':
    print(base64.b64encode('公众号： 海哥python'.encode('utf-8')))
    print(base64.b64decode(b'5YWs5LyX5Y+377yaIOa1t+WTpXB5dGhvbg==').decode('utf-8'))
