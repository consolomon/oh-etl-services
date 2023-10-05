from datetime import datetime
from logging import Logger
from lib.pg.pg_connect import PgConnect


class DdsChatProcessor:

    INSERT_DDS_H_CHAT_SCRIPT_PATH = "/src/lib/sql/insert_dds_h_chat.sql"
    INSERT_DDS_S_CHAT_INFO_SCRIPT_PATH = "/src/lib/sql/insert_dds_s_chat_info.sql"

    def __init__(
        self,
        logger: Logger,
        pg_connect: PgConnect
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect

    def run(self) -> None:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: DDS CHAT PROCESSOR: START")

        h_result = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.INSERT_DDS_H_CHAT_SCRIPT_PATH,
            operator_mode="insert"
        )
        s_result = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.INSERT_DDS_S_CHAT_INFO_SCRIPT_PATH,
            operator_mode="insert"
        )
        if h_result and s_result:
            self.logger.info(f"{datetime.utcnow()}: DDS CHAT PROCESSOR: SUCCESS")
        else:
            self.logger.info(f"{datetime.utcnow()}: DDS CHAT PROCESSOR: FAILED")

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}:DDS CHAT PROCESSOR: FINISH")


