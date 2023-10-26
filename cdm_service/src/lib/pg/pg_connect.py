from contextlib import contextmanager
from typing import Generator
from pathlib import Path
from logging import Logger
from datetime import datetime
from typing import Type, Dict, Optional, Any
from pydantic import BaseModel

import psycopg
from psycopg import Connection
from psycopg.rows import class_row


class WfSettings(BaseModel):
    wf_id: int
    wf_table: str
    wf_key: str
    wf_value: str | None


class Chat(BaseModel):
    chat_id: int
    chat_type: str
    chat_name: str
    title: str
    description: str | None
    invite_link: str | None
    members_count: int
    is_verified: bool
    is_scam: bool
    is_fake: bool


class Message(BaseModel):
    message_id: int
    message_link: str
    from_chat: str
    sender_chat: str | None
    sender_user: str | None
    message_ts: datetime
    views_count: int
    forwards_count: int
    message_text: str
    attached_user: str | None
    attached_link: str | None
    attached_email: str | None
    attached_hashtags: str | None


def get_class_type(class_name: str) -> Type[WfSettings | Chat | Message]:
    match class_name:
        case "Chat":
            return Chat
        case "Message":
            return Message
        case "WfSettings":
            return WfSettings


class PgConnect:
    def __init__(self, host: str, port: int, db_name: str, user: str, pw: str, sslmode: str = "prefer") -> None:
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.pw = pw
        self.sslmode = sslmode

    def url(self) -> str:
        return """
            host={host}
            port={port}
            dbname={db_name}
            user={user}
            password={pw}
            target_session_attrs=read-write
            sslmode={sslmode}
        """.format(
            host=self.host,
            port=self.port,
            db_name=self.db_name,
            user=self.user,
            pw=self.pw,
            sslmode=self.sslmode)

    @contextmanager
    def connection(self) -> Generator[Connection, None, None]:
        conn = psycopg.connect(self.url())
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def pg_operator(
            self,
            log: Logger,
            path_to_script: str,
            operator_mode: str,
            selected_class: Optional[str] = None,
            script_args: Optional[Dict] = None
    ) -> Optional[Any]:
        script = Path(path_to_script).read_text()
        log.info(f"Prepared script file to execute: {path_to_script}")
        try:
            with self.connection() as conn:

                log.info("Postgres connection success")

                # If operator mode is "INSERT"
                if operator_mode == 'insert':
                    cur = conn.cursor()
                    if script_args is not None:
                        cur.execute(script, script_args)
                    else:
                        cur.execute(script)
                    log.info(f"Postgres: data has been uploaded successfully")
                    return True
                # If operator mode is "SELECT"
                elif operator_mode == 'select':
                    with conn.cursor(row_factory=class_row(get_class_type(selected_class))) as cur:
                        if script_args is not None:
                            cur.execute(script, script_args)
                        else:
                            cur.execute(script)
                        data = cur.fetchall()
                        cur.close()
                        log.info("Postgres operator: data has been downloaded successfully")
                        return data
                else:
                    log.error(f"Postgres operator: operator mode hasn't matched with any setup. Check the args")
                    return False
        except psycopg.DatabaseError as e:
            log.error(f"Postgres operator: ERROR: operator_mode: {operator_mode}")
            log.error(f"Postgres operator: selected_class: {selected_class}, script_args: {script_args}")
            log.error(f"Postgres operator: occurred database error: {e}")
            return False
