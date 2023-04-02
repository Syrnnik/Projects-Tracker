from os import getenv

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///" + getenv('DB_PATH')
HOST = getenv('HOST')
PORT = int(getenv('PORT'))
