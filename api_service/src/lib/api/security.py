import uuid
import functools
from flask import request

from lib.api import users
from app_config import AppConfig


def key_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers.get("x-api-user") and request.headers.get("x-api-key"):
            api_user = request.headers.get("x-api_user")
            api_key = request.headers.get("x-api-key")
        else:
            return {"message": "Please provide an API key and user"}, 400
        # Check if API key is correct and valid
        config = AppConfig()
        if api_key == config.API_ADMIN_KEY:
            return func(*args, **kwargs)
        redis = config.redis_client()
        if users.check_user(api_user, api_key, redis):
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key and name is not valid"}, 403
    return decorator


def admin_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers:
            api_key = request.headers.get("x-api-key")
        else:
            return {"message": "Please provide an admin API key"}, 400
        # Check if API key is correct and valid

        if api_key == AppConfig().API_ADMIN_KEY:
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403
    return decorator


def init_api_key_check(config: AppConfig):
    redis = config.redis_client()
    admin = {
        "user_name": "admin",
        "user_key": config.API_ADMIN_KEY,
        "user_level": "admin"
    }
    redis.set("api_admin", admin)

    if redis.get("api_users") is None:
        redis.set("api_users", {})


def create_api_key(user_name: str) -> str:
    return uuid.uuid5(uuid.uuid4(), user_name).hex
