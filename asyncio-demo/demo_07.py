#! -*-conding: UTF-8 -*-
# @公众号: 海哥python
import asyncio
from typing import Any, Optional, List, Callable


class Status:
    """用于判断Future状态"""
    pending: int = 1
    finished: int = 2
    cancelled: int = 3


class Future(object):

    def __init__(self) -> None:
        """初始化时， Feature处理pending状态， 等待set result"""
        self.status: int = Status.pending
        self._result: Any = None
        self._exception: Optional[Exception] = None
        self._callbacks: List[Callable[['Future'], None]] = []

    def add_done_callback(self, fn: [['Future'], None]) -> None:
        """添加完成时的回调"""
        self._callbacks.append(fn)

    def cancel(self):
        """取消当前的Feature"""
        if self.status != Status.pending:
            return False
        self.status = Status.cancelled
        for fn in self._callbacks:
            fn(self)
        return True

    def set_exception(self, exc: Exception) -> None:
        """设置异常"""
        if self.status != Status.pending:
            raise RuntimeError("Can not set exc")
        self._exception = exc
        self.status = Status.finished

    def set_result(self, result: Any) -> None:
        """设置结果"""
        if self.status != Status.pending:
            raise RuntimeError("Can not set result")
        self.status = Status.finished
        self._result = result
        for fn in self._callbacks:
            fn(self)

    def result(self):
        """获取结果"""
        if self.status == Status.cancelled:
            raise asyncio.CancelledError
        elif self.status != Status.finished:
            raise RuntimeError("Result is not read")
        elif self._exception is not None:
            raise self._exception
        return self._result

    def __iter__(self):
        """通过生成器来模拟协程， 当收到结果通知时， 会返回结果"""
        if self.status == Status.pending:
            yield self
        return self.result()
