from datetime import datetime
from logging import Logger
from hs_etl_services.stg_service.src.lib.pg.pg_connect import PgConnect
from hs_etl_services.stg_service.src.lib.pyrogram_api.pyrogram_client import PyrogramClient


class StgChatProcessor:
    def __init__(
            self,
            logger: Logger,
            pg_connect: PgConnect,
            pyrogram_client: PyrogramClient,
            chat_name: str
    ) -> None:
        self.logger = logger
        self.pg_connect = pg_connect
        self.pyrogram_client = pyrogram_client
        self.chat_name = chat_name

    def run(self) -> bool:

        # log notification about start of the job
        self.logger.info(f"{datetime.utcnow()}: STG CHAT PROCESSOR: START")

        # setup connection with telegram
        with self.pyrogram_client.get_client() as pyrogram:

            # get new chat object
            chat = pyrogram.get_chat(self.chat_name)

            # insert or update chat in stg layer of the database
            if chat is not None:
                self.logger.info(f"{datetime.utcnow()}: STG CHAT PROCESSOR: get chat {self.chat_name}")
                with self.pg_connect.connection() as pg_conn:
                    cur = pg_conn.cursor()
                    cur.execute(
                        """
                        INSERT INTO stg.chats (
                            chat_id,
                            chat_type,
                            title,
                            description,
                            invite_link,
                            members_count,
                            restrictions_list,
                            is_verified,
                            is_scum,
                            is_fake
                        )
                        VALUES (
                            %(chat_id)s,
                            %(chat_type)s,
                            %(title)s,
                            %(description)s,
                            %(invite_link)s,
                            %(members_count)s,
                            %(restrictions_list)s,
                            %(is_verified)s,
                            %(is_scum)s,
                            %(is_fake)s,
                        )
                        ON CONFLICT (chat_id) DO UPDATE
                        SET
                            chat_type = EXCLUDED.chat_type,
                            title = EXCLUDED.title,
                            description = EXCLUDED.description,
                            invite_link = EXCLUDED.invite_link,
                            members_count = EXCLUDED.members_count,
                            restrictions_list = EXCLUDED.restrictions_list,
                            is_verified = EXCLUDED.is_verified,
                            is_scum = EXCLUDED.is_scum,
                            is_fake = EXCLUDED.is_fake
                        """,
                        {
                            "chat_id": chat.chat_id,
                            "chat_type": chat.chat_type,
                            "title": chat.chat_type,
                            "description": chat.description,
                            "invite_link": chat.invite_link,
                            "members_count": chat.members_count,
                            "restrictions_list": chat.restrictions_list,
                            "is_verified": chat.is_verified,
                            "is_scum": chat.is_scam,
                            "is_fake": chat.is_fake
                        }
                    )
                    self.logger.info(f"{datetime.utcnow()}: STG CHAT PROCESSOR: SUCCESS: chat {self.chat_name} insert or update")

                    # log notification about finish of the job
                    self.logger.info(f"{datetime.utcnow()}: FINISH")
                    return True
            else:
                self.logger.error(f"{datetime.utcnow()}: STG CHAT PROCESSOR: FAILED: chat {self.chat_name} not found or not available")
            # log notification about finish of the job
            self.logger.info(f"{datetime.utcnow()}: FINISH")
            return False


