import re
from datetime import datetime
from typing import Optional, List, Dict

from pyrogram import Client
from pyrogram.enums.message_entity_type import MessageEntityType


def get_chat(client: Client, chat_name: str) -> Dict:
    try:
        chat = client.get_chat(chat_name)
        return {
            "chat_id": chat.id,
            "chat_type": str(chat.type).removeprefix("ChatType."),
            "chat_name": chat.username,
            "chat_title": chat.title,
            "description": chat.description,
            "invite_link": chat.invite_link,
            "members_count": chat.members_count,
            "is_verified": chat.is_verified,
            "is_scam": chat.is_scam,
            "is_fake": chat.is_fake
        }
    except Exception as e:
        raise e


def get_message_list(client: Client, chat_name: str, limit: int, offset_id: int) -> List[Dict]:
    message_list = []
    print(f"STG MESSAGE PROCESSOR: chat_name: {chat_name}, offset_id: {offset_id}, limit: {limit}")
    try:
        for message in client.search_messages(chat_id=chat_name, limit=limit):
            if offset_id != 0 and message.id <= offset_id:
                print(f"STG MESSAGE PROCESSOR: chat_name {chat_name}: LAST uploaded message_id: {message.id}, message_ts: {message.date}")
                break

            attached_user = None
            attached_linkedin = None
            attached_github = None
            attached_link = None
            attached_email = None
            attached_hashtags = None

            entities = message.entities if message.entities is not None else message.caption_entities
            text = message.text if message.text is not None else message.caption
            if entities is not None:
                for entity in entities:
                    match entity.type:
                        case MessageEntityType.MENTION:

                            attached_user = text[entity.offset: entity.offset + entity.length]

                        case MessageEntityType.TEXT_LINK:

                            match = re.search(r"(github)\.com/.+|(linkedin)\.com/.+", entity.url)
                            if match is not None and match.group(1) == "github":
                                attached_github = entity.url
                            elif match is not None and match.group(2) == "linkedin":
                                attached_linkedin = entity.url
                            elif entity.url.__contains__("@") is False:
                                attached_link = entity.url

                        case MessageEntityType.URL:

                            url = text[entity.offset: entity.offset + entity.length]
                            match = re.search(r"(github)\.com/.+|(linkedin)\.com/.+", url)
                            if match is not None and match.group(1) == "github":
                                attached_github = url
                            elif match is not None and match.group(2) == "linkedin":
                                attached_linkedin = url
                            elif entity.url.__contains__("@") is False:
                                attached_link = entity.url

                        case MessageEntityType.EMAIL:

                            attached_email = text[entity.offset: entity.offset + entity.length]

                        case MessageEntityType.HASHTAG:

                            attached_hashtags = str(attached_hashtags) + "," + text[entity.offset: entity.offset + entity.length]

            if attached_hashtags is not None:
                attached_hashtags = attached_hashtags.removeprefix("None,")

            message_list.append(
                {
                    "message_id": message.id,
                    "message_link": message.link,
                    "from_chat": message.chat.id,
                    "sender_chat": (None if message.sender_chat is None else message.sender_chat.id),
                    "sender_user": (None if message.from_user is None else message.from_user.id),
                    "message_ts": message.date,
                    "views_count": message.views,
                    "forwards_count": message.forwards,
                    "message_text": (message.text if message.text is not None else message.caption),
                    "attached_user": attached_user,
                    "attached_github": attached_github,
                    "attached_linkedin": attached_linkedin,
                    "attached_link": attached_link,
                    "attached_email": attached_email,
                    "attached_hashtags": attached_hashtags
                }
            )
    except Exception as e:
        raise e
    finally:
        return message_list
