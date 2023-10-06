from lib.redis.redis_client import RedisClient


def check_user(user_name: str, user_key: str, redis: RedisClient) -> bool:
    user_dict = redis.get("api_users")
    if user_dict.get(user_name) is not None:
        user = user_dict.get(user_name)
        if user["user_key"] == user_key:
            return True
        else:
            return False
    else:
        return False


def check_admin(user_key: str, redis: RedisClient) -> bool:
    user = redis.get("api_admin")
    if user["user_key"] == user_key:
        return True
    else:
        return False


def set_user(user: dict, admin_key: str, redis: RedisClient):
    if check_admin(admin_key, redis):
        user_dict = redis.get("api_users")
        user_dict[user["user_name"]] = user
        redis.set("api_users", user_dict)
        return True
    else:
        return False


def get_user(user_name: str, admin_key: str, redis: RedisClient) -> dict | None:
    if check_admin(admin_key, redis):
        user_dict = redis.get("api_users")
        return user_dict.get(user_name)
    else:
        return None


def delete_user(user_name: str, admin_key: str, redis: RedisClient):
    if check_admin(admin_key, redis):
        user_dict = redis.get("api_users")
        if user_dict.get(user_name) is not None:
            user = user_dict.pop(user_name)
            redis.set("api_users", user_dict)
            return user
        return None
    else:
        return False
