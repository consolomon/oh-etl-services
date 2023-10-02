from datetime import datetime
from logging import Logger
from lib.pg.pg_connect import PgConnect


class DdsPositionTechnologyProcessor:

    INSERT_DDS_L_POSITION_TECHNOLOGY_SCRIPT_PATH = "/src/lib/sql/insert_dds_l_position_technology.sql"
    SELECT_DDS_L_POSITION_TECHNOLOGY_LAST_DT_SCRIPT_PATH = "/src/lib/sql/select_dds_l_position_technology_last_dt.sql"

    def __init__(
        self,
        logger: Logger,
        pg_connect: PgConnect
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect

    def run(self) -> None:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: DDS POSITION TECHNOLOGY PROCESSOR: START")

        last_load_dt = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_DDS_L_POSITION_TECHNOLOGY_LAST_DT_SCRIPT_PATH,
            operator_mode="select",
            selected_class="LastLoadDt"
        )[0].load_dt

        result = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.INSERT_DDS_L_POSITION_TECHNOLOGY_SCRIPT_PATH,
            operator_mode="insert",
            script_args={
                "load_dt": last_load_dt,
            }
        )
        if result:
            self.logger.info(f"{datetime.utcnow()}: DDS POSITION TECHNOLOGY PROCESSOR: SUCCESS")
        else:
            self.logger.info(f"{datetime.utcnow()}: DDS POSITION TECHNOLOGY PROCESSOR: FAILED")

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}: DDS POSITION TECHNOLOGY PROCESSOR: FINISH")
