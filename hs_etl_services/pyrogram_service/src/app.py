import logging
import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app_config import AppConfig, pyrogram_client
from stg_loader.stg_chat_processor import StgChatProcessor
from stg_loader.stg_message_processor import StgMessageProcessor


app = pyrogram_client()


def main():

    # Setup service config, pyrogram client and logger
    config = AppConfig()
    app_logger = logging.getLogger("PYROGRAM CLIENT")
    app_logger.setLevel(logging.DEBUG)

    # Setup chat and message processors

    chat_proc = StgChatProcessor(app_logger, config.pg_warehouse_db(), app)
    message_proc = StgMessageProcessor(app_logger, config.pg_warehouse_db(), app)

    while True:
        chat_proc.run()
        print(f"{datetime.utcnow()}: STG CHAT PROCESSOR: FINISHED")
        message_proc.run()
        print(f"{datetime.utcnow()}: STG MESSAGE PROCESSOR: FINISHED")
        time.sleep(config.DEFAULT_JOB_INTERVAL)
        print(f"{datetime.utcnow()}: RESTARTING CYCLE")

    # Setup Background Scheduler
    # scheduler = BackgroundScheduler()
    # Setup job function and schedule config
    # scheduler.add_job(func=proc.run, trigger="interval", seconds=config.DEFAULT_JOB_INTERVAL)

    # Launch application
    # scheduler.start()


if __name__ == '__main__':
    main()
