import re
from datetime import datetime
from logging import Logger
from lib.pg.pg_connect import PgConnect, WfSettings


class DdsResumePositionTechnologyProcessor:
    BATCH_LIMIT = 1500

    SELECT_WF_SETTINGS_SCRIPT_PATH = "/src/lib/sql/select_wf_settings.sql"
    INSERT_WF_SETTINGS_SCRIPT_PATH = "/src/lib/sql/insert_wf_settings.sql"

    SELECT_DDS_RESUMES_SCRIPT_PATH = "/src/lib/sql/select_dds_resumes.sql"
    SELECT_DDS_POSITIONS_SCRIPT_PATH = "/src/lib/sql/select_dds_positions.sql"
    SELECT_DDS_TECHNOLOGIES_SCRIPT_PATH = "/src/lib/sql/select_dds_technologies.sql"

    INSERT_DDS_L_RESUME_POSITION_SCRIPT_PATH = "/src/lib/sql/insert_dds_l_resume_position.sql"
    INSERT_DDS_L_RESUME_TECHNOLOGY_SCRIPT_PATH = "/src/lib/sql/insert_dds_l_resume_technology.sql"

    def __init__(
            self,
            logger: Logger,
            pg_connect: PgConnect
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect

    def run(self) -> None:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: START")

        # Get workflow settings for l_resume_position table
        wf_settings = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_WF_SETTINGS_SCRIPT_PATH,
            operator_mode="select",
            selected_class="WfSettings",
            script_args={
                "wf_table": "l_resume_position&l_resume_technology",
                "wf_key": "h_resume.load_dt"
            }
        )

        # Setup basic state in case of empty workflow settings
        if not wf_settings:
            wf_settings = WfSettings(
                wf_id=0,
                wf_table="l_resume_position&l_resume_technology",
                wf_key="h_resume.load_dt",
                wf_value=datetime.min.isoformat(sep=" ", timespec="milliseconds")
            )
        else:
            wf_settings = wf_settings[0]

        self.logger.info(f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: OLD l_resume_position&l_resume_technology wf_settings:")
        self.logger.info(f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: OLD wf_key: {wf_settings.wf_key}, wf_value: {wf_settings.wf_value}")

        # Get a batch of a messages from stg.messages
        resume_list = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_DDS_RESUMES_SCRIPT_PATH,
            operator_mode="select",
            selected_class="ResumeText",
            script_args={
                "load_dt": wf_settings.wf_value,
                "batch_limit": self.BATCH_LIMIT
            }
        )

        # Process the ways when resume list is filled, empty or missing
        if resume_list is False or len(resume_list) == 0:
            self.logger.info(
                f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: don't have new items to process")
        elif resume_list is not False and len(resume_list) > 0:

            # ETL processing matches between positions and resumes
            self.logger.info(
                f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: got new batch with {len(resume_list)} items")

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
            full_pattern = full_pattern.removesuffix("|").replace("+", "\+").replace(".", "\.")

            for resume in resume_list:

                # Search and insert position matches in resume
                for position in positions_list:
                    match = re.search(rf"{position.position_keywords}", resume.message_text, re.IGNORECASE)
                    if match:
                        self.pg_connect.pg_operator(
                            log=self.logger,
                            path_to_script=self.INSERT_DDS_L_RESUME_POSITION_SCRIPT_PATH,
                            operator_mode="insert",
                            script_args={
                                "hk_resume_id": resume.hk_resume_id,
                                "hk_position_id": position.hk_position_id,
                            }
                        )

                # Search and insert tech matches in resume
                matches = re.findall(full_pattern, resume.message_text, re.IGNORECASE)
                for m in matches:
                    self.pg_connect.pg_operator(
                        log=self.logger,
                        path_to_script=self.INSERT_DDS_L_RESUME_TECHNOLOGY_SCRIPT_PATH,
                        operator_mode="insert",
                        script_args={
                            "hk_resume_id": resume.hk_resume_id,
                            "hk_tech_id": tech_dict[m.lower()],
                        }
                    )
                    # Set wf_value as max load_dt in vacancy list
                    if resume.load_dt > datetime.fromisoformat(wf_settings.wf_value):
                        wf_settings.wf_value = resume.load_dt.isoformat(sep=" ", timespec="milliseconds")

            self.logger.info(f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: NEW l_resume_position&l_resume_technology wf_settings:")
            self.logger.info(f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: NEW wf_key: {wf_settings.wf_key}, wf_value: {wf_settings.wf_value}")

            # Update wf_value in workflow settings
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
            self.logger.error(
                f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: FAILED: error in trying to get new batch")

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}: DDS RESUME POSITION TECHNOLOGY PROCESSOR: FINISH")
