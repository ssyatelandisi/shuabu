from hashlib import md5
from datetime import datetime as dt
from timeit import timeit
from urllib import parse, request
import os, base64, random, json

# key = md5(encode(`${params.phone}1${params.password}2${params.step}xjdsb${params.time}`))

GETURL = "http://api.muvip.cn/api/xiaomi/api.php?account={}&password={}&steps={}"


class Params:
    def __init__(self, phone="", password="", step="", p_time=None, **keyargs):
        self.phone = phone
        self.password = password
        self.step = step
        self.time = p_time if p_time else str(int(dt.timestamp(dt.now())))
        self.key = md5(
            base64.b64encode(
                f"{self.phone}1{self.password}2{self.step}xjdsb{self.time}".encode()
            )
        ).hexdigest()


def fetch(user: str, password: str, step: str):
    ip = f"119.120.{random.randint(1,255)}.{random.randint(1,255)}"
    req = request.Request(
        url=GETURL.format(user, password, step),
        # data=parse.urlencode(params.__dict__).encode("utf-8"),
        headers={
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,ko;q=0.5,zh-TW;q=0.4,und;q=0.3,ru;q=0.2",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "referer": "http://api.muvip.cn/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "x-forwarded-for": ip,
            "X-Remote-IP": ip,
            "X-Real-IP": ip,
            "X-Originating-IP": ip,
        },
        method="GET",
    )
    try:
        res = request.urlopen(req, timeout=10.0).read()
    except:
        print(f"请求超时 {user}")
        return False
    else:
        if str(json.loads(res.decode("utf-8")).get("code")) == "1":
            return True
        else:
            print(json.loads(res.decode("utf-8")))
            return False


def shuabu():
    """
    [
        {
            "phone": "usr1",
            "password": "psd1"
        },
        {
            "phone": "usr2",
            "password": "psd2"
        }
    ]
    """
    if not os.environ.get("DATA"):
        print("不存在环境变量DATA")
        return None
    try:
        data = json.loads(os.environ.get("DATA"))
    except Exception as e:
        print(e)
        return None
    step = str(random.randint(18000, 22000))
    for item in data:
        times = 0
        while times <= 5 and not item.get("result", False):  # times失败次数
            result = fetch(item["phone"], item["password"], step)
            if result:
                item["result"] = True
                print(f'{item["phone"]} {step}  sucess')
                break
            else:
                times += 1
                print(f'{item["phone"]} {step}  fail')


if __name__ == "__main__":
    print(
        f'耗时 {timeit(stmt="shuabu()", setup="from __main__ import shuabu", number=1)}\n'
    )
