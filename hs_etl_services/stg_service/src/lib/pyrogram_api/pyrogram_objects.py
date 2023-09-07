from datetime import datetime


class Chat:
    def __init__(
            self,
            chat_id: int,
            chat_type: str,
            title: str,
            description: str,
            invite_link: str,
            members_count: int,
            is_verified: bool,
            is_scam: bool,
            is_fake: bool
    ) -> None:
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.title = title
        self.description = description
        self.invite_link = invite_link
        self.members_count = members_count
        self.is_verified = is_verified
        self.is_scam = is_scam
        self.is_fake = is_fake


class Message:
    def __init__(
            self,
            message_id: int,
            message_link: str,
            from_chat: str,
            from_user: str,
            message_ts: datetime,
            views_count: int,
            forwards_count: int,
            message_text: str
    ) -> None:
        self.message_id = message_id
        self.message_link = message_link
        self.from_chat = from_chat
        self.from_user = from_user
        self.message_ts = message_ts
        self.views_count = views_count
        self.forwards_count = forwards_count
        self.message_text = message_text

