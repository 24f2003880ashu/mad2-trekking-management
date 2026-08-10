from datetime import timedelta
from datetime import timedelta

class Config:

    SECRET_KEY = "mad2-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///trekking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "mad2_trekking_application_super_secret_key_2026"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/0"