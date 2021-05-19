from app.services import up_rank_bp
from flask import request,render_template,session,redirect,url_for,flash,jsonify
from app.forms import LoginForm,SignForm,ChangePersonFrom
from app.models import User
from flask_login import login_user,logout_user,current_user,login_required
from app.cli.fgSpider import getUpRank,getSession,loadUserAgent,getUpRiseFansRank,getUpDownFansRank,getDailyHotVideoRank
from app.cli.fgDetailSiper import getUpDetail,searchKeyword
import datetime
from config import classify
import uuid,logging,os
import ast

@up_rank_bp.route('/up_rank',methods=['GET','POST'])
def up_rank():
    p = session.get('logged_in')
    n = session.get('user_name')
    user = User.query.filter_by(username=n).first()
    if session.get('logged_in') is not True or not user or  user.username!= n:
        return redirect(url_for('up_rank.login'))

    user_face = user.user_face
    user_data = {
        "username":n,
        "user_face":user_face
    }
    if request.method == "GET":
        args = request.args
        period = 1
        datecode = args.get("datecode")
        classId = 0
        ajax = 1
        time_now = datetime.datetime.now()
        datecode_list = []
        if not datecode:
            datecode = (time_now + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        datecode_list = [time_now + datetime.timedelta(days=-num) for num in range(1, 8)]

        uas = loadUserAgent("user_agents.txt")
        s = getSession(uas)
        upRankData = getUpRank(uas,s,datecode,period,classId,ajax)
        upRankData['time_list'] = datecode_list
        upRankData['show_time'] = datetime.datetime.strptime(datecode,"%Y%m%d")
        return render_template("up_rank/up_rank.html",data_dict = upRankData,user_data=user_data)

@up_rank_bp.route('/up_rise_fans',methods=['GET','POST'])
def fans_rise():
    p = session.get('logged_in')
    n = session.get('user_name')
    user = User.query.filter_by(username=n).first()
    if session.get('logged_in') is not True or not user  or user.username!= n:
        return redirect(url_for('up_rank.login'))
    user_face = user.user_face
    user_data = {
        "username": n,
        "user_face": user_face
    }
    args = request.args
    period = args.get("period")
    datecode = args.get("datecode")
    classId = 0
    ajax = 1
    time_now = datetime.datetime.now()
    rank_type = args.get("rank_type")
    datecode_list = []
    if not rank_type:
        rank_type = "day"

    if rank_type == "day":
        period = 1
        if not datecode:
            datecode = (time_now + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        datecode_list = [time_now + datetime.timedelta(days=-num) for num in range(1, 8)]

    elif rank_type == "week":
        period = 7
        if not datecode:
            datecode = (time_now - datetime.timedelta(days=time_now.weekday()+1)).strftime("%Y%m%d")
        datecode_list = [(time_now - datetime.timedelta(days=time_now.weekday()+num)) for num in range(1,51,7)]

    elif rank_type == "mouth":
        period = 30
        this_month_start = datetime.datetime(time_now.year, time_now.month, 1)
        datecode_list = [this_month_start - datetime.timedelta(weeks=num) for num in range(4, 17, 4)]
        if not datecode:
            datecode = datetime.datetime(datecode_list[0].year, datecode_list[0].month, 1).strftime("%Y%m%d")


    uas = loadUserAgent("user_agents.txt")
    s = getSession(uas)
    up_rank_fans_rise = getUpRiseFansRank(uas,s,datecode,period,classId,ajax)
    up_rank_fans_rise['time_list'] = datecode_list
    up_rank_fans_rise['show_time'] = datetime.datetime.strptime(datecode,"%Y%m%d")
    return render_template("up_rank/up_rise_fans_{}.html".format(rank_type),data_dict = up_rank_fans_rise,datetime=datetime,user_data=user_data)

@up_rank_bp.route('/up_down_fans',methods=['GET','POST'])
def down_fans():
    p = session.get('logged_in')
    n = session['user_name']
    user = User.query.filter_by(username=n).first()
    if session.get('logged_in') is not True or not user  or user.username!= n:
        return redirect(url_for('up_rank.login'))
    user_face = user.user_face
    user_data = {
        "username": n,
        "user_face": user_face
    }
    args = request.args
    period = args.get("period")
    datecode = args.get("datecode")
    classId = 0
    ajax = 1
    time_now = datetime.datetime.now()
    rank_type = args.get("rank_type")
    datecode_list = []
    if not rank_type:
        rank_type = "day"

    if rank_type == "day":
        period = 1
        if not datecode:
            datecode = (time_now + datetime.timedelta(days=-1)).strftime("%Y%m%d")
        datecode_list = [time_now + datetime.timedelta(days=-num) for num in range(1, 8)]

    elif rank_type == "week":
        period = 7
        if not datecode:
            datecode = (time_now - datetime.timedelta(days=time_now.weekday() + 1)).strftime("%Y%m%d")
        datecode_list = [(time_now - datetime.timedelta(days=time_now.weekday() + num)) for num in range(1, 51, 7)]

    elif rank_type == "mouth":
        period = 30
        this_month_start = datetime.datetime(time_now.year, time_now.month, 1)
        datecode_list = [this_month_start - datetime.timedelta(weeks=num) for num in range(4, 17, 4)]
        if not datecode:
            datecode = datetime.datetime(datecode_list[0].year, datecode_list[0].month, 1).strftime("%Y%m%d")

    uas = loadUserAgent("user_agents.txt")
    s = getSession(uas)
    up_rank_down_fans = getUpDownFansRank(uas, s, datecode, period, classId, ajax)
    up_rank_down_fans['time_list'] = datecode_list
    up_rank_down_fans['show_time'] = datetime.datetime.strptime(datecode, "%Y%m%d")
    return render_template("up_rank/up_down_fans_{}.html".format(rank_type), data_dict=up_rank_down_fans,
                           datetime=datetime,user_data=user_data)

@up_rank_bp.route('/video_rank',methods=['GET','POST'])
def video_rank():
    #/datecode/period/classId/type
    p = session.get('logged_in')
    n = session['user_name']
    user = User.query.filter_by(username=n).first()
    if session.get('logged_in') is not True or not user  or user.username!= n:
        return redirect(url_for('up_rank.login'))
    user_face = user.user_face
    user_data = {
        "username": n,
        "user_face": user_face
    }
    args = request.args
    period = args.get("period")
    datecode = args.get("datecode")
    classId = args.get("classId")
    type_id = args.get("type_id")
    c_dict = classify
    time_now = datetime.datetime.now()
    datecode_list = []

    if not period:
        period = 1
    else:
        period = int(period)
    if not classId:
        classId = 0
    else:
        classId = int(classId)
    if not type_id :
        type_id  = 0
    else:
        type_id = int(type_id)

    if period == 1:
        datecode_list = [time_now + datetime.timedelta(days=-num) for num in range(2, 8)]
        if not datecode:
            datecode = (time_now + datetime.timedelta(days=-2)).strftime("%Y%m%d")

    elif period == 7:
        datecode_list = datecode_list = [(time_now - datetime.timedelta(days=time_now.weekday() + num)) for num in range(1, 51, 7)]
        if not datecode:
            datecode = (time_now - datetime.timedelta(days=time_now.weekday() + 1)).strftime("%Y%m%d")

    if type_id in c_dict:
        for num in c_dict:
            if num == type_id:
                c_dict[num]["active"] = "active"
            else:
                c_dict[num]["active"] = ""
    else:
        for num in c_dict:
            c_dict[num]["active"] = ""
        c_dict[0]["active"] = "active"

    uas = loadUserAgent("user_agents.txt")
    s = getSession(uas)
    video_rank_dict = getDailyHotVideoRank(uas,s,datecode,period,classId,type_id)
    video_rank_dict["datecode_list"] = datecode_list
    video_rank_dict["classify"] = c_dict
    video_rank_dict["show_time"] = datetime.datetime.strptime(datecode,"%Y%m%d")
    print(c_dict)
    return render_template("up_rank/video_rank.html",data_dict=video_rank_dict,type_id=type_id,classId=classId,period=period,datetime=datetime,user_data=user_data)

@up_rank_bp.route("/detail",methods=["GET","POST"])
def detail():
    p = session.get('logged_in')
    n = session['user_name']
    user = User.query.filter_by(username=n).first()
    if session.get('logged_in') is not True or not user or user.username != n:
        return redirect(url_for('up_rank.login'))

    user_face = user.user_face
    user_data = {
        "username": n,
        "user_face": user_face
    }
    if request.method == 'GET':
        #1up详细 2视频详细
        view_type = request.args.get("view_type")
        if not view_type:
            return redirect(url_for("up_rank.up_rank"))
        if view_type == "1":
            r = request.args
            uid = request.args.get("uid")
            uas = loadUserAgent("user_agents.txt")
            s = getSession(uas)
            detail_data = getUpDetail(uas,s,uid)
            date_time = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            date_time += "  11:31:54"
            return render_template("up_rank/up_detail.html",user_data=user_data,detail_data=detail_data,date_time=date_time)

@up_rank_bp.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template("login.html",form=form)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cheack_user = User.query.filter_by(username=username).first()
        if not cheack_user:
            flash(u"用户不存在")
            return redirect(url_for("up_rank.login"))
        cheack_password = cheack_user.verify_password(password)
        if not cheack_password:
            flash("密码错误")
            return redirect(url_for("up_rank.login"))
        next_page = request.args.get("next")
        if not next_page:
            next_page = url_for('up_rank.up_rank')
        session['logged_in'] = True
        session['user_name'] = username
        return redirect(next_page)


@up_rank_bp.route("/sign",methods=["GET","POST"])
def sign():
    form = SignForm()
    if request.method == "GET":
        return render_template("sign.html",form=form)
    if request.method == "POST":
        if form.validate() is False:
            print(form.errors)
            msg = {}
            for key in form.errors:
                msg[key] = form.errors[key]
                flash(msg)
            print(msg)
            return redirect(url_for("up_rank.sign"))
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        phone = request.form.get("phone")
        sex = request.form.get("sex")
        user_face = request.files
        sign_time = datetime.datetime.now().strftime("%Y-%m-%d")
        #检测用户是否重复
        cheack_user = User.query.filter_by(username=form.username.data).first()
        if cheack_user:
            flash("用户名以存在")
            return redirect(url_for('up_rank.sign'))
        new_uuid = str(uuid.uuid4())
        password_hash = User.get_password_hash(password)
        try:
            if not user_face:
                file_name = "logo.jpg"
            else:
                file_name = username
                user_face.save(r".\app\static\image",file_name)
            User.add_user(new_uuid,username,email,password_hash,file_name,phone,sex,sign_time)
        except Exception as e:
            logging.warning(e)
            flash("创建用户失败，请稍后再试！")
            return redirect(url_for("up_rank.sign"))
        flash("创建用户成功，请登陆！")
        return redirect(url_for("up_rank.login"))

@up_rank_bp.route("/personal",methods=["GET","POST"])
def personal():
    p = session.get('logged_in')
    n = session['user_name']
    user = User.query.filter_by(username=n).first()
    if session.get('logged_in') is not True or not user or user.username != n:
        return redirect(url_for('up_rank.login'))
    form = ChangePersonFrom()
    if request.method == "GET":
        user_face = user.user_face
        user_data = {
            "username": n,
            "user_face": user_face,
            "id":str(user.uuid),
            "phone":user.phone,
            "email":user.email,
            "sign_time":user.sign_time,
            "sex":user.sex,
            "intru":user.introduction
        }
        #1或none 为 个人中心，2为更改个人信息界面 3为通知界面 4为管理界面
        view_type = request.args.get("view_type")
        if view_type == "1" or not view_type:
            return render_template("personal.html",user_data=user_data,view_type="1")
        elif view_type == "2" :
            return render_template("personal.html",user_data=user_data,view_type="2",form=form)
        elif view_type == "3" :
            return render_template("personal.html",user_data=user_data,view_type="3")
        elif view_type == "4":
            users = User.query.filter(User.username!=n).filter(User.active=='0').all()
            return render_template("personal.html",user_data=user_data,view_type="4",users=users)
        elif view_type == "5":
            users = User.query.filter(User.username!=n).filter(User.active=='-1').all()
            return render_template("personal.html", user_data=user_data, view_type="5", users=users)
        elif view_type == "7":
            if user.active != "1":
                return redirect(url_for("up_rank.login"))
            id = request.args.get("id")
            result = User.changeActive(id,"-1")
            print(result)
            return redirect(url_for("up_rank.personal",view_type="4"))
        elif view_type == "8":
            if user.active != "1":
                return redirect(url_for("up_rank.login"))
            id = request.args.get("id")
            cheack_user = User.query.filter_by(uuid=id).first()
            if not cheack_user:
                return redirect(url_for("up_rank.personal",view_type="4"))
            form = ChangePersonFrom()
            user_data = {
                "username": cheack_user.username,
                "user_face": cheack_user.user_face,
                "id": str(cheack_user.uuid),
                "phone": cheack_user.phone,
                "email": cheack_user.email,
                "sign_time": cheack_user.sign_time,
                "sex": cheack_user.sex,
                "intru": cheack_user.introduction
            }
            return render_template("personal.html", user_data=user_data, view_type="8",form=form)
        elif view_type == "9":
            if user.active != "1":
                return redirect(url_for("up_rank.login"))
            id = request.args.get("id")
            result = User.changeActive(id, "0")
            print(result)
            return redirect(url_for("up_rank.personal", view_type="5"))



    if request.method == "POST":
        if form.validate() is False:
            print(form.errors)
            msg = {}
            for key in form.errors:
                msg[key] = form.errors[key]
                flash(msg)
            print(msg)
            return redirect(url_for("up_rank.personal",view_type="2"))
        username = request.form.get("username")
        cheack_user = User.query.filter_by(username=n).first()
        if cheack_user:
            flash({
                "username":"用户名以存在！"
            })
            return redirect(url_for("up_rank.personal",view_type="2"))
        old_psw = request.form.get("old_password")
        cheack_psw = User.get_password_hash(old_psw)
        if cheack_psw != user.password_hash:
            flash({
                "old_password":"输入的旧密码与当前密码不一致！"
            })
            return redirect(url_for("up_rank.personal",view_type="2"))
        new_psw_hash = User.get_password_hash(request.form.get("password"))
        email = request.form.get("email")
        phone = request.form.get("email")
        sex = request.form.get("sex")
        intru = request.form.get("intru")
        if intru:
            intru = None
        User.update_user(cheack_user,username,email,new_psw_hash,None,phone,sex,intru)
        flash("更改成功，请重新登录！")
        session["login_in"] = False
        return  redirect(url_for("up_rank.login"))


@up_rank_bp.route("/search",methods=["POST"])
def search():
    p = session.get('logged_in')
    n = session['user_name']
    user = User.query.filter_by(username=n).first()
    if session.get('logged_in') is not True or not user or user.username != n:
        return jsonify({
            "status_code":400,
            "msg":""
        })
    if request.method == "POST":
        keyword = request.form.get("keyword")
        if keyword :
            keyword = ast.literal_eval(keyword)
            uas = loadUserAgent("user_agents.txt")
            s = getSession(uas)
            search_result = searchKeyword(uas,s,keyword)
        if search_result:
            return jsonify({
                "status_code":200,
                "data":search_result
            })
        else:
            return {}
