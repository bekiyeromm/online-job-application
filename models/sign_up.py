from sqlalchemy import create_engine, text
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()


con_string = os.getenv("DATABASE_CONNECTION_STRING")
engine = create_engine(con_string)
columns = [
    'user_id',
    'username',
    'age',
    'address',
    'email',
    'password']


def insert_into_sign_up(data):
    with engine.connect() as conn:
        query = text(
            "INSERT INTO sign_up (username, age, address, email, password) VALUES (:username, :age, :address, :email, :password)")
        conn.execute(query,
                     {"username": data['username'],
                      "age": data['age'],
                         "address": data['address'],
                         "email": data['email'],
                         "password": data['password']})
        conn.commit()
