import requests

from datetime import datetime
from logging import Logger
from pyrogram import Client
from typing import List

# from lib.pg.pg_connect import PgConnect
from hs_etl_services.pyrogram_service.src.lib.pg.pg_connect import PgConnect
from hs_etl_services.pyrogram_service.src.lib.pyrogram_api.pyrogram_client import get_chat


class StgChatProcessor:
    GET_CHAT_NAME_URL = "http://localhost:5011/api/get_chat"
    SELECT_STG_CHATS_SCRIPT_PATH = "/home/consolomon/PycharmProjects/HiringScanner/hs_etl_services/pyrogram_service/src/lib/sql/select_stg_chats.sql"
    INSERT_STG_CHATS_SCRIPT_PATH = "/home/consolomon/PycharmProjects/HiringScanner/hs_etl_services/pyrogram_service/src/lib/sql/insert_stg_chats.sql"

    def __init__(
            self,
            logger: Logger,
            pg_connect: PgConnect,
            pyrogram_client: Client,
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect
        self.pyrogram_client = pyrogram_client

    def run(self):

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: STG CHAT PROCESSOR: START")

        old_chat_list = self.pg_connect.pg_operator(
            log=self.logger,
            path_to_script=self.SELECT_STG_CHATS_SCRIPT_PATH,
            operator_mode="select",
            selected_class="Chat"
        )
        chat_name_list = [x.chat_name for x in old_chat_list]

        # Try to get new chat name through HTTP request
        response = requests.get(self.GET_CHAT_NAME_URL).json()
        self.logger.info(f"{datetime.utcnow()}: STG CHAT PROCESSOR: try to get new chat name from API")
        if response['chat_name'] is not None:

            # get new chat object
            chat_name = response['chat_name']
            if isinstance(chat_name, str):

                # If there is only one chat
                self.logger.info(f"{datetime.utcnow()}: STG CHAT PROCESSOR: get new chat name: {chat_name}")
                chat = get_chat(self.pyrogram_client, chat_name)
                if chat is not None:
                    self.logger.info(
                        f"{datetime.utcnow()}: STG CHAT PROCESSOR: SUCCESS: new chat is found: {chat_name}")
                    chat_name_list.append(chat_name)
                else:
                    self.logger.error(
                        f"{datetime.utcnow()}: STG CHAT PROCESSOR: FAILED: new chat not found or not available")

            elif isinstance(chat_name, List):

                # If there are many chats in list
                for chat_item in chat_name:
                    self.logger.info(f"{datetime.utcnow()}: STG CHAT PROCESSOR: get new chat name: {chat_item}")
                    chat = get_chat(self.pyrogram_client, chat_item)
                    if chat is not None:
                        self.logger.info(
                            f"{datetime.utcnow()}: STG CHAT PROCESSOR: SUCCESS: new chat is found: {chat_item}")
                        chat_name_list.append(chat_item)
                    else:
                        self.logger.error(
                            f"{datetime.utcnow()}: STG CHAT PROCESSOR: FAILED: new chat not found or not available")
            else:
                self.logger.error(
                    f"{datetime.utcnow()}: STG CHAT PROCESSOR: FAILED: new chat not found or not available")
        else:
            self.logger.warning(f"{datetime.utcnow()}: STG CHAT PROCESSOR: FAILED: haven't got new chat")

        # upsert for all chats
        # insert or update chat in stg layer of the database
        for chat_name in chat_name_list:
            chat = get_chat(self.pyrogram_client, chat_name)
            if chat is None:
                self.logger.warning(
                    f"{datetime.utcnow()}: STG CHAT PROCESSOR: FAILED: chat {chat_name} not found or not available")
            else:
                self.logger.info(
                    f"{datetime.utcnow()}: STG CHAT PROCESSOR: CHAT_ID VALUE: {chat['chat_id']}")
                result = self.pg_connect.pg_operator(
                    log=self.logger,
                    path_to_script=self.INSERT_STG_CHATS_SCRIPT_PATH,
                    operator_mode="insert",
                    script_args={
                        "chat_id": chat['chat_id'],
                        "chat_type": chat['chat_type'],
                        "chat_name": chat['chat_name'],
                        "title": chat['chat_title'],
                        "description": chat['description'],
                        "invite_link": chat['invite_link'],
                        "members_count": chat['members_count'],
                        "is_verified": chat['is_verified'],
                        "is_scam": chat['is_scam'],
                        "is_fake": chat['is_fake']
                    }
                )
                if result is not True:
                    self.logger.warning(
                        f"{datetime.utcnow()}: STG CHAT PROCESSOR: postgres: failed to upload chat {chat_name} in database")

        # log notification about finish of the job
        self.logger.info(f"{datetime.utcnow()}: STG CHAT PROCESSOR: FINISH")
