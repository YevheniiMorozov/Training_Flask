from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application import app, POSTGRES_URI, POSTGRES_TEST


app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
if app.config["TESTING"]:
    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_TEST


engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker()
