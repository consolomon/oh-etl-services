import re
from datetime import datetime
from logging import Logger
from lib.pg.pg_connect import PgConnect, WfSettings


class DdsVacancyPositionTechnologyProcessor:

    BATCH_LIMIT = 1000

    SELECT_WF_SETTINGS_SCRIPT_PATH = "/src/lib/sql/select_wf_settings.sql"
    INSERT_WF_SETTINGS_SCRIPT_PATH = "/src/lib/sql/insert_wf_settings.sql"

    SELECT_DDS_VACANCIES_SCRIPT_PATH = "/src/lib/sql/select_dds_vacancies.sql"
    SELECT_DDS_POSITIONS_SCRIPT_PATH = "/src/lib/sql/select_dds_positions.sql"
    SELECT_DDS_TECHNOLOGIES_SCRIPT_PATH = "/src/lib/sql/select_dds_technologies.sql"

    INSERT_DDS_L_VACANCY_POSITION_SCRIPT_PATH = "/src/lib/sql/insert_dds_l_vacancy_position.sql"
    INSERT_DDS_L_VACANCY_TECHNOLOGY_SCRIPT_PATH = "/src/lib/sql/insert_dds_l_vacancy_technology.sql"

    def __init__(
            self,
            logger: Logger,
            pg_connect: PgConnect
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect

    def run(self) -> None:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: DDS VACANCY POSITION TECHNOLOGY PROCESSOR: START")

        # Get workflow settings for l_vacancy_position table
        wf_settings = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_WF_SETTINGS_SCRIPT_PATH,
            operator_mode="select",
            selected_class="WfSettings",
            script_args={
                "wf_table": "l_vacancy_position&l_vacancy_technology",
                "wf_key": "h_vacancy.load_dt"
            }
        )

        # Setup basic state in case of empty workflow settings
        if not wf_settings:
            wf_settings = WfSettings(
                wf_id=0,
                wf_table="l_vacancy_position&l_vacancy_technology",
                wf_key="h_vacancy.load_dt",
                wf_value=datetime.min.isoformat(sep=" ", timespec="milliseconds")
            )
        else:
            wf_settings = wf_settings[0]

        # Get a batch of a messages from stg.messages
        vacancy_list = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_DDS_VACANCIES_SCRIPT_PATH,
            operator_mode="select",
            selected_class="VacancyText",
            script_args={
                "load_dt": wf_settings.wf_value,
                "batch_limit": self.BATCH_LIMIT
            }
        )

        # Process the ways when vacancy list is filled, empty or missing
        if vacancy_list is None:
            self.logger.info(f"{datetime.utcnow()}: DDS VACANCY POSITION TECHNOLOGY PROCESSOR: don't have new items to process")
        elif vacancy_list is not None and vacancy_list is not False:

            # ETL processing matches between positions and vacancies
            self.logger.info(
                f"{datetime.utcnow()}: DDS VACANCY POSITION TECHNOLOGY PROCESSOR: got new batch with {len(vacancy_list)} items")

            # Get positions list from database
            positions_list = self.pg_connect.pg_operator(
                log=self.logger,
                path_to_script=self.SELECT_DDS_POSITIONS_SCRIPT_PATH,
                operator_mode="select",
                selected_class="HPosition"
            )

            # Get technology list from database
            tech_list = self.pg_connect.pg_operator(
                log=self.logger,
                path_to_script=self.SELECT_DDS_TECHNOLOGIES_SCRIPT_PATH,
                operator_mode="select",
                selected_class="HTechnology"
            )

            # Create tech map to optimize searching process
            full_pattern = r""
            tech_dict = {}
            for tech in tech_list:
                full_pattern += (tech.tech_name + "|")
                tech_dict[tech.tech_name.lower()] = tech.hk_tech_id
            full_pattern = full_pattern.removesuffix("|")

            for vacancy in vacancy_list:

                # Search and insert position matches in vacancy
                for position in positions_list:
                    match = re.search(rf"{position.position_keywords}", vacancy.message_text, re.IGNORECASE)
                    if match:
                        self.pg_connect.pg_operator(
                            log=self.logger,
                            path_to_script=self.INSERT_DDS_L_VACANCY_POSITION_SCRIPT_PATH,
                            operator_mode="insert",
                            script_args={
                                    "hk_vacancy_id": vacancy.hk_vacancy_id,
                                    "hk_position_id": position.hk_position_id,
                            }
                        )

                # Search and insert tech matches in vacancy
                matches = re.findall(full_pattern, vacancy.message_text, re.IGNORECASE)
                for m in matches:
                    self.pg_connect.pg_operator(
                        log=self.logger,
                        path_to_script=self.INSERT_DDS_L_VACANCY_TECHNOLOGY_SCRIPT_PATH,
                        operator_mode="insert",
                        script_args={
                                "hk_vacancy_id": vacancy.hk_vacancy_id,
                                "hk_tech_id": tech_list[m.lower()],
                        }
                    )

            # Update wf_value in workflow settings
            wf_settings.wf_value = vacancy_list[len(vacancy_list) - 1].load_dt.isoformat(sep=" ", timespec="milliseconds")
            self.pg_connect.pg_operator(
                log=self.logger,
                path_to_script=self.INSERT_WF_SETTINGS_SCRIPT_PATH,
                operator_mode="insert",
                script_args={
                    "wf_table": wf_settings.wf_table,
                    "wf_key": wf_settings.wf_key,
                    "wf_value": wf_settings.wf_value
                }
            )

        else:
            self.logger.error(f"{datetime.utcnow()}: DDS VACANCY POSITION TECHNOLOGY PROCESSOR: FAILED: error in trying to get new batch")

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}: DDS VACANCY POSITION TECHNOLOGY PROCESSOR: FINISH")
