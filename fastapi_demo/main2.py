#! -*-conding: UTF-8 -*-
# @公众号: 海哥python
"""
路由测试
"""

from fastapi import FastAPI
from fastapi.routing import APIRoute


def app_hello():
    return {"msg": "hello world"}


routes = [
    APIRoute(path="/", methods=["GET"], endpoint=app_hello)
]

app = FastAPI(title="学习", version="1.0.0", description="学习", routes=routes)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main2:app", host="127.0.0.1", port=8000, reload=True)

    """
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
