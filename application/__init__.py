from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_USER = "postgres"
DB_PASS = 1488
IP = "127.0.0.1"
DB_NAME = "students"
DB_TEST = 'test'

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASS}@{IP}/{DB_NAME}"
POSTGRES_TEST = f"postgresql://{DB_USER}:{DB_PASS}@{IP}/{DB_TEST}"


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
if app.config["TESTING"]:
    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_TEST

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])


Base = declarative_base()
Base.metadata.clear()
