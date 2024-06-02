from sqlalchemy import create_engine, text
import dotenv
from dotenv import load_dotenv
import os
from flask import request
from sqlalchemy.engine import Result


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
    Accepts applicant information from HTML form, checks
    if applicants are signed up, and inserts into the database table named
    applications.
    """
    with engine.connect() as conn:
        user_check_query = text(
            "SELECT user_id FROM sign_up WHERE user_id = :user_id")
        user_exists = conn.execute(
            user_check_query, {
                "user_id": user_id}).fetchone()

        if user_exists:
            application_check_query = text(
                """SELECT id FROM applications
                WHERE user_id = :user_id AND job_id = :job_id AND email = :email""")
            application_exists = conn.execute(
                application_check_query, {
                    "user_id": user_id, "job_id": job_id, "email": data['email']}).fetchone()

            if application_exists:
                return 'exists'

            insert_query = text("""
                INSERT INTO applications (job_id, full_name, email, linkedin,
                qualification, experience, resume, user_id, status)
                VALUES (:job_id, :full_name, :email, :linkedin, :qualification,
                :experience, :resume, :user_id, 'pending')
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
            return 'success'
        else:
            return 'user_not_found'


def view_all_applicant():
    """
    a function which retrives   data from the data base based on
    job id and return dictionery object of that data if data is found
    or none if the data is not found
    """
    with engine.connect() as conn:
        query = text(
            '''SELECT id, job_id, full_name, email, linkedin, qualification,
            experience, status FROM applications''')
        result = conn.execute(query).all()
        return result


def view_applicant_by_job_id(job_id):
    """
    A function which retrieves data from the database based on
    job id and returns a dictionary object of that data if found,
    or None if not found.
    """
    with engine.connect() as conn:
        query = text('SELECT * FROM applications WHERE job_id = :job_id')
        result = conn.execute(query, {'job_id': job_id})
        row = result.all()
        return row


def change_application_status(application_id, status):
    """
    A function to change the status of applicants
    """
    if status not in ['pending', 'reviewed', 'selected']:
        raise ValueError("Invalid status value")

    with engine.connect() as conn:
        select_details_query = text('''
            SELECT a.email, a.full_name, j.title
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.id = :application_id
        ''')
        result = conn.execute(select_details_query,
                              {'application_id': application_id}).fetchone()

        if result is None:
            raise ValueError("Applicant not found")

        applicant_email = result[0]
        applicant_name = result[1]
        job_title = result[2]
        update_status_query = text(
            '''UPDATE applications SET status = :status
            WHERE id = :application_id'''
        )
        conn.execute(
            update_status_query, {
                'status': status, 'application_id': application_id})
        conn.commit()
        return applicant_email, applicant_name, job_title
