#! -*-conding: UTF-8 -*-
# @公众号: 海哥python
"""
路径参数校验
"""
from os import getcwd, path
from enum import Enum

from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
import cv2

app = FastAPI(title="学习", version="1.0.0", description="学习")


class EnumDemo(str, Enum):
    """
    枚举类
    """
    A = "A"
    B = "B"
    C = "C"


@app.get("/hello/{enum}")
def app_hello(enum: EnumDemo):
    return {"msg": f"hello {enum.value}"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main3:app", host="127.0.0.1", port=8001, reload=True)

    """
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
