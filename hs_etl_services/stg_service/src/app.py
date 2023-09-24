import logging
import json
from json import JSONDecodeError
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

    # setup log level
    app.logger.setLevel(logging.DEBUG)

    # get chat name from request body
    chat_name = flask.request.form.get('chat_name')

    # return response message
    if chat_name is not None:

        # Insert chat name as item in file
        app.logger.info(f"API POST CHAT: post new chat {chat_name}")
        # Open the file with new chat names in read and update mode
        try:
            file = open(config.CHAT_NAME_FILE_PATH, 'r', encoding="utf-8")
            # Read the list in current state
            chat_name_list = list(json.load(file)['chat_name'])
            # Clean up the file
            file.close()
            file = open(config.CHAT_NAME_FILE_PATH, 'w', encoding="utf-8")
            # Add new chat name into the list and write in the file
            chat_name_list.append(chat_name)
            json.dump(obj={"chat_name": chat_name_list}, fp=file)

            app.logger.info(f"API POST CHAT: new chat {chat_name} sent successfully")
            app.logger.info(f"API POST CHAT: new chats count: {len(chat_name_list)}")
            app.logger.info(f"API POST CHAT: chat list: {str(chat_name_list)}")
            # Close updated file
            file.close()
        except FileNotFoundError:
            app.logger.warning(f"API POST CHAT: CHAT_NAME_FILE is not exists! Create a new one")
            file = open(config.CHAT_NAME_FILE_PATH, 'x', encoding="utf-8")
            json.dump(obj={"chat_name": []}, fp=file)
            file.close()

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

    # Setup log level
    app.logger.setLevel(logging.DEBUG)

    # Get chat name list from local file
    try:
        file = open(config.CHAT_NAME_FILE_PATH, 'r', encoding="utf-8")
        chat_name_list = json.load(file)['chat_name']
        file.close()
        # return chat_name_list in response body
        app.logger.info(f"API GET CHAT: post {len(chat_name_list)} new chat names in Pyrogram client")
        answer = flask.jsonify(
            chat_name=chat_name_list,
            message="success",
            statusCode=200
        )
        file = open(config.CHAT_NAME_FILE_PATH, 'w', encoding="utf-8")
        json.dump(obj={"chat_name": []}, fp=file)
        file.close()
        return answer
    except JSONDecodeError:
        # Return failed status in response body
        app.logger.info(f"API GET CHAT: chat_name is empty, send failed status in response")
        return flask.jsonify(
            chat_name=None,
            message="failed",
            statusCode=400
        )
    except FileNotFoundError:
        app.logger.warning(f"API POST CHAT: CHAT_NAME_FILE is not exists! Create a new one")
        file = open(config.CHAT_NAME_FILE_PATH, 'x', encoding="utf-8")
        json.dump(obj={"chat_name": []}, fp=file)
        file.close()
        return flask.jsonify(
            chat_name=None,
            message="failed",
            statusCode=400
        )


# API endpoint to post new position into database
# Available through GET-request by address: localhost:5011/api/get_chat
@app.post("/api/post_position")
def post_position():

    # Setup log level
    app.logger.setLevel(logging.DEBUG)

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

    # Setup log level
    app.logger.setLevel(logging.DEBUG)

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
