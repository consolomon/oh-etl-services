import logging
import flask
from apscheduler.schedulers.background import BackgroundScheduler

from app_config import AppConfig
from cdm_loader.webserver_update_processor import WebserverUpdateProcessor


app = flask.Flask(__name__)
# Setup application config with environment variables and constants
config = AppConfig()
app.secret_key = config.FLASK_SECRET_KEY


if __name__ == '__main__':

    # Setup log level
    app.logger.setLevel(logging.DEBUG)

    # Setup processor
    proc = WebserverUpdateProcessor(app.logger, config)

    # Setup BackgroundScheduler to run processor by time schedule
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=proc.run, trigger="cron", hour="0,4,8,12,16,20")
    scheduler.start()

    # run Flask application
    app.run(debug=True, host='0.0.0.0', port=5012, use_reloader=False)
