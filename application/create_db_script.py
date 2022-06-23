import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from application import IP


conn = psycopg2.connect(
    host=IP,
    user="postgres",
    password="1488"
)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

with open("create_database.sql", "r") as db_file, open("create_user.sql", "r") as user_file:
    create_user = user_file.read()
    create_db = db_file.read()

if __name__ == '__main__':
    cursor = conn.cursor()
    cursor.execute(create_db)
    cursor.execute(create_user)