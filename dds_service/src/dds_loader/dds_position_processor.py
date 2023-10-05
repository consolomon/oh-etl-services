from datetime import datetime
from logging import Logger
from lib.pg.pg_connect import PgConnect


class DdsPositionProcessor:

    INSERT_DDS_S_POSITION_INFO_SCRIPT_PATH = "/src/lib/sql/insert_dds_s_position_info.sql"
    INSERT_DDS_H_POSITION_SCRIPT_PATH = "/src/lib/sql/insert_dds_h_position.sql"

    def __init__(
        self,
        logger: Logger,
        pg_connect: PgConnect
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect

    def run(self) -> None:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: DDS POSITION PROCESSOR: START")

        h_result = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.INSERT_DDS_H_POSITION_SCRIPT_PATH,
            operator_mode="insert"
        )

        s_result = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.INSERT_DDS_S_POSITION_INFO_SCRIPT_PATH,
            operator_mode="insert"
        )
        if h_result and s_result:
            self.logger.info(f"{datetime.utcnow()}: DDS POSITION PROCESSOR: SUCCESS")
        else:
            self.logger.info(f"{datetime.utcnow()}: DDS POSITION PROCESSOR: FAILED")

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}:DDS POSITION PROCESSOR: FINISH")
