import requests
from bs4 import BeautifulSoup as bs
import random
import logging,re
from time import sleep
from app import redis_client as rc
from datetime import  datetime
from app.cli.cache import cache
from app.cli.setSession import loadUserAgent,getSession

@cache("UpRank")
def getUpRank(uas: list,session:requests.session,datecode,period,classId,ajax) -> dict:
    """
    获取up主排名
    :param uas:user-agents 列表
    :return:
    """
    ua = str(random.choice(uas))
    header = {
        'User-Agent': ua,
        'Referer': "http://bz.feigua.cn/member/",
        'Origin': 'http://bz.feigua.cn',
        'Host': "bz.feigua.cn",
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': "keep-alive",
    }

    url = "http://bz.feigua.cn/rank/fans"
    upRankList = []
    data = {
        "datecode": datecode,
        "classId": classId,
        "ajax": ajax,
        "period": period
    }
    try:
        r = session.get(url, headers=header,data=data)

    except Exception as e:
        logging.warning("网站连接超时：{}".format(e))
        return False

    else:
        r.encoding = "utf-8"
        soup = bs(r.text, "html.parser")
        rows = soup.find_all(class_="list-row")
        for row in rows:
            rank = row.find(class_="index-rank").contents[0].strip() #排名
            face_url = row.find(class_="up-info__avatar").contents[1].find("img").attrs['src'] #头像图片链接
            up_name = row.find(class_="up-info__info-name").contents[1].contents[0].strip() #up主名称
            up_lv = row.find(class_="up-info__info-lv").contents[0].strip() #up主等级，称号
            up_fans = row.find_all(class_="col-item")[3].contents[0]    #up主粉丝数
            up_works = row.find_all(class_="col-item")[4].contents[0]   #作品总数
            up_get = row.find_all(class_="col-item")[5].contents[0]   #充电人数
            brand_compare_id = row.find_all(class_="col-item")[1].find(class_="up-info__avatar").contents[1].attrs['href']
            brand_compare_id = re.search("#/Blogger/Detail/(.*)",brand_compare_id).groups(1)[0]

            data = {
                'rank':rank,
                'face_url':face_url,
                'up_name':up_name,
                'up_lv':up_lv,
                'up_fans':up_fans,
                'up_get':up_get,
                'up_works':up_works,
                'brand_compare_id':brand_compare_id
            }
            upRankList.append(data)

    return {
        "UpRank":upRankList
    }

@cache("UpRiseFansRank")
def getUpRiseFansRank(uas: list,session:requests.session,datecode,period,classId,ajax) -> dict:
    """
    获取up主粉丝增长排名
    :param uas:user-agents 列表
    :return:
    """
    ua = str(random.choice(uas))
    header = {
        'User-Agent': ua,
        'Referer': "http://bz.feigua.cn/member/",
        'Origin': 'http://space.bilibili.com',
        'Host': "bz.feigua.cn",
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': "keep-alive",
    }
    url = "http://bz.feigua.cn/rank/risefans"
    upRiseFansRankList = []
    data = {
        "datecode":datecode,
        "classId":classId,
        "ajax":ajax,
        "period":period
    }
    try:
        r = session.get(url, headers=header,data=data)

    except Exception as e:
        logging.warning("网站连接超时：{}".format(e))
        return False

    else:
        r.encoding = "utf-8"
        soup = bs(r.text, "html.parser")
        rows = soup.find_all(class_="list-row")
        for row in rows:
            rank = row.find(class_="index-rank").contents[0].strip()  # 排名
            face_url = row.find(class_="up-info__avatar").contents[1].find("img").attrs['src']  # 头像图片链接
            up_name = row.find(class_="up-info__info-name").contents[1].contents[0].strip()  # up主名称
            up_lv = row.find(class_="up-info__info-lv").contents[0].strip()  # up主等级，称号
            up_risefans = row.find_all(class_="col-item")[3].contents[0] #粉丝增量
            up_fans = row.find_all(class_="col-item")[3].contents[0] #粉丝总数
            up_fans_growth_rate = row.find_all(class_="col-item")[5].contents[0] #涨粉率
            brand_compare_id = row.find_all(class_="col-item")[1].find(class_="up-info__avatar").contents[1].attrs['href']
            brand_compare_id = re.search("#/Blogger/Detail/(.*)", brand_compare_id).groups(1)[0]


            data = {
                'rank': rank,
                'face_url': face_url,
                'up_name': up_name,
                'up_lv': up_lv,
                'up_risefans':up_risefans,
                'up_fans': up_fans,
                'up_fans_growth_rate': up_fans_growth_rate,
                'brand_compare_id': brand_compare_id
            }

            upRiseFansRankList.append(data)

    return {
        "UpRiseFansRank":upRiseFansRankList
    }

