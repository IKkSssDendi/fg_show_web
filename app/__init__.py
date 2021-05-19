from flask import Flask
from app.databse import db
import config
from flaskext.markdown import Markdown
from flask_bootstrap import  Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from app.extensions import redis_client,imagefiles
from flask_uploads import configure_uploads

moment = Moment()  # 时间本地化
bootstrap = Bootstrap()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.config['product'])

    db.init_app(app)
    Markdown(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login.init_app(app)
    redis_client.init_app(app)
    configure_uploads(app,imagefiles)
    login.login_view = 'login'

    from app.services import up_rank_bp
    app.register_blueprint(up_rank_bp)

    return app