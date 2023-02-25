#! -*-conding=: UTF-8 -*-
# 2023/2/25 9:54
"""
protobuf 序列化与反序列化
"""


from __future__ import print_function


import hello_pb2


def run():
    request = hello_pb2.HelloRequest(name='goodspeed2')
    res_str = request.SerializeToString()
    print(res_str)
    print(len(res_str))  # 这里可以看出protobuf压缩比是比json高

    # 字符串反向生成对象
    request2 = hello_pb2.HelloRequest()
    request2.ParseFromString(res_str)
    print(request2)


if __name__ == '__main__':
    run()
