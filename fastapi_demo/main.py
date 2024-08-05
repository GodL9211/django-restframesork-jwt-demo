#! -*-conding: UTF-8 -*-
# @公众号: 海哥python

from fastapi import FastAPI, APIRouter

app = FastAPI(title="学习", version="1.0.0", description="学习")


@app.get("/hello", tags=["hello"])
def app_hello():
    return {"msg": "hello world"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

    """
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
