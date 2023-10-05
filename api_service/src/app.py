import logging
import flask
from apscheduler.schedulers.background import BackgroundScheduler

from app_config import AppConfig
from stg_loader.sample_job import SampleMessageProcessor

app = flask.Flask(__name__)
# Setup application config with environment variables and constants
config = AppConfig()
app.secret_key = config.FLASK_SECRET_KEY


# Endpoint to check service status
# Available through GET-request by address: localhost:5011/health.
@app.get('/health')
def health():
    return 'healthy'


# API endpoint to post chat_name into Pyrogram Client through local file
# Available through POST-request by address: localhost:5011/api/post_chat
# Parameter in request body: chat_name (str)
@app.post('/api/post_chat')
def post_chat():

    # get chat name from request body
    chat_name = flask.request.form.get('chat_name')

    # return response message
    if chat_name is not None:

        chat_name = chat_name.removeprefix("https://t.me/")
        app.logger.info(f"API POST CHAT: post new chat {chat_name}")

        redis = config.redis_client()
        chat_name_list = redis.get("chat_name")
        if chat_name_list is None:
            chat_name_list = []
        chat_name_list.append(chat_name)
        app.logger.info(f"API POST CHAT: new chats count: {len(chat_name_list)}")
        redis.set("chat_name", chat_name_list)

        return flask.jsonify(
            message="POST SUCCESS",
            statusCode=200
        )
    else:
        return flask.jsonify(
            message="POST FAILED",
            statusCode=400
        )


# API endpoint to get chat_name from Pyrogram Client
# Available through GET-request by address: localhost:5011/api/get_chat
@app.get('/api/get_chat')
def get_chat():

    try:
        redis = config.redis_client()
        chat_name_list = redis.get("chat_name")
        if len(chat_name_list) > 0:
            app.logger.info(f"API GET CHAT: get {len(chat_name_list)} new chat names in Pyrogram client")
            # Clear chat_name_list in redis
            redis.set("chat_name", [])
            # Return chat_name_list in response body
            return flask.jsonify(
                chat_name=chat_name_list,
                message="success",
                statusCode=200
            )
        else:
            app.logger.info("API GET CHAT: chat_name list is empty, send failed status in response")
            return flask.jsonify(
                chat_name=None,
                message="failed",
                statusCode=400
            )

    except Exception as e:
        app.logger.error(f"API POST CHAT: occurred error {e}")
        return flask.jsonify(
                chat_name=None,
                message="failed",
                statusCode=400
            )


# API endpoint to post new position into database
# Available through GET-request by address: localhost:5011/api/get_chat
@app.post("/api/post_position")
def post_position():

    # Get new values from request body
    position_name = flask.request.form.get("position_name")
    position_keywords = flask.request.form.get("position_keywords")

    if position_name is not None and position_keywords is not None:

        # Insert new position into database
        app.logger.info(f"API POST POSITION: post new position {position_name}")

        config.pg_warehouse_db().pg_operator(
            log=app.logger,
            path_to_script=config.INSERT_STG_POSITION_SCRIPT_PATH,
            operator_mode="insert",
            script_args={
                "position_name": position_name,
                "position_keywords": position_keywords
            }
        )
        return flask.jsonify(
            message="POST SUCCESS",
            statusCode=200
        )
    elif position_name is None:
        app.logger.error(f"API POST POSITION: ERROR: position name value is empty, check post request")
        return flask.jsonify(
            message="POST FAILED",
            statusCode=400
        )
    elif position_keywords is None:
        app.logger.error(f"API POST POSITION: ERROR: position keywords value is empty, check post request")
        return flask.jsonify(
            message="POST FAILED",
            statusCode=400
        )
    else:
        app.logger.error(f"API POST POSITION: ERROR: request body is empty, check post request")
        return flask.jsonify(
            message="POST FAILED",
            statusCode=400
        )


@app.post("/api/post_technology")
def post_technology():

    # Get new value from request body
    tech_name = flask.request.form.get("tech_name")

    if tech_name is not None:

        # Insert new position into database
        app.logger.info(f"API POST TECHNOLOGY: post new technology {tech_name}")

        config.pg_warehouse_db().pg_operator(
            log=app.logger,
            path_to_script=config.INSERT_STG_TECHNOLOGY_SCRIPT_PATH,
            operator_mode="insert",
            script_args={
                "tech_name": tech_name
            }
        )
        return flask.jsonify(
            message="POST SUCCESS",
            statusCode=200
        )
    else:
        app.logger.error(f"API POST TECHNOLOGY: ERROR: request body is empty, check post request")
        return flask.jsonify(
            message="POST FAILED",
            statusCode=400
        )


if __name__ == '__main__':

    # Setup log level
    app.logger.setLevel(logging.DEBUG)

    # Setup processor
    # proc = SampleMessageProcessor(app.logger)

    # Setup BackgroundScheduler to run processor by time schedule
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=proc.run, trigger="interval", seconds=config.DEFAULT_JOB_INTERVAL)
    # scheduler.start()

    # run Flask application
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
