from datetime import datetime
from logging import Logger
from pyrogram import Client

from lib.pg.pg_connect import PgConnect, WfSettings
from lib.pyrogram_api.pyrogram_client import get_message_list


class StgMessageProcessor:

    BATCH_LIMIT = 100
    SELECT_STG_CHATS_SCRIPT_PATH = "/home/consolomon/PycharmProjects/HiringScanner/hs_etl_services/pyrogram_service/src/lib/sql/select_stg_chats.sql"
    INSERT_STG_MESSAGES_SCRIPT_PATH = "/home/consolomon/PycharmProjects/HiringScanner/hs_etl_services/pyrogram_service/src/lib/sql/insert_stg_messages.sql"
    SELECT_WF_SETTINGS_SCRIPT_PATH = "/home/consolomon/PycharmProjects/HiringScanner/hs_etl_services/pyrogram_service/src/lib/sql/select_wf_settings.sql"
    INSERT_WF_SETTINGS_SCRIPT_PATH = "/home/consolomon/PycharmProjects/HiringScanner/hs_etl_services/pyrogram_service/src/lib/sql/insert_wf_settings.sql"

    def __init__(
            self,
            logger: Logger,
            pg_connect: PgConnect,
            pyrogram_client: Client
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect
        self.pyrogram_client = pyrogram_client

    def run(self) -> None:

        # Log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: START")

        # Get chat name list from DDS layer in database
        chat_list = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_STG_CHATS_SCRIPT_PATH,
            operator_mode="select",
            selected_class="Chat"
        )
        chat_name_list = [x.chat_name for x in chat_list]

        # Loop of extracting messages from each chat in list
        for chat_name in chat_name_list:

            # Get workflow settings for this chat
            wf_settings = self.pg_connect.pg_operator(
                log=self.logger,
                path_to_script=self.SELECT_WF_SETTINGS_SCRIPT_PATH,
                operator_mode="select",
                selected_class="WfSettings",
                script_args={
                    "wf_table": "messages",
                    "wf_key": chat_name
                }
            )

            # Setup basic state in case of empty workflow settings
            if not wf_settings:
                wf_settings = WfSettings(
                    wf_id=0,
                    wf_table="messages",
                    wf_key=chat_name,
                    wf_value="0"
                )
            else:
                wf_settings = wf_settings[0]

            # Get new batch of messages
            message_list = get_message_list(
                client=self.pyrogram_client,
                chat_name=chat_name,
                limit=self.BATCH_LIMIT,
                offset_id=int(wf_settings.wf_value)
            )

            # Insert new batch of messages
            for message in message_list:
                result = self.pg_connect.pg_operator(
                    log=self.logger,
                    path_to_script=self.INSERT_STG_MESSAGES_SCRIPT_PATH,
                    operator_mode="insert",
                    script_args={
                        "message_id": message["message_id"],
                        "message_link": message["message_link"],
                        "from_chat": message["from_chat"],
                        "sender_chat": message["sender_chat"],
                        "sender_user": message["sender_user"],
                        "message_ts": message["message_ts"],
                        "views_count": message["views_count"],
                        "forwards_count": message["forwards_count"],
                        "message_text": message["message_text"],
                        "attached_user": message["attached_user"],
                        "attached_link": message["attached_user"],
                        "attached_email":  message["attached_email"],
                        "attached_hashtags":  message["attached_hashtags"]
                    }
                )

                # Log notification in case of message insert was failed
                if result is False:
                    self.logger.warning(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: unable to insert new message!")
                    self.logger.warning(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: message_id: {message['message_id']}")
                    self.logger.warning(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: message_link: {message['message_link']}")

                # Update workflow settings value
                if message["message_id"] > int(wf_settings.wf_value):
                    wf_settings.wf_value = message["message_id"]

            # Update workflow settings in database
            result = self.pg_connect.pg_operator(
                log=self.logger,
                path_to_script=self.INSERT_WF_SETTINGS_SCRIPT_PATH,
                operator_mode="insert",
                script_args={
                    "wf_table": wf_settings.wf_table,
                    "wf_key": wf_settings.wf_key,
                    "wf_value": str(wf_settings.wf_value)
                }
            )

        # Log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: FINISH")
