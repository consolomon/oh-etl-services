import os

from lib.pg import PgConnect
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid


class AppConfig:
    CERTIFICATE_PATH = '/crt/my_CA.crt'
    DEFAULT_JOB_INTERVAL = 1800

    def __init__(self) -> None:

        self.pg_warehouse_host = str(os.getenv('PG_WAREHOUSE_HOST') or "")
        self.pg_warehouse_port = int(str(os.getenv('PG_WAREHOUSE_PORT') or 0))
        self.pg_warehouse_dbname = str(os.getenv('PG_WAREHOUSE_DBNAME') or "")
        self.pg_warehouse_user = str(os.getenv('PG_WAREHOUSE_USER') or "")
        self.pg_warehouse_password = str(os.getenv('PG_WAREHOUSE_PASSWORD') or "")

    def pg_warehouse_db(self):
        return PgConnect(
            self.pg_warehouse_host,
            self.pg_warehouse_port,
            self.pg_warehouse_dbname,
            self.pg_warehouse_user,
            self.pg_warehouse_password
        )


def pyrogram_client():

    telegram_api_id = int(os.getenv('TELEGRAM_API_ID') or 0)
    telegram_api_hash = str(os.getenv('TELEGRAM_API_HASH') or "")
    phone_number = str(os.getenv('TELEGRAM_PHONE_NUMBER') or "")
    client = Client(
        name="hs_explorer",
        api_id=telegram_api_id,
        api_hash=telegram_api_hash,
        device_model="HS_client",
        test_mode=True,
        hide_password=True,
        workers=2
    )
    client.connect()
    sent_code_info = client.send_code(phone_number)
    phone_code = input("Please enter your phone code: ")  # Sent phone code using last function
    while True:
        try:
            client.sign_in(phone_number, sent_code_info.phone_code_hash, phone_code)
            break
        except SessionPasswordNeeded:
            password = input("Please enter your pass: ")  # Sent phone code using last function
            try:
                client.check_password(password)
                break
            except PasswordHashInvalid:
                print("pass error try again")
        except PhoneCodeInvalid:
            print("code error try again")
    return client
