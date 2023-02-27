#! -*-conding=: UTF-8 -*-
# 2023/2/25 9:54
"""
grpc客户端代码, 使用with, 调用grpc的go服务端(另一个go仓中实现)
"""


from __future__ import print_function

import grpc

import hello_pb2
import hello_pb2_grpc


def run():
    with grpc.insecure_channel("127.0.0.1:8972") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name="haifeng"))
        print("Greeter client received: " + response.reply)


if __name__ == '__main__':
    run()

    """
    python3 greeter_client2.py
    greeter client received: Hello haifeng
    """