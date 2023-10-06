import os

from lib.pg import PgConnect
from lib.redis.redis_client import RedisClient


class AppConfig:

    CERTIFICATE_PATH = '/crt/my_CA.crt'
    INSERT_STG_POSITION_SCRIPT_PATH = "/src/lib/sql/insert_stg_position.sql"
    INSERT_STG_TECHNOLOGY_SCRIPT_PATH = "/src/lib/sql/insert_stg_technology.sql"
    DEFAULT_JOB_INTERVAL = 60
    DEFAULT_BATCH_SIZE = 100

    def __init__(self) -> None:
        self.pg_warehouse_host = str(os.getenv('PG_WAREHOUSE_HOST') or "")
        self.pg_warehouse_port = int(str(os.getenv('PG_WAREHOUSE_PORT') or 0))
        self.pg_warehouse_dbname = str(os.getenv('PG_WAREHOUSE_DBNAME') or "")
        self.pg_warehouse_user = str(os.getenv('PG_WAREHOUSE_USER') or "")
        self.pg_warehouse_password = str(os.getenv('PG_WAREHOUSE_PASSWORD') or "")

        self.redis_host = str(os.getenv("REDIS_HOST") or "")
        self.redis_port = int(os.getenv("REDIS_PORT") or 0)
        self.redis_password = str(os.getenv("REDIS_PASSWORD") or "")

        self.FLASK_SECRET_KEY = str(os.getenv('FLASK_SECRET_KEY') or "")
        self.API_ADMIN_KEY = str(os.getenv('API_ADMIN_KEY') or "")

    def pg_warehouse_db(self) -> PgConnect:
        return PgConnect(
            self.pg_warehouse_host,
            self.pg_warehouse_port,
            self.pg_warehouse_dbname,
            self.pg_warehouse_user,
            self.pg_warehouse_password
        )

    def redis_client(self) -> RedisClient:
        return RedisClient(
            self.redis_host,
            self.redis_port,
            self.redis_password
        )
