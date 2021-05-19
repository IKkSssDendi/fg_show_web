from app import redis_client as rc
from app.cli.setSession import loadUserAgent,getSession
from datetime import datetime
import ast

def cache(dataType:str,*args, **kwargs):
    """
    :param dataType:
    upRank up主排名
    upRiseFansRank up粉丝增加排名
    upDownFansRank up主掉粉排名
    hotVideoRank    视频播放排名
    :param datetime "%Y-%m-%d"
    :param args:
    :param kwargs:
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            args_data = [data for data in args]
            name = func.__name__
            date_time = args_data[2]
            period = args_data[3]
            classId = args_data[4]
            classify = None
            if name == "getDailyHotVideoRank":
                classify = args_data[5]
                key = "{}-{}-{}-{}-{}".format(dataType, period, classId, classify,date_time)
            else:
                key = "{}-{}-{}-{}".format(dataType,period,classId,date_time)
            if rc.hexists(name,key):
                data_dict = rc.hget(name,key)
                data_dict = ast.literal_eval(bytes.decode(data_dict))

                return data_dict
            else:
                uas = loadUserAgent("user_agents.txt")
                session = getSession(uas)
                period = args_data[3]
                classId = args_data[4]
                if not classify :
                    ajax = args_data[5]
                    data_dict = func(uas, session, date_time, period, classId, ajax)
                else:
                    data_dict = func(uas, session, date_time, period, classId, classify)
                data_dict["date_time"] = datetime.now().strftime("%Y-%m-%d")
                rc.hset(name,key,str(data_dict))

                return data_dict
        return wrapper
    return decorator

def detailCache(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            args_data = [data for data in args]
            uid = args_data[2]
            name = uid
            date_time = datetime.now().strftime("%Y%m%d")
            key = uid + date_time
            if rc.hexists(name, key):
                data = rc.hget(name,key)
                data = ast.literal_eval(bytes.decode(data))
                return data
            else:
                uas = loadUserAgent("user_agents.txt")
                session = getSession(uas)
                data = func(uas,session,uid)
                rc.hset(name,key,str(data))
            return data
        return wrapper
    return decorator