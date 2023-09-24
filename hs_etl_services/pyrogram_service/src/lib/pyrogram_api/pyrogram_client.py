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
    try:
        for message in client.get_chat_history(chat_name, limit=limit):
            if offset_id != 0 and message.id <= offset_id:
                print(f"STG MESSAGE PROCESSOR: chat_name {chat_name}: last uploaded message_id: {message.id}")
                break
            print(f"STG MESSAGE PROCESSOR: chat_name {chat_name}: uploaded message_id: {message.id}, message_ts: {message.date}")
            attached_user = None
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
                            attached_link = entity.url
                        case MessageEntityType.URL:
                            attached_link = text[entity.offset: entity.offset + entity.length]
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
                    "attached_link": attached_link,
                    "attached_email": attached_email,
                    "attached_hashtags": attached_hashtags
                }
            )
    except Exception as e:
        raise e
    finally:
        return message_list
