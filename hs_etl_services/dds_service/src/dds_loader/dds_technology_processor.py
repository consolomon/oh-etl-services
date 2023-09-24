from datetime import datetime
from logging import Logger
from lib.pg.pg_connect import PgConnect


class DdsTechnologyProcessor:

    INSERT_DDS_TECHNOLOGIES_SCRIPT_PATH = "/src/lib/sql/insert_dds_technologies.sql"

    def __init__(
        self,
        logger: Logger,
        pg_connect: PgConnect
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect

    def run(self) -> None:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: DDS TECHNOLOGY PROCESSOR: START")

        result = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.INSERT_DDS_TECHNOLOGIES_SCRIPT_PATH,
            operator_mode="insert"
        )
        if result:
            self.logger.info(f"{datetime.utcnow()}: DDS TECHNOLOGY PROCESSOR: SUCCESS")
        else:
            self.logger.info(f"{datetime.utcnow()}: DDS TECHNOLOGY PROCESSOR: FAILED")

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}:DDS TECHNOLOGY PROCESSOR: FINISH")
