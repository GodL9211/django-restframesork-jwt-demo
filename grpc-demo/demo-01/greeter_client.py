#! -*-conding=: UTF-8 -*-
# 2023/2/25 9:54
"""
grpc客户端代码
"""


from __future__ import print_function

import grpc

import hello_pb2
import hello_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = hello_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(hello_pb2.HelloRequest(name='goodspeed2'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
