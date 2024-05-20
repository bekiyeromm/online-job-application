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
    """
    a function to which accepts applicant detail from html form
    inserts into database.
    """
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