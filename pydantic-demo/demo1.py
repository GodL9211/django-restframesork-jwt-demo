#! -*-conding: UTF-8 -*-
# @公众号: 海哥python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError, EmailStr, computed_field
from loguru import logger


class User(BaseModel):
    id: int
    name: str = "小卤蛋"
    age: int
    email: EmailStr
    signup_ts: Optional[datetime] = None
    friends: List[str] = []

    @computed_field  # 计算属性
    @property
    def link(self) -> str:
        return f"尼古拉斯 · {self.name}"


if __name__ == '__main__':

    # logger.info(User.model_json_schema())

    user_data = {
        "id": 123,
        "name": "小卤蛋",
        "age": 20,
        "email": "xiaoludan@example.com",
        'signup_ts': '2024-07-19 00:22',
        'friends': ["公众号：海哥python", '小天才', b''],
    }
    #
    try:
        user = User(**user_data)
        logger.info(f"{user.model_dump()} .... type: {type(user.model_dump())}")
    except ValidationError as e:
        logger.error(f"Validation error: {e.json()}")
