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
        query = text(
            "INSERT INTO users (username, password) values (:username, :password)")
        conn.execute(query,
                     {"username": data['username'],
                      "password": data['password']})
        conn.commit()


def view_users():
    """
    a function which retrives   data from the data base based on
    job id and return dictionery object of that data if data is found
    or none if the data is not found
    """
    with engine.connect() as con:
        query = "select * from users"
        result = con.execute(text(query))
        result_all = result.fetchall()
        result_dicts = []
        for row in result_all:
            result_dict = {}
            for column, value in zip(result.keys(), row):
                result_dict[column] = value
            result_dicts.append(result_dict)
    return result_dicts


def view_user_by_id(user_id):
    """
    Retrieves data from the database for a single user based on user ID
    """
    with engine.connect() as con:
        query = "SELECT * FROM users WHERE id = :user_id"
        # Pass parameters as a dictionary
        result = con.execute(text(query), {"user_id": user_id})
        user = result.fetchone()
        if user:
            user_dict = {}
            for column, value in zip(result.keys(), user):
                user_dict[column] = value
            return user_dict
        else:
            return None


def update_users_in_db(data):
    """updates a specific user in the users table using the
    user id"""
    with engine.connect() as conn:
        res = text(
            "UPDATE users SET username = :username, password = :password WHERE id = :id")
        conn.execute(res,
                     {"username": data['username'],
                      "password": data['password'],
                      "id": data['id']})
        conn.commit()


def delete_user_from_db(id):
    """deletes a user from the users table using user id"""
    with engine.connect() as conn:
        res = text("DELETE FROM users WHERE id = :id")
        conn.execute(res, {"id": id})
        conn.commit()
