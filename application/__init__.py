from flask import Flask

DB_USER = "postgres"
DB_PASS = 1488
IP = "127.0.0.1"
DB_NAME = "students"


app = Flask(__name__)

POSTGRESURI = f"postgresql://{DB_USER}:{DB_PASS}@{IP}/{DB_NAME}"

app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRESURI
app.config['DEBUG'] = True
