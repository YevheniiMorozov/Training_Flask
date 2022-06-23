from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application import app, POSTGRES_URI


app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI


engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker()
