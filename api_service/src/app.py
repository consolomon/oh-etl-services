import logging
import flask
from apscheduler.schedulers.background import BackgroundScheduler

from app_config import AppConfig
from lib.api import security, users

app = flask.Flask(__name__)
# Setup application config with environment variables and constants
config = AppConfig()
app.secret_key = config.FLASK_SECRET_KEY


@app.get('/health')
def health():
    """
    Endpoint to check service status
    Method: GET
    Address: localhost:5010/health.
    :return: "healthy"
    """
    return 'healthy'


@app.post('/api/post_chat')
@security.key_required
def post_chat():
    """
    API endpoint to post chat_name into Pyrogram Client through Redis
    Method: POST
    Address: localhost:5010/api/post_chat
    Required parameters:
        form: chat_name: str
        header: {"x-api-user":"user_name", "x-api-key": "user_key"}
    """

    # get chat name from request body
    chat_name = flask.request.form.get('chat_name')

    # return response message
    if chat_name is not None:

        chat_name = chat_name.removeprefix("https://t.me/")
        app.logger.info(f"API POST CHAT: post new chat {chat_name}")

        redis = config.redis_client()
        chat_name_list = redis.get("chat_name")
        chat_name_archive = redis.get("chat_name_archive")
        if chat_name_list is None:
            chat_name_list = []
        if chat_name_archive is None:
            chat_name_archive = []
        chat_name_list.append(chat_name)
        chat_name_archive.append(chat_name)
        app.logger.info(f"API POST CHAT: new chats count: {len(chat_name_list)}")
        app.logger.info(f"API POST CHAT: total chats count in archive: {len(chat_name_archive)}")
        redis.set("chat_name", chat_name_list)
        redis.set("chat_name_archive", chat_name_archive)

        return flask.jsonify(
            message="POST SUCCESS",
            statusCode=200
        )
    else:
        return flask.jsonify(
            message="POST FAILED",
            statusCode=400
        )


@app.get('/api/get_chat')
@security.key_required
def get_chat():
    """
    API endpoint to get chat_name from Redis to Pyrogram Client
    Method: GET
    Address: localhost:5010/api/get_chat
    Required parameters:
        header: {"x-api-user":"user_name", "x-api-key": "user_key"}
    :return: List[str]
    """

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
                statusCode=410
            )


@app.get('/api/admin/get_chat_archive')
@security.admin_required
def get_chat_archive():
    """
    API endpoint to get chat_name archive from Redis
    Method: GET
    Address: localhost:5010/api/admin/get_chat_archive
    Required parameters:
        header: {"x-api-user":"user_name", "x-api-key": "user_key"}
    :return: List[str]
    """

    try:
        redis = config.redis_client()
        chat_name_archive = redis.get("chat_name_archive")
        if len(chat_name_archive) > 0:
            app.logger.info(f"API GET CHAT ARCHIVE: get {len(chat_name_archive)} chat names from archive")
            # Return chat_name_list in response body
            return flask.jsonify(
                chat_name=chat_name_archive,
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
                statusCode=410
            )


@app.post("/api/post_position")
@security.key_required
def post_position():
    """
    API endpoint to insert position into database
    Method: POST
    Address: localhost:5010/api/post_position
    Required parameters:
        form: position_name: str, position_keywords: str
        header: {"x-api-user":"user_name", "x-api-key": "user_key"}
    """

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
            statusCode=411
        )
    elif position_keywords is None:
        app.logger.error(f"API POST POSITION: ERROR: position keywords value is empty, check post request")
        return flask.jsonify(
            message="POST FAILED",
            statusCode=412
        )
    else:
        app.logger.error(f"API POST POSITION: ERROR: request body is empty, check post request")
        return flask.jsonify(
            message="POST FAILED",
            statusCode=400
        )


@app.post("/api/post_technology")
@security.key_required
def post_technology():
    """
    API endpoint to insert technology into database
    Method: POST
    Address: localhost:5010/api/post_technology
    Required parameters:
        form: tech_name: str
        header: {"x-api-user":"user_name", "x-api-key": "user_key"}
    """

    # Get new value from request body
    tech_name = flask.request.form.get("tech_name")

    if tech_name is not None:

        # Insert new technology into database
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
        app.logger.error("API POST TECHNOLOGY: ERROR: request body is empty, check post request")
        return flask.jsonify(
            message="POST FAILED",
            statusCode=400
        )


@app.post("/api/admin/set_user")
@security.admin_required
def set_user():

    # Get new values from request body
    user_name = flask.request.form.get("user_name")

    if user_name is not None:

        user_key = security.create_api_key(user_name)
        user_level = flask.request.form.get("user_level", "basic")
        user = {
            "user_name": user_name,
            "user_key": user_key,
            "user_level": user_level
        }
        users.set_user(user, config.API_ADMIN_KEY, config.redis_client())
        return flask.jsonify(
            new_user=user,
            message="SET USER SUCCESS",
            statusCode=200
        )
    else:
        app.logger.error("API ADMIN SET USER: ERROR: request body is empty, check post request")
        return flask.jsonify(
            message="SET USER FAILED",
            statusCode=400
        )


@app.post("/api/admin/get_user")
@security.admin_required
def get_user():

    # Get new values from request body
    user_name = flask.request.form.get("user_name")

    if user_name is not None:

        user = users.get_user(user_name, config.API_ADMIN_KEY, config.redis_client())
        if user is not None:
            return flask.jsonify(
                user=user,
                message="GET USER SUCCESS",
                statusCode=200
            )
        else:
            app.logger.error("API ADMIN SET USER: ERROR: this username is not registered")
            return flask.jsonify(
                message="GET USER FAILED",
                statusCode=410
            )
    else:
        app.logger.error("API ADMIN SET USER: ERROR: request body is empty, check post request")
        return flask.jsonify(
            message="GET USER FAILED",
            statusCode=400
        )


@app.post("/api/admin/delete_user")
@security.admin_required
def delete_user():

    # Get new values from request body
    user_name = flask.request.form.get("user_name")

    if user_name is not None:

        deleted_user = users.delete_user(user_name, config.API_ADMIN_KEY, config.redis_client())
        return flask.jsonify(
            deleted_user=deleted_user,
            message="DELETE USER SUCCESS",
            statusCode=200
        )
    else:
        app.logger.error("API ADMIN SET USER: ERROR: request body is empty, check post request")
        return flask.jsonify(
            message="GET USER FAILED",
            statusCode=400
        )


if __name__ == '__main__':

    # Setup log level
    app.logger.setLevel(logging.DEBUG)

    # Setup api_key protection
    security.init_api_key_check(config)

    # Setup processor
    # proc = SampleMessageProcessor(app.logger)

    # Setup BackgroundScheduler to run processor by time schedule
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=proc.run, trigger="interval", seconds=config.DEFAULT_JOB_INTERVAL)
    # scheduler.start()

    # run Flask application
    app.run(debug=True, host='0.0.0.0', port=5010, use_reloader=False)
