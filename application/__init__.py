from flask import Flask

DB_USER = "postgresql"
DB_PASS = 15042021
IP = "localhost:5432"
DB_NAME = "students"


app = Flask(__name__)

POSTGRESURI = f"postgresql://{DB_USER}:{DB_PASS}@{IP}/{DB_NAME}"

app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRESURI
