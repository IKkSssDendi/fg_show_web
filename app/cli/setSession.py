import requests
import random
from time import sleep


def getSession(uas: list) -> requests.session:
    ua = str(random.choice(uas))
    index_url = 'http://bz.feigua.cn/'
    login_url = "http://bz.feigua.cn/login"
    header = {
        'User-Agent': ua,
        'Referer': "http://bz.feigua.cn/login",
        'Origin': "http://bz.feigua.cn",
        'Host': "bz.feigua.cn",
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': "keep-alive",
    }

    s = requests.session()

    data = {
        "tel":"",
        "password":""
    }

    s.get(index_url)
    sleep(1)
    s.post(login_url,headers=header,data=data)

    return s

def loadUserAgent(uaFileName: str) -> list:
    """
    传入user-agents.txt 返回user-agent list
    :param uaFileName:
    :return:
    """
    uas = []
    with open(uaFileName, "rb") as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
        random.shuffle(uas)
    return uas