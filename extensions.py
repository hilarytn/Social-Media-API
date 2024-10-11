from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail
import redis

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()

# Initialize Redis
redis_client = None

def init_redis(app):
    global redis_client
    redis_client = redis.StrictRedis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        password=app.config['REDIS_PASSWORD'],
        decode_responses=True
    )