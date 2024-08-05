#! -*-conding: UTF-8 -*-
# @公众号: 海哥python
from functools import wraps

from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError

app = Flask(__name__)


# 创建一个 Pydantic 模型来表示请求体中的数据
class User(BaseModel):
    model_config = {"extra": "forbid"}  # 不允许额外字段
    id: int
    name: str
    email: str


def validate_request_body(model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                body = model.model_validate(request.json)
                return func(body, *args, **kwargs)
            except ValidationError as e:
                return jsonify({"error": e.errors()}), 400

        return wrapper

    return decorator


@app.route('/users', methods=['POST'])
@validate_request_body(User)
def create_user2(user: User):
    # 在这里可以处理用户数据，例如保存到数据库
    # ...
    print(user.model_dump())

    # 返回成功响应
    return jsonify({"message": "User created successfully", "user": user.dict()}), 201


if __name__ == '__main__':
    app.run(debug=True)
