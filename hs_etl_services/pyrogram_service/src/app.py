import logging
import time
from datetime import datetime

from app_config import AppConfig
from stg_loader.stg_chat_processor import StgChatProcessor
from stg_loader.stg_message_processor import StgMessageProcessor

config = AppConfig()
app = config.pyrogram_client()


def main():

    # Setup logger
    app_logger = logging.getLogger("PYROGRAM CLIENT")

    # Setup processors

    chat_proc = StgChatProcessor(app_logger, config.pg_warehouse_db(), app)
    message_proc = StgMessageProcessor(app_logger, config.pg_warehouse_db(), app)

    # Init processors
    chat_proc.run()
    print(f"{datetime.utcnow()}: STG CHAT PROCESSOR: INIT COMPLETED")
    message_proc.run()
    print(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: INIT COMPLETED")
    print(f"{datetime.utcnow()}: PYROGRAM CLIENT: START SCHEDULE LOOP")
    while True:

        if datetime.utcnow().hour % 8 == 0:
            print(f"{datetime.utcnow()}: STG CHAT PROCESSOR: START")
            chat_proc.run()
            print(f"{datetime.utcnow()}: STG CHAT PROCESSOR: FINISHED")

        print(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: START")
        message_proc.run()
        print(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: FINISHED")
        time.sleep(config.DEFAULT_JOB_INTERVAL)


if __name__ == '__main__':
    main()
