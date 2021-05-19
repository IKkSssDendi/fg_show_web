from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db,login

PROFILE_FILE = "profiles.json"

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    uuid = db.Column(db.String(70), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_face = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    sex = db.Column(db.String(10))
    sign_time = db.Column(db.String(20))
    introduction = db.Column(db.String(200))
    active = db.Column(db.String(5)) #0普通用户，1管理员，-1拉黑
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self,uuid,username,email,password_hash,user_face,phone,sex,sign_time):
        self.uuid = uuid
        self.username = username
        self.email = email
        self.password_hash = password_hash,
        self.user_face = user_face
        self.phone = phone
        self.sex = sex
        self.sign_time = sign_time
        self.active = "0"
    def __repr__(self):
        return '<User {}>'.format(self.username)

    @classmethod
    def add_user(self,uuid,username,email,password_hash,user_face,phone,sex,sign_time):
        new_user = User(uuid,username,email,password_hash,user_face,phone,sex,sign_time)
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def update_user(self,user,username,email,password_hash,user_face,phone,sex,intru):
        if username:
            user.username = username
        if email:
            user.email = email
        if password_hash:
            user.password_hash = password_hash
        if phone:
            user.phone = phone
        if sex:
            user.sex = sex
        if intru:
            user.introduction = intru
        db.session.commit()

    @classmethod
    def changeActive(cls,uuid,active):
        try:
            user = User.query.filter_by(uuid=uuid).first()
            user.active = active
            db.session.commit()
        except Exception as e:
            return False
        return True


    @classmethod
    def get_password_hash(self,password):
        return generate_password_hash(password)

    @property
    def password(self):
        raise  AttributeError("password 是不可读属性!")

    @password.setter
    def password(self,password:str) -> None:
        '''
        数据库只存储密码的哈希值。
        '''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password:str) -> bool:
        return check_password_hash(self.password_hash,password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.String(70), db.ForeignKey('user.uuid'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
