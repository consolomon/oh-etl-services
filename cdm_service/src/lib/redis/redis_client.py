import json
from typing import Dict, List

import redis


class RedisClient:
    def __init__(self, host: str, port: int, password: str) -> None:
        self.client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            ssl=False)

    def set(self, k, v):
        self.client.set(k, json.dumps(v))

    def get(self, k) -> Dict | List | None:

        obj: str | None = self.client.get(k)  # type: ignore
        if obj is not None:
            return json.loads(obj)
        else:
            return None
