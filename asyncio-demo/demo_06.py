#! -*-conding: UTF-8 -*-
# @公众号: 海哥python


import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

# 选择事件循环
selector: DefaultSelector = DefaultSelector()
# 用于判断是否有事件在运行
running_cnt: int = 0


def request(host: str) -> None:
    """模拟请求并打印响应体"""
    # 告诉主函数， 自己的事件还在运行
    global running_cnt
    running_cnt += 1

    # 初始化socket
    url: str = f"http://{host}"
    sock: socket.SocketType = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect((host, 80))
    except BlockingIOError:
        pass

    response_bytes: bytes = b""

    def read_response() -> None:
        """接收响应参数， 并判断请求是否结束"""
        nonlocal response_bytes
        chunk: bytes = sock.recv(4096)
        print(f"recv {host} body success")
        if chunk:
            response_bytes += chunk
        else:
            # 没有数据代表请求结束了， 注销监听
            selector.unregister(sock.fileno())
            global running_cnt
            running_cnt -= 1

    def connected() -> None:
        """socket建立连接时的回调"""
        # 取消监听
        selector.unregister(sock.fileno())
        print(f"{host} connect success")
        # 发送请求， 并监听读事件， 以及注册对应的接收响应函数
        sock.send(f"GET {url} HTTP/1.0\r\nHost: {host}\r\n\r\n".encode("ascii"))
        selector.register(sock.fileno(), EVENT_READ, read_response)

    selector.register(sock.fileno(), EVENT_WRITE, connected)


if __name__ == "__main__":
    # 同时多个请求
    request("so1n.me")
    request("github.com")
    request("google.com")
    request("baidu.com")
    # 监听是否有事件在运行
    while running_cnt > 0:
        # 等待事件循环通知事件是否已经完成
        for key, mask in selector.select():
            key.data()
