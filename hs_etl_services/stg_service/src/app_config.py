import os

from lib.pg import PgConnect
from lib.pyrogram_api.pyrogram_client import PyrogramClient


class AppConfig:
    CERTIFICATE_PATH = '/crt/YandexInternalRootCA.crt'
    DEFAULT_JOB_INTERVAL = 60
    DEFAULT_BATCH_SIZE = 100

    def __init__(self) -> None:
        self.pg_warehouse_host = str(os.getenv('PG_WAREHOUSE_HOST') or "")
        self.pg_warehouse_port = int(str(os.getenv('PG_WAREHOUSE_PORT') or 0))
        self.pg_warehouse_dbname = str(os.getenv('PG_WAREHOUSE_DBNAME') or "")
        self.pg_warehouse_user = str(os.getenv('PG_WAREHOUSE_USER') or "")
        self.pg_warehouse_password = str(os.getenv('PG_WAREHOUSE_PASSWORD') or "")

        self.telegram_api_id = int(os.getenv('TELEGRAM_API_ID') or 0)
        self.telegram_api_hash = str(os.getenv('TELEGRAM_API_HASH') or "")

    def pg_warehouse_db(self):
        return PgConnect(
            self.pg_warehouse_host,
            self.pg_warehouse_port,
            self.pg_warehouse_dbname,
            self.pg_warehouse_user,
            self.pg_warehouse_password
        )

    def pyrogram_client(self):
        return PyrogramClient(
            self.telegram_api_id,
            self.telegram_api_hash
        )
