from sqlalchemy import create_engine, text
import dotenv
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
import bcrypt

load_dotenv()


con_string = os.getenv("DATABASE_CONNECTION_STRING")
engine = create_engine(con_string)

columns = [
    'username',
    'password']


def insert_into_users(data):
    """
    Inserts user data into the users table.
    """
    password = data['password']
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    with engine.connect() as conn:
        query = text(
            """INSERT INTO users (username, password)
            VALUES (:username, :password)"""
        )
        conn.execute(query,
                     {"username": data['username'],
                      "password": hashed_password.decode('utf-8')})
        conn.commit()

def check_user_exists(username):
    """
    Checks if a user with the given username already exists.
    """
    with engine.connect() as conn:
        query = text('SELECT * FROM users WHERE username = :username')
        result = conn.execute(query, {'username': username}).fetchone()
        return result is not None


def view_users():
    """
    a function which retrives all user data from the data base
    and return dictionery object
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
    """
    updates a specific user in the users table using theuser id
    """
    password = data['password']
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with engine.connect() as conn:
        query = text(
            """UPDATE users SET username = :username,
            password = :password WHERE id = :id"""
        )
        conn.execute(query,
                     {"username": data['username'],
                      "password": hashed_password.decode('utf-8'),
                      "id": data['id']})
        conn.commit()


def delete_user_from_db(id):
    """
    deletes a user from the users table using user id
    """
    with engine.connect() as conn:
        res = text("DELETE FROM users WHERE id = :id")
        conn.execute(res, {"id": id})
        conn.commit()
