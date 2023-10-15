import re
from datetime import datetime
from logging import Logger
from lib.pg.pg_connect import PgConnect, WfSettings, Message


class DdsResumeVacancyProcessor:

    BATCH_LIMIT = 2000

    SELECT_STG_MESSAGES_SCRIPT_PATH = "/src/lib/sql/select_stg_messages.sql"
    SELECT_WF_SETTINGS_SCRIPT_PATH = "/src/lib/sql/select_wf_settings.sql"
    INSERT_WF_SETTINGS_SCRIPT_PATH = "/src/lib/sql/insert_wf_settings.sql"

    INSERT_DDS_H_RESUME_SCRIPT_PATH = "/src/lib/sql/insert_dds_h_resume.sql"
    INSERT_DDS_S_RESUME_INFO_SCRIPT_PATH = "/src/lib/sql/insert_dds_s_resume_info.sql"

    INSERT_DDS_H_VACANCY_SCRIPT_PATH = "/src/lib/sql/insert_dds_h_vacancy.sql"
    INSERT_DDS_S_VACANCY_INFO_SCRIPT_PATH = "/src/lib/sql/insert_dds_s_vacancy_info.sql"

    INSERT_DDS_H_NOT_MATCH_SCRIPT_PATH = "/src/lib/sql/insert_dds_h_not_match.sql"
    INSERT_DDS_S_NOT_MATCH_INFO_SCRIPT_PATH = "/src/lib/sql/insert_dds_s_not_match_info.sql"

    RESUME_PATTERN = r"#resume|#cv|my resume|my cv|looking[\s-]?for[\s-]?a[\s-]?job|open[\s-]?to[\s-]?work|about me:"
    RESUME_PATTERN_RUS = r"#резюме|моё резюме|ищу[\s-]?работу|о себе:"
    VACANCY_PATTERN = r"#jobs|vacancy|what you.*ll do|what we offer|we offer|requirement[s]?|responsibilit|what you.*ll need|we expect|nice to have|good to have|job description|we are looking for|company is looking for|our benefits|company:"
    VACANCY_PATTERN_RUS = r"вакансия|обязанности|чем.*заниматься|что нужно будет делать|мы ожидаем|будет плюсом|мы предлагаем|задачи|требования|мы ищем|компания:|условия:|наш кандидат|наши ожидания|компенсаци[я,и]?"
    WORK_EXP_PATTERN = r"experience\D+([\d+.]+)\s?(years?)|([\d+.]+)\s?(years?).* experience"
    GRADE_PATTERNS = [r"junior", r"middle", r"senior", r"lead"]
    WORK_FORMAT_PATTERNS = [r"full[\s-]?time", r"part[\s-]?time", r"remote", r"hybrid", r"office", r"freelance"]

    def __init__(
            self,
            logger: Logger,
            pg_connect: PgConnect
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect

    def run(self) -> None:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: DDS RESUME VACANCY PROCESSOR: START")

        # Get workflow settings for resume&vacancy tables
        wf_settings = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_WF_SETTINGS_SCRIPT_PATH,
            operator_mode="select",
            selected_class="WfSettings",
            script_args={
                "wf_table": "resume&vacancy",
                "wf_key": "stg.messages.message_ts"
            }
        )

        # Setup basic state in case of empty workflow settings
        if not wf_settings:
            wf_settings = WfSettings(
                wf_id=0,
                wf_table="resume&vacancy",
                wf_key="stg.messages.message_ts",
                wf_value=datetime.min.isoformat(sep=" ", timespec="milliseconds")
            )
        else:
            wf_settings = wf_settings[0]

        # Get a batch of a messages from stg.messages
        message_list = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_STG_MESSAGES_SCRIPT_PATH,
            operator_mode="select",
            selected_class="Message",
            script_args={
                "message_ts": wf_settings.wf_value,
                "batch_limit": self.BATCH_LIMIT
            }
        )
        # Process the ways when message list is filled, empty or missing
        if message_list is False or len(message_list) == 0:
            self.logger.warning(f"{datetime.utcnow()}: DDS RESUME VACANCY PROCESSOR: don't have new items to process")
        elif message_list is not False and len(message_list) > 0:

            # ETL processing from message into resume or vacancy
            self.logger.info(
                f"{datetime.utcnow()}: DDS RESUME VACANCY PROCESSOR: got new batch with {len(message_list)} items")

            for message in message_list:

                # Search matches for work experience, grade and work format
                work_experience = self.search_work_exp(message)
                grade = self.search_grade(message)
                work_format = self.search_work_format(message)

                # Split messages between resume and vacancy
                self.logger.warning(
                    f"{datetime.utcnow()}: DDS RESUME VACANCY PROCESSOR: is resume: {self.is_resume(message)}, is vacancy: {self.is_vacancy(message)}")
                if self.is_resume(message):

                    self.pg_connect.pg_operator(
                        log=self.logger,
                        path_to_script=self.INSERT_DDS_H_RESUME_SCRIPT_PATH,
                        operator_mode="insert",
                        script_args={
                                "chat_id": message.from_chat,
                                "message_id": message.message_id,
                        }
                    )

                    self.pg_connect.pg_operator(
                        log=self.logger,
                        path_to_script=self.INSERT_DDS_S_RESUME_INFO_SCRIPT_PATH,
                        operator_mode="insert",
                        script_args={
                                "chat_id": message.from_chat,
                                "message_id": message.message_id,
                                "message_link": message.message_link,
                                "sender_chat": message.sender_chat,
                                "sender_user": message.sender_user,
                                "message_ts": message.message_ts,
                                "views_count": message.views_count,
                                "forwards_count": message.forwards_count,
                                "message_text": message.message_text,
                                "attached_user": message.attached_user,
                                "attached_github": message.attached_github,
                                "attached_linkedin": message.attached_linkedin,
                                "attached_link": message.attached_link,
                                "attached_email": message.attached_email,
                                "attached_hashtags": message.attached_hashtags,
                                "work_experience": work_experience,
                                "grade": grade,
                                "work_format": work_format
                        }
                    )
                elif self.is_vacancy(message) is True:

                    self.pg_connect.pg_operator(
                        log=self.logger,
                        path_to_script=self.INSERT_DDS_H_VACANCY_SCRIPT_PATH,
                        operator_mode="insert",
                        script_args={
                                "chat_id": message.from_chat,
                                "message_id": message.message_id,
                        }
                    )

                    self.pg_connect.pg_operator(
                        log=self.logger,
                        path_to_script=self.INSERT_DDS_S_VACANCY_INFO_SCRIPT_PATH,
                        operator_mode="insert",
                        script_args={
                                "chat_id": message.from_chat,
                                "message_id": message.message_id,
                                "message_link": message.message_link,
                                "sender_chat": message.sender_chat,
                                "sender_user": message.sender_user,
                                "message_ts": message.message_ts,
                                "views_count": message.views_count,
                                "forwards_count": message.forwards_count,
                                "message_text": message.message_text,
                                "attached_user": message.attached_user,
                                "attached_link": message.attached_link,
                                "attached_email": message.attached_email,
                                "attached_hashtags": message.attached_hashtags,
                                "work_experience": work_experience,
                                "grade": grade,
                                "work_format": work_format
                        }
                    )
                else:

                    self.pg_connect.pg_operator(
                        log=self.logger,
                        path_to_script=self.INSERT_DDS_H_NOT_MATCH_SCRIPT_PATH,
                        operator_mode="insert",
                        script_args={
                                "chat_id": message.from_chat,
                                "message_id": message.message_id,
                        }
                    )

                    self.pg_connect.pg_operator(
                        log=self.logger,
                        path_to_script=self.INSERT_DDS_S_NOT_MATCH_INFO_SCRIPT_PATH,
                        operator_mode="insert",
                        script_args={
                                "chat_id": message.from_chat,
                                "message_id": message.message_id,
                                "message_link": message.message_link,
                                "sender_chat": message.sender_chat,
                                "sender_user": message.sender_user,
                                "message_ts": message.message_ts,
                                "views_count": message.views_count,
                                "forwards_count": message.forwards_count,
                                "message_text": message.message_text,
                                "attached_user": message.attached_user,
                                "attached_link": message.attached_link,
                                "attached_email": message.attached_email,
                                "attached_hashtags": message.attached_hashtags,
                                "work_experience": work_experience,
                                "grade": grade,
                                "work_format": work_format
                        }
                    )

                    self.logger.warning(
                        f"{datetime.utcnow()}: DDS RESUME VACANCY PROCESSOR: message didn't feet in vacancy and resume pattern")
                    self.logger.warning(
                        f"{datetime.utcnow()}: DDS RESUME VACANCY PROCESSOR: from_chat: {message.from_chat} message_id: {message.message_id}")

            # Update wf_value in workflow settings
            wf_settings.wf_value = message_list[len(message_list) - 1].message_ts.isoformat(sep=" ", timespec="milliseconds")
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
            self.logger.error(f"{datetime.utcnow()}: DDS RESUME VACANCY PROCESSOR: FAILED: error in trying to get new batch")

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}: DDS RESUME VACANCY PROCESSOR: FINISH")

    def is_resume(self, message: Message) -> bool:
        try:
            return (re.search(self.RESUME_PATTERN, message.message_text, re.IGNORECASE) is not None or
                    re.search(self.RESUME_PATTERN_RUS, message.message_text, re.IGNORECASE) is not None)
        except AttributeError:
            return False

    def is_vacancy(self, message: Message) -> bool:
        try:
            return (re.search(self.VACANCY_PATTERN, message.message_text, re.IGNORECASE) is not None or
                    re.search(self.VACANCY_PATTERN_RUS, message.message_text, re.IGNORECASE) is not None)
        except AttributeError:
            return False

    def search_work_exp(self, message: Message) -> str | None:

        match = re.search(self.WORK_EXP_PATTERN, message.message_text, re.IGNORECASE)
        if match:
            result = ""
            for m in match.groups():
                result += (m + " " if m else "")
            return result
        else:
            return None

    def search_grade(self, message: Message) -> str | None:
        result = ""
        for p in self.GRADE_PATTERNS:
            match = re.search(p, message.message_text, re.IGNORECASE)
            if match:
                result += (match.group() + ",")
        return result.removesuffix(",").lower() if len(result) > 0 else None

    def search_work_format(self, message: Message) -> str | None:
        result = ""
        for p in self.WORK_FORMAT_PATTERNS:
            match = re.search(p, message.message_text, re.IGNORECASE)
            if match:
                result += (match.group() + ",")
        return result.removesuffix(",").lower() if len(result) > 0 else None
