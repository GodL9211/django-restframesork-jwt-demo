# ! -*-conding: UTF-8 -*-
# @公众号: 海哥python
from datetime import datetime
from typing import List, Optional
from typing_extensions import Self  # 如果python版本不低于3.11，则可以直接从typing中导入Self
from pydantic import BaseModel, ValidationError, EmailStr, field_validator, model_validator


def check_name(v: str) -> str:
    """Validator to be used throughout"""
    if not v.startswith("小"):
        raise ValueError("must be startswith 小")
    return v


class User(BaseModel):
    id: int
    name: str = "小卤蛋"
    age: int
    email: EmailStr
    signup_ts: Optional[datetime] = None
    friends: List[str] = []

    validate_fields = field_validator("name")(check_name)

    @field_validator("age")
    @classmethod
    def check_age(cls, age):
        if age < 18:
            raise ValueError("用户年龄必须大于18岁")
        return age

    @model_validator(mode="after")
    def check_age_and_name(self) -> Self:
        if self.age < 30 and self.name != "小卤蛋":
            raise ValueError("用户年龄必须小于30岁, 且名字必须为小卤蛋")

        return self


if __name__ == '__main__':
    user_data = {
        "id": 123,
        "name": "小小卤蛋",
        "age": 20,
        "email": "xiaoludan@example.com",
        'signup_ts': '2024-07-19 00:22',
        'friends': ["公众号：海哥python", '小天才', b''],
    }
    try:
        user = User(**user_data)
        print(user.model_dump())
    except ValidationError as e:
        print(f"Validation error: {e.json()}")