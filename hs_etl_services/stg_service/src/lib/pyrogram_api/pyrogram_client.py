import json
import re
import logging
from datetime import datetime
from contextlib import contextmanager
from typing import Generator, List

from pyrogram import Client
from pyrogram_objects import Chat, Message


class PyrogramClient:
    def __init__(self, api_id: int, api_hash: str):
        self.api_id = api_id,
        self.api_hash = api_hash

    @contextmanager
    def get_client(self) -> Generator[Client, None, None]:
        client = Client("hs_app", self.api_id, self.api_hash)
        try:
            yield client
        except Exception as e:
            client.stop()
            raise e
        finally:
            client.stop()

    def get_chat(self, chat_name: str) -> Chat:
        try:
            with self.get_client() as client:
                chat = client.get_chat(chat_name)
                return Chat(
                    chat.id,
                    str(chat.type),
                    chat.title,
                    chat.description,
                    chat.invite_link,
                    chat.members_count,
                    chat.is_verified,
                    chat.is_scam,
                    chat.is_fake
                )
        except Exception as e:
            raise e

    def get_message_list(self, chat_list: List[str], offset_id: int, limit: int) -> list[Message]:
        message_list = []
        try:
            with self.get_client() as client:
                for chat_name in chat_list:
                    for message in client.get_chat_history(chat_name, limit=limit, offset_id=offset_id):
                        message_list.append(
                            Message(
                                message.id,
                                message.link,
                                (json.loads(message.sender_chat)['id'] if message.sender_chat is not None else None),
                                (json.loads(message.from_user)['id'] if message.from_user is not None else None),
                                message.date,
                                message.views,
                                message.forwards,
                                message.text
                            )
                        )
        except Exception as e:
            raise e
        finally:
            return message_list

"""
    def transform_new_increment(self, keywords):
        try:
            jobs_df = pd.read_csv('../../../../../oh_increment.csv')
            jobs_df["chat_id"] = jobs_df["chat_json"].apply(lambda x: json.loads(x)['id'])
            jobs_df["chat_title"] = jobs_df["chat_json"].apply(lambda x: json.loads(x)['title'])
            jobs_df["matched"] = jobs_df["text"].apply(lambda x: True if re.search(keywords, str(x).lower()) else False)
            jobs_df["hidden_links"] = jobs_df.apply(get_links, axis=1)
            print(jobs_df[jobs_df["matched"]])
        except Exception as e:
            self.log.error(f'Error: {e}')


def get_links(x, regexp='http\S+'):
    try:
        entities = json.loads(str(x['entities']))
        for i in entities:
            print(f"type class: {type(i['type'])}, type value: {i['type']}")
            if i['type'] == "MessageEntityType.TEXT_LINK":
                print(i['url'])
                return i['url']
            elif i['type'] == "MessageEntityType.URL":
                url = re.findall(regexp, x['text'])[0]
                return url
            else:
                return None
    except json.JSONDecodeError:
        return None
"""
