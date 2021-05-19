import requests
from bs4 import BeautifulSoup as bs
import random
import logging,re,ast
from app.cli.setSession import loadUserAgent,getSession
from app.cli.cache import detailCache
from bs4.element import NavigableString

@detailCache()
def getUpDetail(uas: list,session:requests.session,uid):
    """
    缓存key uid + datetime
    up_face up头像
    up_name 名称
    up_url up主 主页
    classic 分类
    sex 性别
    lv等级
    member会员
    intru简介
    tags 标签
    fans_num 粉丝数
    vedio_num 视频数
    pay_num 充电总数
    hdl 互动率
    zfb 转粉比
    bfb 播放比
    fsb_1 点赞粉丝比
    fsb_2 收藏粉丝比
    fsb_3评论粉丝比
    fsb_4转发粉丝比
    fsb_5弹幕粉丝比
    fsb_6投币粉丝比
    bf 播放总数
    dz 点赞总数
    sc 收藏总数
    pl 评论总数
    dm 弹幕总数
    fx 分享总数
    tb 投币总数
    :param uas:
    :param session:
    :param uid:
    :return:
    """
    url = "http://bz.feigua.cn/Blogger/Detail/{}".format(uid)
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

    try:
        r = session.get(url)
    except Exception as e:
        logging.warning("网站连接超时：{}".format(e))
        return False
    else:
        r.encoding = "utf-8"
        soup = bs(r.text, "html.parser")
        up_face = soup.find(class_="flex-column-col1").find(class_="up-info__avatar").contents[1].attrs["src"]
        up_name = soup.find(class_="flex-column-col1").find(class_="up-info__info-name").contents[1].text.strip()
        up_url = soup.find(class_="flex-column-col1").find(class_="up-info__info-name").contents[1].attrs['href']
        classic = soup.find(class_="flex-column-col1").find(class_="up-info__info3 clearfix").contents[1].contents[1].contents[0].strip()
        sex = soup.find(class_="flex-column-col1").find(class_="up-info__info3 clearfix").contents[3].contents[1].contents[0].strip()
        lv = soup.find(class_="flex-column-col1").find(class_="up-info__info3 clearfix").contents[5].contents[1].contents[0].strip()
        member = soup.find(class_="flex-column-col1").find(class_="up-info__info3 clearfix").contents[7].contents[1].contents[0].strip()
        intru_list = soup.find(class_="flex-column-col1").find(class_="more-data").find(class_="up-info__info2").find_all("p")
        intru = {}
        for content in intru_list:
            if len(content) == 2:
                key = content.contents[0].contents[0].strip()
                intru[key] = content.contents[1].strip()
            else:
                key = content.contents[1].contents[0].strip()
                intru[key] = content.contents[2].strip()
        try:
            tags = ast.literal_eval(re.search("var tags = (.*);",str(soup)).groups(1)[0].strip())
        except:
            tags = None
        print(tags)
        sj_1_list = soup.find(class_="flex-column-col2").find(class_="updetail__info-data-box").find(class_="el-row el-row--flex").find_all(class_="el-col el-col-6")[1:]
        sj_1 = {}
        for content in sj_1_list:
            key = content.contents[0].strip()
            sj_1[key] = content.contents[2].contents[0].strip()
        sj_2_list = soup.find(class_="flex-column-col2").find(class_="video-data").find_all(class_="el-row el-row--flex")
        sj_2 = {}
        for content in sj_2_list:
            s = content.find_all(class_="el-col el-col-6")
            for content_data in s :
                key = content_data.contents[0].strip()
                try:
                    sj_2[key] = content_data.contents[3].contents[0].strip()
                except:
                    sj_2[key] = content_data.contents[2].contents[0].strip()
        sj_3_list = soup.find(class_="flex-column-col2").find(class_="updetail__info-data").find_all(class_="el-row el-row--flex")
        sj_3 = {}
        for content in sj_3_list:
            s = content.find_all(class_="el-col el-col-6")[1:]
            for content_data in s:
                key = content_data.contents[0].strip()
                sj_3[key] = content_data.contents[2].contents[0].strip()
        sj_4_list = soup.find(class_="new-data-block").find_all(class_="data-block")
        sj_4 = {}
        for content in sj_4_list:
            s = content.find_all(class_="data-block-item")
            for item in s:
                key = item.contents[0].strip()
                if len(item.contents) > 3:
                    sj_4[key] = item.contents[4].strip()
                else :
                    sj_4[key] = item.contents[2].strip()
        sj_5_list = soup.find(class_="main-right").find(class_="new-data-block").find_all(class_="data-block-item")
        sj_5 = {}
        for content_data in sj_5_list:
            key = content_data.contents[0].strip()
            print(key)
            try:
                if re.search("\-",str(content_data.contents[1].contents[3].contents[0])):
                    t = "-1"
                else:
                    t = "1"
            except:
                if re.search("\-", str(content_data.contents[3].contents[3].contents[0])):
                    t = "-1"
                else:
                    t = "1"
            if key == '新增收藏':
                sj_5[key] = {
                    "now": str(content_data.contents[3].contents[1].contents[0]).strip(),
                    "before": str(content_data.contents[4].strip()),
                    "rate": str(content_data.contents[3].contents[3].contents[0]).strip(),
                    "tag": t
                }
            else:
                sj_5[key] = {
                    "now":str(content_data.contents[1].contents[1].contents[0]).strip(),
                    "before":str(content_data.contents[2].strip()),
                    "rate":str(content_data.contents[1].contents[3].contents[0]).strip(),
                    "tag":t
                }
        fansDataNew = ast.literal_eval(re.search("var fansDataNew = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))
        fansIncDataNew = ast.literal_eval(re.search("var fansIncDataNew = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))
        #日期
        bloggerdate = ast.literal_eval(re.search("var bloggerdate = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))
        #粉丝
        bloggerfansIncData = ast.literal_eval(
            re.search("var bloggerfansIncData = (.*);", str(soup)).groups(1)[0].strip().replace("null", "None"))
        #三连
        #点赞
        bloggerlikeIncData = ast.literal_eval(re.search("var bloggerlikeIncData = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))
        #收藏
        bloggerfavoriteIncData = ast.literal_eval(re.search("var bloggerfavoriteIncData = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))
        #投币
        bloggercoinIncData = ast.literal_eval(re.search("var bloggercoinIncData = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))


        #播放
        bloggerplayIncData = ast.literal_eval(re.search("var bloggerplayIncData = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))
        #评论
        bloggerreplyIncData = ast.literal_eval(re.search("var bloggerreplyIncData = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))
        #弹幕
        bloggerdanmuIncData = ast.literal_eval(re.search("var bloggerdanmuIncData = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))
        #分享
        bloggershareIncData = ast.literal_eval(re.search("var bloggershareIncData = (.*);", str(soup)).groups(1)[0].strip().replace("null","None"))

        data = {
            "up_face":up_face,
            "up_name":up_name,
            "urp_url":up_url,
            "classic":classic,
            "sex":sex,
            "lv":lv,
            "member":member,
            "intru":intru,
            "tags":tags,
            "sj_1":sj_1,
            "sj_2":sj_2,
            "sj_3":sj_3,
            "sj_4":sj_4,
            "sj_5":sj_5,
            "fansDataNew":fansDataNew,
            "fansIncDataNew ":fansIncDataNew ,
            "bloggerfansIncData":bloggerfansIncData ,

            "bloggerdate":bloggerdate ,

            "bloggerlikeIncData":bloggerlikeIncData,
            "bloggerfavoriteIncData":bloggerfavoriteIncData,
            "bloggercoinIncData":bloggercoinIncData,

            "bloggerplayIncData":bloggerplayIncData,
            "bloggerreplyIncData":bloggerreplyIncData,
            "bloggerdanmuIncData":bloggerdanmuIncData,
            "bloggershareIncData":bloggershareIncData

        }

        return data

def searchKeyword(ua,session,keyword):
    url = "http://bz.feigua.cn/member/TopSearch?keyword={}".format(keyword)
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

    try:
        r = session.get(url)
    except Exception as e:
        logging.warning("网站连接超时：{}".format(e))
        return False
    else:
        r.encoding = "utf-8"
        soup = bs(r.text, "html.parser")
        box = soup.find_all(class_="search-result-box")
        if box:
            items = box[0]
        else:
            return {}
        up_dict = {}
        up_list = []
        vedio_dict = {}
        up_data = items.find_all(class_="search-result-item")[0]
        up_num = up_data.contents[1].contents[3].contents[0].strip()
        up_items = up_data.find_all('li')
        for up_item in up_items:
            up_dict["up_face"] = up_item.find(class_="up-info__avatar").contents[1].contents[1].attrs["src"]
            isEm = up_item.find(class_="up-info__info-name").find_all('em')
            if isEm:
                name_str = ''
                for data in up_item.find(class_="up-info__info-name").contents[1].contents:
                    if isinstance(data, NavigableString):
                        name_str += data.strip()
                    else:
                        name_str += data.contents[0].strip()
                up_dict["up_name"] = name_str
            else:
                up_dict["up_name"] = up_item.find(class_="up-info__info-name").contents[1].contents[0].strip()
                print(up_dict)
            up_dict["fans_num"] = up_item.find(class_="up-info__info-lv").contents[0].strip()
            up_dict["uid"] = re.search("#/Blogger/Detail/(.*)",up_item.find(class_="up-info__avatar").contents[1].attrs["href"]).groups(1)[0]
            print(up_dict)
            up_list.append(up_dict)
            up_dict = {}
        vedio_data = items.find_all(class_="search-result-item")[1]
        vedio_dict = {}
        vedio_list = []
        vedio_num = vedio_data.contents[1].contents[3].contents[0].strip()
        vedip_items = vedio_data.find_all('li')
        for vedio_item in vedip_items:
            vedio_dict["up_face"] = vedio_item.find(class_="up-info__avatar").contents[1].contents[1].attrs["src"]
            isEm = vedio_item.find(class_="up-info__info-name").find_all('em')
            if isEm:
                name_str = ''
                for data in vedio_item.find(class_="up-info__info-name").contents[1].contents:
                    if isinstance(data, NavigableString):
                        name_str += data.strip()
                    else:
                        name_str += data.contents[0].strip()
                vedio_dict["up_name"] = name_str
            else:
                vedio_dict["up_name"] = vedio_item.find(class_="up-info__info-name").contents[1].contents[0].strip()
                print(vedio_dict)
            vedio_dict["fans_num"] = vedio_item.find(class_="up-info__info-lv").contents[0].strip()
            print(up_dict)
            vedio_list.append(up_dict)
            vedio_dict = {}
        data = {
            "up_num":up_num,
            "vedio_num":vedio_num,
            "up_list":up_list,
            "vedio_list":vedio_list
        }
        print(soup)
        return data

if __name__ == "__main__":
    uas = loadUserAgent("user_agents.txt")
    session = getSession(uas)
    searchKeyword(uas,session,"罗翔")