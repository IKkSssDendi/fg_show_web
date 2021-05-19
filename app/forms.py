from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,FileField,TextAreaField
from  wtforms.fields import core
from wtforms.validators import DataRequired,EqualTo,Email,Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import imagefiles

class LoginForm(FlaskForm):
    '''
        username:   账号
        password:   密码
        remeber_me: 记住我选项布尔值
    '''
    username = StringField("username",validators=[DataRequired()],render_kw={'placeholder':'请输入账号：'})
    password = PasswordField("password",validators=[DataRequired()],render_kw={'placeholder':'请输入密码：'})
    remember_me = BooleanField("记住我",default=False)
    submit = SubmitField("login")


class SignForm(FlaskForm):
    '''
        username:   账号
        password:   密码
        remeber_me: 记住我选项布尔值
    '''
    username = StringField("username",validators=[DataRequired(message=u"账号或密码不能为空"),Length(1,11)],render_kw={'placeholder':'请输入账号：'})
    password = PasswordField("password",validators=[DataRequired(message=u"账号密码不能为空"),Length(6,16),EqualTo("cheack_password",message=u"两次输入的密码不一致")],render_kw={'placeholder':'请输入密码：'})
    cheack_password = PasswordField("cheack_password",render_kw={'placeholder':'请再次输入密码：'})
    email = StringField("E-mail",validators=[Email(message=u"邮箱格式错误")],render_kw={'placeholder':'请输入邮箱'})
    phone = StringField("telphone",validators=[Length(6,11)],render_kw={'placeholder':'请输入手机号码'})
    sex = core.SelectField(label="性别",
        choices=(
            ("1","男"),
            ("0","女"),
            ("3","未知")
        ))
    user_face = FileField(u'user_face', validators=[
        FileAllowed(imagefiles, u'只能上传图片！')])
    submit = SubmitField("sign")

class ChangePersonFrom(FlaskForm):
    username = StringField("username", validators=[DataRequired(message=u"账号或密码不能为空"),Length(1,6)])
    old_password = PasswordField("password", validators=[DataRequired(message=u"账号密码不能为空")],render_kw={'placeholder': '请输入旧密码：'})
    password = PasswordField("password", validators=[DataRequired(message=u"账号密码不能为空"),Length(6,16),
                                                     EqualTo("cheack_password", message=u"两次输入的密码不一致")],
                             render_kw={'placeholder': '请输入新密码：'})
    cheack_password = PasswordField("cheack_password", render_kw={'placeholder': '请再次输入密码：'})
    email = StringField("E-mail", validators=[Email(message=u"邮箱格式错误")])
    phone = StringField("telphone",validators=[Length(6,11)])
    sex = core.SelectField(label="性别",
                           choices=(
                               ("1", "男"),
                               ("0", "女"),
                               ("3", "未知")
                           ))
    user_face = FileField(u'user_face', validators=[
        FileAllowed(imagefiles, u'只能上传图片！')])
    intru = TextAreaField(u"intru",validators=[Length(0,200)])
    submit = SubmitField("change")