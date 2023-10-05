import time
from datetime import datetime
from logging import Logger


class SampleMessageProcessor:
    def __init__(self,
                 logger: Logger) -> None:
        self.logger = logger

    def run(self) -> None:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: START")

        time.sleep(2)

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}: FINISH")