@cache("UpDownFansRank")
def getUpDownFansRank(uas: list,session:requests.session,datecode,period,classId,ajax) -> dict:
    """
    获取up主掉粉排名
    :param uas:user-agents 列表
    :return:
    """
    ua = str(random.choice(uas))
    header = {
        'User-Agent': ua,
        'Referer': "http://bz.feigua.cn/member/",
        'Origin': 'http://space.bilibili.com',
        'Host': "bz.feigua.cn",
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': "keep-alive",
    }

    url = "http://bz.feigua.cn/rank/downfansRank"
    upDownFansRankList = []
    data = {
        "datecode": datecode,
        "classId": classId,
        "ajax": ajax,
        "period": period
    }
    try:
        r = session.get(url, headers=header, data=data)

    except Exception as e:
        logging.warning("网站连接超时：{}".format(e))
        return False

    else:
        r.encoding = "utf-8"
        soup = bs(r.text, "html.parser")
        rows = soup.find_all(class_="list-row")
        for row in rows:
            rank = row.find(class_="index-rank").contents[0].strip()  #排名
            face_url = row.find(class_="up-info__avatar").contents[1].find("img").attrs['src']  #头像图片链接
            up_name = row.find(class_="up-info__info-name").contents[1].contents[0].strip()  #up主名称
            up_lv = row.find(class_="up-info__info-lv").contents[0].strip()  #up主等级，称号
            up_fans = row.find_all(class_="col-item")[3].contents[0]  #粉丝总数
            up_downfans = row.find_all(class_="col-item")[4].contents[0]    #掉粉数量
            up_downrate = row.find_all(class_="col-item")[5].contents[0]    #掉粉率
            brand_compare_id = row.find_all(class_="col-item")[1].find(class_="up-info__avatar").contents[1].attrs['href']
            brand_compare_id = re.search("#/Blogger/Detail/(.*)", brand_compare_id).groups(1)[0]

            data = {
                'rank': rank,
                'face_url': face_url,
                'up_name': up_name,
                'up_lv': up_lv,
                'up_fans': up_fans,
                'up_downfans': up_downfans,
                'up_downrate': up_downrate,
                'brand_compare_id': brand_compare_id
            }

            upDownFansRankList.append(data)

    return {
        "UpDownFansRank":upDownFansRankList
    }

