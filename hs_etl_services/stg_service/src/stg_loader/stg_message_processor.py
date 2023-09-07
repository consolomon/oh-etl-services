import time
from datetime import datetime
from logging import Logger
from hs_etl_services.stg_service.src.lib.pg.pg_connect import PgConnect
from hs_etl_services.stg_service.src.lib.pyrogram_api.pyrogram_client import PyrogramClient


class StgMessageProcessor:
    def __init__(
            self,
            logger: Logger,
            pg_connect: PgConnect,
            pyrogram_client: PyrogramClient
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect
        self.pyrogram_client = pyrogram_client

    # функция, которая будет вызываться по расписанию.
    def run(self) -> None:
        # Пишем в лог, что джоб был запущен.
        self.logger.info(f"{datetime.utcnow()}: START")

        # Имитация работы. Здесь будет реализована обработка сообщений.
        time.sleep(2)

        # Пишем в лог, что джоб успешно завершен.
        self.logger.info(f"{datetime.utcnow()}: FINISH")
