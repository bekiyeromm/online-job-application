from sqlalchemy import create_engine, text
import dotenv
from dotenv import load_dotenv
import os
from flask import request

load_dotenv()


con_string = os.getenv("DATABASE_CONNECTION_STRING")
engine = create_engine(con_string)
columns = [
    'id',
    'job_id',
    'full_name',
    'email',
    'linkedin',
    'qualification',
    'experience',
    'resume']


def get_user_id_from_request():
    """
    Retrieve user_id from the sign_up table based on some
    identifier in the request.
    """
    email = request.form.get("email")
    if email:
        with engine.connect() as conn:
            query = text(
                "SELECT user_id FROM sign_up WHERE email = :email")
            result = conn.execute(query, {'email': email}).fetchone()
            if result:
                return result[0]  # Return the user_id if found
    return None


def insert_application(user_id, job_id, data):
    """
    Accepts applicant information from HTML form checks
    if applicants are sign up
    and inserts into the database table named applications.
    """
    # Check if the user is registered in the sign_up table
    with engine.connect() as conn:
        user_check_query = text(
            "SELECT user_id FROM sign_up WHERE user_id = :user_id")
        user_exists = conn.execute(
            user_check_query, {
                "user_id": user_id}).fetchone()

        if user_exists:
            # If the user exists, insert the application
            insert_query = text("""
                INSERT INTO applications (job_id, full_name, email, linkedin, qualification, experience, resume, user_id)
                VALUES (:job_id, :full_name, :email, :linkedin, :qualification, :experience, :resume, :user_id)
            """)
            conn.execute(insert_query, {
                "job_id": job_id,
                "full_name": data['full_name'],
                "email": data['email'],
                "linkedin": data['linkedin'],
                "qualification": data['qualification'],
                "experience": data['experience'],
                "resume": data['resume'],
                "user_id": user_id
            })
            conn.commit()
            return True
        else:
            # If the user does not exist, return False
            return False


def view_all_applicant():
    """
    a function which retrives   data from the data base based on
    job id and return dictionery object of that data if data is found
    or none if the data is not found
    """
    with engine.connect() as conn:
        query = text('SELECT id, job_id, full_name, email, linkedin, qualification, experience FROM applications')
        result = conn.execute(query).all()
        return result


def view_applicant_by_job_id(job_id):
    """
   a function which retrives   data from the data base based on
   job id and return dictionery object of that data if data is found
   or none if the data is not found
   """
    with engine.connect() as conn:
        query = text('SELECT * FROM applications WHERE job_id = :job_id')
        result = conn.execute(query, {'job_id': job_id})
        row = result.all()
        return row