@cache("DailyHotVideoRank")
def getDailyHotVideoRank(uas: list,session:requests.session,datecode,period,classId,classify,ajax=None) -> dict:
    """
    获取up主掉粉排名
    :param uas:user-agents 列表
    :param datecode 时期代码
    :param period 天数代码 1 表示日榜 7 表示周榜
    :param classId 排名类型 0 新增播放 1 新增点赞 2 新增收藏 3 新增投币
    :param classify 视频分类
    :return:
    """
    ua = str(random.choice(uas))
    header = {
        'User-Agent': ua,
        'Referer': "http://bz.feigua.cn/member/",
        'Origin': 'http://space.bilibili.com',
        'Host': "bz.feigua.cn",
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': "keep-alive",
    }

    url = "http://bz.feigua.cn/ranking/DailyHotVideo/{}/{}/{}/{}.html".format(datecode,period,classId,classify)
    DailyHotVideoRankList = []
    try:
        r = session.get(url, headers=header)

    except Exception as e:
        logging.warning("网站连接超时：{}".format(e))
        return False

    else:
        r.encoding = "utf-8"
        soup = bs(r.text, "html.parser")
        rows = soup.find(class_="list-bd").find_all(class_="list-row")
        for row in rows:
            video_rank = row.find(class_="index-rank italic-order").contents[0].strip()
            video_img = row.find(class_="up-info__avatar").contents[1].find("img").attrs['src']
            video_time = row.find(class_="up-info__avatar").find(class_="time").contents[0] #视频时间长度
            video_title = row.find(class_="up-info__info-name relative").contents[1].contents[0]
            video_author = row.find(class_="info-list-name").contents[1].contents[3].contents[0]
            author_face = format(row.find(class_="info-list-name").contents[1].contents[1].attrs['src'])
            video_massege = row.find(class_="up-info__info-list relative").contents[3].contents[0] #简介
            video_class = row.find(class_="up-info__info-name relative").contents[3].contents[0] #视频类型 自制 活动 转载
            video_date = row.find(class_="info-list-name").contents[3].contents[0]  #视频发布日期
            video_rate_rise = row.find_all(class_="rank-compare-item")[1].find(class_="rise-data").contents[0]#新增播放量
            video_rate = row.find_all(class_="rank-compare-item")[1].contents[3].contents[0]#播放量
            video_like_rise = row.find_all(class_="rank-compare-item")[2].find(class_="rise-data").contents[0]#新增点赞数量
            video_like = row.find_all(class_="rank-compare-item")[2].contents[3].contents[0]#点赞数量
            video_get_rise = row.find_all(class_="rank-compare-item")[3].find(class_="rise-data").contents[0]  # 新增收藏
            video_get = row.find_all(class_="rank-compare-item")[3].contents[3].contents[0]  # 收藏数
            video_comment_rise = row.find_all(class_="rank-compare-item")[4].find(class_="rise-data").contents[0]  # 新增评论
            video_comment = row.find_all(class_="rank-compare-item")[4].contents[3].contents[0]  # 评论数
            video_coin_rise = row.find_all(class_="col-item")[7].find(class_="rise-data").contents[0]  # 新增投币
            video_coin = row.find_all(class_="col-item")[7].contents[1].contents[3].contents[0] # 硬币数

            data ={
                "video_rank":video_rank,
                "video_img":video_img,
                "video_time":video_time,
                "video_title":video_title ,
                "video_massege":video_massege,
                "video_author":video_author,
                "author_face":author_face ,
                "video_class":video_class,
                "video_date":video_date,
                "video_rate_rise":video_rate_rise,
                "video_rate":video_rate,
                "video_like_rise":video_like_rise,
                "video_like":video_like,
                "video_get_rise":video_get_rise,
                "video_get":video_get,
                "video_comment_rise":video_comment_rise,
                "video_comment":video_comment,
                "video_coin_rise":video_coin_rise,
                "video_coin":video_coin

            }

            DailyHotVideoRankList.append(data)

        return {
            "DailyHotVideoRankList":DailyHotVideoRankList
        }

# def getUpDetail(uas: list,session:requests.session,urlFix:str,dataTime:str=datetime.now().strftime("%Y-%m-%d")) -> dict:
#     ua = str(random.choice(uas))
#     header = {
#         'User-Agent': ua,
#         'Referer': "http://bz.feigua.cn/member/",
#         'Origin': 'http://space.bilibili.com',
#         'Host': "bz.feigua.cn",
#         'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
#         'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
#         'Accept': 'application/json, text/javascript, */*; q=0.01',
#         'Connection': "keep-alive",
#     }
#
#     url = "{}{}".format("http://bz.feigua.cn/Member",urlFix)
#     DailyHotVideoRankList = []
#     try:
#         r = session.get(url, headers=header)
#
#     except Exception as e:
#         logging.warning("网站连接超时：{}".format(e))
#         return False
#
#     else:
#         r.encoding = "utf-8"
#         soup = bs(r.text, "html.parser")
#         return soup


if __name__ == "__main__":
    uas = loadUserAgent("user_agents.txt")
    session = getSession(uas)
    # upRankDict = getUpRank(uas,session)
    # print(upRankDict)
    # upRiseFansRankDict = getUpRiseFansRank(uas,session)
    # print(upRiseFansRankDict)
    # upDownFansRankDict = getUpDownFansRank(uas,session)
    # print(upDownFansRankDict)
    # hotVideoRankList = getDailyHotVideoRank(uas,session)
    # print(hotVideoRankList)
    l = getDailyHotVideoRank(uas,session,20210404,1,0,1)


