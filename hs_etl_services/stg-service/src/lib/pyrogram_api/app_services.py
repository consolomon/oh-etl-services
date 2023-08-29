import os
import json
import re
import logging
from datetime import datetime
from typing import List

from dotenv import load_dotenv
import pyrogram
from pyrogram import Client
import pandas as pd


class App:
    def __init__(self, targets: List, log: logging):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.log = log
        self.targets = targets
        self.df = None

    def extract_new_increment(self):

        dotenv_path = os.path.join(self.path + '/dot.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        API_HASH = os.environ['API_HASH']
        API_ID = os.environ['API_ID']

        all_messages = []
        try:
            with Client("oh_app", API_ID, API_HASH) as app:
                for target in self.targets:
                    for message in app.get_chat_history(target, limit=20):
                        all_messages.append(
                            [message.sender_chat, message.id, message.date, message.text, message.entities])

            df = pd.DataFrame(all_messages)
            df.columns = ["chat_json", "message_id", "date", "text", "entities"]
            self.df = df
            df.to_csv(f'{self.path}/oh_increment.csv', index=False)
            self.log.info('Download successful')
            self.log.info(f'Dataset path: {self.path}/oh_increment.csv')
            return self.path
        except Exception as e:
            self.log.error(f'Error: {e}')

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
