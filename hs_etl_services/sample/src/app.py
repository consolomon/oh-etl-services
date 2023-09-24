import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app_config import AppConfig
from sample_app.sample_job import SampleMessageProcessor

app = Flask(__name__)


# Endpoint to check service status
# Available through GET-request by address: localhost:5011/health.
@app.get('/health')
def health():
    return 'healthy'


if __name__ == '__main__':

    # Setup log level
    app.logger.setLevel(logging.DEBUG)

    # Setup application config
    config = AppConfig()

    # Setup processor
    proc = SampleMessageProcessor(app.logger)

    # Setup BackgroundScheduler to run processor by time schedule
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=proc.run, trigger="interval", seconds=config.DEFAULT_JOB_INTERVAL)
    scheduler.start()

    # run Flask application
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
