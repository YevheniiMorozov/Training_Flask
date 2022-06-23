from flask import Flask

from sqlalchemy.ext.declarative import declarative_base


DB_USER = "teacher"
DB_PASS = "password"
IP = "127.0.0.1"
DB_NAME = "students"

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASS}@{IP}/{DB_NAME}"


app = Flask(__name__)


Base = declarative_base()
Base.metadata.clear()
