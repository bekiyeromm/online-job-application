from sqlalchemy import create_engine, text
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()


con_string = os.getenv("DATABASE_CONNECTION_STRING")
engine = create_engine(con_string)

columns = [
    'username',
    'password']


def insert_into_users(data):
    with engine.connect() as conn:
        query = text("INSERT INTO users (username, password) values (:username, :password)")
        conn.execute(query, {"username": data['username'], "password": data['password']})
        conn.commit()