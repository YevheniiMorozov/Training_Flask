from application import app
from database import models
from sqlalchemy import create_engine
from database.database import SessionLocal


engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
models.Base.metadata.create_all(engine)


@app.route("/")
def index():
    return "Hello world"


if __name__ == '__main__':
    app.run(debug=True)