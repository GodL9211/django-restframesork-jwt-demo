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


@app.on_event("startup")
async def startup_event():
    print("启动事件")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"msg": "服务器错误"}, headers=exc.headers)


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


@app.get("/hello/{user_id}/article/{article_id}")
def app_hello2(user_id: int = Path(..., ge=1, le=100), article_id: int = Path(..., ge=1, le=100)):
    return {"msg": f"hello {user_id} {article_id}"}


def read_in_chunks():
    video_path = "./a05bebe89f4e6ce502ca5c3dcf68c440.mp4"
    cap = cv2.VideoCapture(video_path)
    suc = cap.isOpened()
    while suc:
        suc, frame = cap.read()
        if suc:
            ret, jpeg = cv2.imencode('.jpg', frame)
            cv2.waitKey(1)
            yield jpeg.tobytes()
        else:
            break
        cap.release()


@app.get("/stream_video")
def open_cv():
    return StreamingResponse(read_in_chunks(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/dow_video")
def download_video():
    return FileResponse("./a05bebe89f4e6ce502ca5c3dcf68c440.mp4", filename="11.mp4")


@app.get("/http_exception")
async def http_exception():
    raise HTTPException(status_code=500, detail="服务器错误")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main3:app", host="127.0.0.1", port=8001, reload=True)

    """
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
