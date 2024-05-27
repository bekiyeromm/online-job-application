from sqlalchemy import create_engine, text
import dotenv
import bcrypt
from dotenv import load_dotenv
import os
from werkzeug.security import check_password_hash

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
    """
    a function to which accepts applicant detail from html form
    inserts into database.
    """
    with engine.connect() as conn:
        query = text(
            """INSERT INTO sign_up (username, age, address, email, password)
            VALUES (:username, :age, :address, :email, :password)""")
        conn.execute(query,
                     {"username": data['username'],
                      "age": data['age'],
                         "address": data['address'],
                         "email": data['email'],
                         "password": data['password']})
        conn.commit()


def view_reg_applicant_by_job_id():
    """
    returns all applicants who applied for specific
    job using job_id
    """
    with engine.connect() as con:
        query = "select * from sign_up"
        result = con.execute(text(query))
        result_all = result.fetchall()

        """
        Convert each Row object into a dictionary and return dictionary
        """

        result_dicts = []
        for row in result_all:
            result_dict = {}
            for column, value in zip(result.keys(), row):
                result_dict[column] = value
            result_dicts.append(result_dict)
    return result_dicts


def search_applicant_by_userid(user_id):
    """
    a function which retrives   data from the data base using
    user id and return dictionery object of that data if data is found
    or none if the data is not found
    """
    with engine.connect() as conn:
        query = text('SELECT * FROM sign_up WHERE user_id = :user_id')
        result = conn.execute(query, {'user_id': user_id})
        row = result.fetchone()

        if row:
            return dict(zip(columns, row))
        else:
            return None


def view_all_member():
    """
    A function that retrieves all sign-up users' data from the database.
    Returns a list of dictionaries containing that data if found,
    or None if no data is found.
    """
    with engine.connect() as conn:
        query = text('SELECT * FROM sign_up')
        result = conn.execute(query)
        rows = result.fetchall()

        if rows:
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
        else:
            return None


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_existing_user(username, email):
    """
    Function to check if a user with the provided username or email
    already exists.Returns True if the user exists, False otherwise.
    """
    with engine.connect() as conn:
        query = text(
            '''SELECT COUNT(*) FROM sign_up
            WHERE username = :username OR email = :email''')
        result = conn.execute(query, {'username': username, 'email': email})
        count = result.scalar()

    return count > 0


def check_user_credentials(email, password):
    """
    a function to check and return user credential(email and password)
    """
    with engine.connect() as conn:
        query = text('SELECT * FROM sign_up WHERE email = :email')
        result = conn.execute(query, {'email': email}).mappings().fetchone()
        if result and result['password'] == password:
            return result
        return None
