from flask_redis import  FlaskRedis
from flask_uploads import UploadSet, IMAGES


imagefiles = UploadSet("imagefiles", IMAGES)
redis_client = FlaskRedis()
