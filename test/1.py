#! -*-conding=: UTF-8 -*-
# 2024/1/19 16:46


# from dataclasses import dataclass
#
#
# @dataclass(order=True)
# class Player:
#     name: str
#     number: int
#     position: str
#
#     grade: str
#     age: int = 18  # 默认值，跟函数定义一样，需要往后放
#
#     # def __post_init__(self):
#     #     self.sort_index = self.age
#
#
# harden = Player('James Harden', 1, 'PG', 'S+', 34)
# bryant = Player(name='Kobe Bryant', number=24, position='PG', grade='S+', age=41)
#
# # 排序
# # players = [bryant, harden]
# # players_sorted = sorted(players)
# # players_sorted = sorted(players, key=lambda player: player.sort_index)
# # [Player(name='James Harden', number=1, position='PG', age=34, grade='S+'), Player(name='Kobe Bryant', number=24, position='PG', age=41, grade='S+')]
#
# print(harden.name)  # James Harden
# print(bryant.name)  # Kobe Bryant
#
# print(harden)  # Player(name='James Harden', number=1, position='PG', grade='S+', age=34)
#
# # 比较, 默认按照属性定义的顺序比较的
# print(harden < bryant)  # True
# # print(players_sorted)


# from functools import total_ordering
# from dataclasses import dataclass
#
#
# @dataclass
# class Player:
#     name: str
#     number: int
#     position: str
#     grade: str
#     age: int = 18
#
#     def __eq__(self, other):
#         return self.name == other.name  # 只比较 name
#
#     def __lt__(self, other):
#         return self.age < other.age  # 只比较 age
#
#
# # 示例使用
# harden = Player('James Harden', 1, 'PG', 'S+', 34)
# bryant = Player(name='Kobe Bryant', number=24, position='PG', grade='S+', age=41)
#
# result = harden < bryant  # 按照 age 进行比较
# print(result)  # 输出 True，因为 34 < 41
# print(harden.name)  # James Harden
# print(bryant.name)  # Kobe Bryant
# print(bryant == harden)  # False

#
# from dataclasses import dataclass, field, fields
# from typing import List
#
#
# @dataclass
# class Player:
#     name: str
#     number: int
#     position: str
#     grade: str
#     age: int = 18
#
#
# # 示例使用
# harden = Player('James Harden', 1, 'PG', 'S+', 34)
# leonard = Player(name='Kawhi Leonard', number=2, position='SF', grade='S+')
#
#
# @dataclass
# class Team:
#     name: str = field(metadata={'unit': 'name'})
#     players: List[Player] = field(default_factory=lambda: [leonard], metadata={'unit': 'players'})
#
#
# clippers = Team("clippers", [harden])
# clippers1 = Team("clippers")
# print(harden.name)
# print(leonard.name)
# print(leonard.age)
#
# print(clippers.players)
# print(clippers1.players)
#
# print(fields(clippers))
# print(fields(clippers)[1].metadata)


# import requests
# from dataclasses import dataclass
# import dataclasses
# from marshmallow import fields, EXCLUDE, validate
# import desert
#
#
# @dataclass
# class Activity:
#     activity: str
#     participants: int = dataclasses.field(metadata=desert.metadata(
#         fields.Int(required=True,
#                    validate=validate.Range(min=1, max=50,
#                                            error="Participants must be between 1 and 50 people"))
#     ))
#     price: float = dataclasses.field(metadata=desert.metadata(
#         fields.Float(required=True,
#                      validate=validate.Range(
#                          min=0, max=50,
#                          error="Price must be between $1 and $50"))
#     ))
#
#     def __post_init__(self):
#         self.price = self.price * 100
#
#
# def get_activity():
#     # resp = requests.get("https://www.boredapi.com/api/activity").json()
#     resp = {
#         "activity": "Improve your touch typing",
#         "type": "busywork",
#         "participants": 1,
#         # "price": 1.0,
#         "price": 51,
#         "link": "https://en.wikipedia.org/wiki/Touch_typing",
#         "key": "2526437",
#         "accessibility": 0.8
#     }
#     # 只提取关心的部分，未知内容选择忽略
#     schema = desert.schema(Activity, meta={"unknown": EXCLUDE})
#     return schema.load(resp)
#
#
# print(get_activity())


# import json

# from jsonpath_ng import jsonpath, parse
#
# json_data = '{"name": "John", "age": 30, "city": "New York"}'
# expression = parse('$.name')
#
# matches = [match.value for match in expression.find(json.loads(json_data))]
#
# name = matches[0] if matches else None
# print(name)


# from dataclasses import dataclass, field
#
#
# @dataclass(order=True, unsafe_hash=True)
# class Player:
#     name: str
#     number: int
#     position: str = field(hash=False)  # 不参与hash
#     grade: str
#     age: int = 18
#
#
# # 示例使用
# harden = Player('James Harden', 1, 'PG', 'S+', 34)
# harden2 = Player('James Harden', 1, 'PG', 'S+', 34)
#
# harden3 = Player('James Harden', 1, 'SG', 'S+', 34)
#
# print({harden, harden2})
# print({harden, harden3})


# from dataclasses import dataclass
#
#
# @dataclass
# class Configuration:
#     api_key: str
#     timeout: int = 30
#     max_retries: int = 5
#
#
# # 使用配置对象
# config = Configuration(api_key="my_api_key", timeout=20)
#
# # 输出对象信息
# print(config)

from dataclasses import dataclass, field


@dataclass(order=True)
class Person:
    name: str
    age: int


@dataclass(order=True)
class Player(Person):
    number: int
    position: str
    grade: str
    team: str = "nba"


# 示例使用
harden = Player(name='James Harden', age=34, number=1, position='PG', grade='S+')
bryant = Player(name='Kobe Bryant', age=41, number=24, position='PG', grade='S+')

print(harden.name)  # James Harden
print(bryant.name)  # Kobe Bryant
print(bryant.age)  # 41
print(bryant.team)  # nba

# 使用 order 参数，可以比较对象的大小（用于排序）
print(harden < bryant)  # True
