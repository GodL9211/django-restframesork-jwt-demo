#! -*-conding=: UTF-8 -*-
# 2023/2/25 9:53
"""
grpc服务端代码
"""


from concurrent import futures
import time

import grpc

import hello_pb2
import hello_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(hello_pb2_grpc.GreeterServicer):
    # 工作函数
    def SayHello(self, request, context):
        print('Hello, %s!' % request.name)
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    # 1. 实例化server gRPC 服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 2. 注册逻辑到server中
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # 3. 启动server
    server.add_insecure_port('[::]:50051')
    server.start()  # start() 不会阻塞，如果运行时你的代码没有其它的事情可做，你可能需要循环等待。
    # try:
    #     while True:
    #         time.sleep(_ONE_DAY_IN_SECONDS)
    # except KeyboardInterrupt:
    #     server.stop(0)

    server.wait_for_termination()  # 设置阻塞


if __name__ == '__main__':
    serve()
