# 部分飞瓜数据抓取展示WEB


## 特别声明

* 本仓库发布的 `fg_show_web` 项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
* 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。
* `IKkSssDendi` 对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.
* 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。
* 以任何方式查看此项目的人或直接或间接使用`fg_show_web`项目的任何脚本的使用者都应仔细阅读此声明。`IKkSssDendi` 保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或j`fg_show_web`项目，则视为您已接受此免责声明。
* 您必须在下载后的24小时内从计算机或手机中完全删除以上内容。

>您使用或者复制了本仓库且本人制作的任何代码或项目，则视为已接受此声明，请仔细阅读
您在本声明未发出之时点使用或者复制了本仓库且本人制作的任何代码或项目且此时还在使用，则视为已接受此声明，请仔细阅读

## 简介
该项目功能为抓取飞瓜数据部分Bilibili板块数据进行缓存并在Web端进行展示，该项目纯属自娱自乐的产物。

## 项目结构

` 

    │  config.py
    │  README.md
    │  requirements.txt
    │  run.py
    │  tree.txt
    │  user_agents.txt
    │  
    └─app
        │  databse.py
        │  extensions.py
        │  forms.py
        │  models.py
        │  __init__.py
        │  
        ├─cli
        │      cache.py
        │      fgDetailSiper.py
        │      fgSpider.py
        │      setSession.py
        │      user_agents.txt
        │      __init__.py
        │      
        ├─services
        │      up_rank.py
        │      __init__.py
        │      
        ├─static
        │  ├─css
        │  │      login.css
        │  │      
        │  ├─image
        │  │      jiamianqishi.png
        │  │      logo.jpg
        │  │      rz.jpg
        │  │      
        │  └─js
        │          customed.js
        │          search.js
        │          
        └─templates
            │  base.html
            │  login.html
            │  personal.html
            │  sign.html
            │  
            └─up_rank
                    up_detail.html
                    up_down_fans_day.html
                    up_down_fans_mouth.html
                    up_down_fans_week.html
                    up_rank.html
                    up_rise_fans_day.html
                    up_rise_fans_mouth.html
                    up_rise_fans_week.html
                    video_rank.html
                
`

## 如何使用
* ` pip install -r requirements.txt`
* 在config.py中配置好相关信息
* 在`setSession.py`配置好自己的飞瓜数据账号与密码
* `run run.py`

## 效果图
![登录界面](https://i.loli.net/2021/05/19/21uwORALtJVN6Pa.png)
![榜单界面](https://i.loli.net/2021/05/19/FnOjMf4yPLYXIH2.png)
![up主详细](https://i.loli.net/2021/05/19/76b5iFBmSruDPQA.png)
![搜索界面](https://i.loli.net/2021/05/19/FJIpRsv3Aynb5tL.png)
![个人中心](https://i.loli.net/2021/05/19/yAgQKXrf1ujhOnU.png)

## To-Do-List

- 登录，注册功能
  - [x] 密码哈希存储
  - [x] 密匙加密 
  - [ ] 管理员权限鉴权
  - [ ] 注册头像文件存储
- 数据页面
  - [x] UP主总榜单  
  - [x] UP主掉粉榜单
   - [x] UP主涨粉榜单
   - [x] 视频播放量榜单
   - [x] 视频分区
   - [x] 时间选择
   - [x] UP主 详细
   - [ ] 视频详细
   - [x] 搜索功能
   - [ ] 数据Excel文件导出
 - 个人中心
   - [x] 个人数据 （待完善）
   - [ ] 通知发布，管理
   - [x] 黑名单 （待完善）
- to be continued ...