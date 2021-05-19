from os import path

class Config:

    SECRET_KEY = ''

    #DATABASE
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #UP_LOAD
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    UPLOADED_IMAGEFILES_DEST = path.join(path.dirname(path.abspath(__file__))),"/app/static/image"


    DEBUG = True



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ""
    REDIS_URL = ""


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = ""

config = {
    "development": DevelopmentConfig,
    "test":ProductionConfig,
    "product":ProductionConfig,
    'default':DevelopmentConfig
}

classify = {
        0:{
            "title":"不限",
            "active":"",
            "code":'0'
        },
        155:{
            "title":"时尚",
            "active":"",
            "code":'155'
        },
        160:{
            "title":"生活",
            "active":"",
            "code":'160'
        },
         1:{
            "title":"动画",
            "active":"",
            "code":'1'
        },
         3:{
            "title":"音乐",
            "active":"",
            "code":'3'
        },
         129:{
            "title":"舞蹈",
            "active":"",
            "code":'129'
        },
         4:{
            "title":"游戏",
            "active":"",
            "code":'4'
        },
         36:{
            "title":"知识",
            "active":"",
            "code":'36'
        },
         188:{
            "title":"数码",
            "active":"",
            "code":'188'
        },
         202:{
            "title":"咨询",
            "active":"",
            "code":'202'
        },
         119:{
            "title":"鬼畜",
            "active":"",
            "code":'119'
        },
         165:{
            "title":"广告",
            "active":"",
            "code":'165'
        },
         5:{
            "title":"娱乐",
            "active":"",
            "code":'5'
        },
         181:{
            "title":"影视",
            "active":"",
            "code":'181'
        },
         13:{
            "title":"番剧",
            "active":"",
            "code":'13'
        },
         167:{
            "title":"国创",
            "active":"",
            "code":'167'
        },
        177:{
            "title":"纪录片",
            "active":"",
            "code":'177'
        },
        23:{
            "title":"电影",
            "active":"",
            "code":'23'
        },
        11:{
            "title":"电视剧",
            "active":"",
            "code":'11'
        },
    }