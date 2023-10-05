import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app_config import AppConfig
from dds_loader.dds_chat_processor import DdsChatProcessor
from dds_loader.dds_position_processor import DdsPositionProcessor
from dds_loader.dds_technology_processor import DdsTechnologyProcessor
from dds_loader.dds_resume_vacancy_proccesor import DdsResumeVacancyProcessor
from dds_loader.dds_vacancy_position_technology_processor import DdsVacancyPositionTechnologyProcessor
from dds_loader.dds_resume_position_technology_processor import DdsResumePositionTechnologyProcessor
from dds_loader.dds_position_technology_processor import DdsPositionTechnologyProcessor

app = Flask(__name__)


# Endpoint to check service status
# Available through GET-request by address: localhost:5012/health.
@app.get('/health')
def health():
    return 'healthy'


if __name__ == '__main__':

    # Setup log level
    app.logger.setLevel(logging.WARNING)

    # Setup application config
    config = AppConfig()

    # Setup processors
    chat_proc = DdsChatProcessor(app.logger, config.pg_warehouse_db())
    position_proc = DdsPositionProcessor(app.logger, config.pg_warehouse_db())
    tech_proc = DdsTechnologyProcessor(app.logger, config.pg_warehouse_db())
    resume_vacancy_proc = DdsResumeVacancyProcessor(app.logger, config.pg_warehouse_db())
    vacancy_position_tech_proc = DdsVacancyPositionTechnologyProcessor(app.logger, config.pg_warehouse_db())
    resume_position_tech_proc = DdsResumePositionTechnologyProcessor(app.logger, config.pg_warehouse_db())
    position_tech_proc = DdsPositionTechnologyProcessor(app.logger, config.pg_warehouse_db())

    # Init processors
    chat_proc.run()
    position_proc.run()
    tech_proc.run()

    # Setup BackgroundScheduler to run processor by time schedule
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=chat_proc.run, trigger="cron", hour="0,8,16", minute="0")
    scheduler.add_job(func=position_proc.run, trigger="cron", hour="0,8,16", minute="0")
    scheduler.add_job(func=tech_proc.run, trigger="cron", hour="0,8,16", minute="0")
    scheduler.add_job(func=resume_vacancy_proc.run, trigger="cron", minute="10")
    scheduler.add_job(func=vacancy_position_tech_proc.run, trigger="cron", minute="20-40/10")
    scheduler.add_job(func=resume_position_tech_proc.run, trigger="cron", minute="20-40/10")
    scheduler.add_job(func=position_tech_proc.run, trigger="cron", minute="50")
    scheduler.start()

    # run Flask application
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
