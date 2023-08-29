# Vacancy parser in Telegram:
API Telegram: https://core.telegram.org/api \
For Telegram parsing we will use [Pyrogram library](https://docs.pyrogram.org/intro/quickstart)\
\
First of all, we need to register our app to get access to Telegram API \
https://my.telegram.org/apps \
Setup pyrogram and tgcrypto (it recommended in Pyrogram docs):\
https://docs.pyrogram.org/intro/install

In this case secret keys are - **App api_id** and **App api_hash** from Telegram app page https://my.telegram.org/apps \
We need to add our API_ID and API_HASH in **dot.env** file

### Library import
```
import pyrogram
import requests
import numpy as np
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from pyrogram import Client
import pandas as pd
import json
from datetime import datetime
import re
from IPython.core.display import display, HTML, clear_output
import ipywidgets as widgets

pyrogram.__version__
```
> '1.4.1'

**WARNING:** There is a secret keys, therefore we keep it in environment config (file dot.env)\
If you make your code public file *dot.env* shouldn't be published (add into gitignore)
```
dotenv_path = os.path.join('dot.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    
os.environ['DEMO']
```
> 'demo'
```
API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']
```
### Create authorization module pyro_auth.py
```
from pyrogram import Client
import os
from dotenv import load_dotenv


path = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(path + '/dot.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    
API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']
with Client("my_account", API_ID, API_HASH) as app: 
    app.send_message("me", "Авторизация прошла успешно")
```

If authorization was successful you get new active session in your Telegram app with name CPython. \
You can see it if you open your Telegram app and go to  Settings --> Devices. \
You can close this session and disconnect you device from this account by this way. \
If you need you can make authorization again by script `pyro_auth.py`, with phone number and password

