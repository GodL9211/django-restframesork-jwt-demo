#! -*-conding: UTF-8 -*-
# @公众号: 海哥python


import json
import requests
from functools import partial
import time
import hashlib
import subprocess

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
# import execjs


def get_time_stamp():
    return int(time.time() * 1000)


def generate_sign(target):
    md5 = hashlib.md5()
    md5.update(target.encode())
    res = md5.hexdigest()
    return res


url = "https://mhapi.yiche.com/hcar/h_car/api/v1/param/get_param_details"

uuid = "000750ef-d6d6-45d8-9ed3-8864fcb3e6ad"

timestamp = get_time_stamp()

param = {"cityId": "1501", "serialId": "7219"}

target = f'cid=508&param={json.dumps(param)}19DDD1FBDFF065D3A4DA777D2D7A81EC{timestamp}'

sign = generate_sign(target)

params = {
    "cid": "508",
    "param": json.dumps(param)
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://car.yiche.com/hongqihs5/peizhi/",
    "Cookie": "CIGUID=000750ef-d6d6-45d8-9ed3-8864fcb3e6ad; selectcity=320100; selectcityid=1501; selectcityName=%E5%8D%97%E4%BA%AC; auto_id=de6ccf16bb10303bb8ae4fc2243912ac; CIGDCID=sWtRAyHkEkcThDM7ie2xEKtbTS2GhB3m; Hm_lvt_610fee5a506c80c9e1a46aa9a2de2e44=1719905729; UserGuid=000750ef-d6d6-45d8-9ed3-8864fcb3e6ad; isWebP=true; locatecity=320100; bitauto_ipregion=58.213.147.125%3A%E6%B1%9F%E8%8B%8F%E7%9C%81%E5%8D%97%E4%BA%AC%E5%B8%82%3B1501%2C%E5%8D%97%E4%BA%AC%E5%B8%82%2Cnanjing; csids=7219_8156_5586; pageCount=3; Hm_lpvt_610fee5a506c80c9e1a46aa9a2de2e44=1719975723",
    "X-City-Id": "1501",
    "X-Ip-Address": "58.213.147.125",
    "X-Platform": "pc",
    "X-Sign": sign,
    "X-Timestamp": str(timestamp),
    "X-User-Guid": uuid
}

res = requests.get(url=url, params=params, headers=headers)
data = res.text
with open("config.json", 'w', encoding='utf-8') as f:
    f.write(data)
