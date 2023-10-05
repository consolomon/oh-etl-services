import time
from datetime import datetime
from logging import Logger


class SampleMessageProcessor:
    def __init__(
        self,
        logger: Logger,

    ) -> None:
        self.logger = logger

    # функция, которая будет вызываться по расписанию.
    def run(self) -> None:
        # Пишем в лог, что джоб был запущен.
        self.logger.info(f"{datetime.utcnow()}: START")

        # Имитация работы. Здесь будет реализована обработка сообщений.
        time.sleep(2)

        # Пишем в лог, что джоб успешно завершен.
        self.logger.info(f"{datetime.utcnow()}: FINISH")
