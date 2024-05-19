from sqlalchemy import create_engine, text
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()


con_string = os.getenv("DATABASE_CONNECTION_STRING")
engine = create_engine(con_string)
columns = [
    'id',
    'title',
    'location',
    'salary',
    'currency',
    'responsibilities',
    'requirements',
    'release_date',
    'expiration_date']


def insert_into_job(data):
    with engine.connect() as conn:
        query = text("INSERT INTO jobs (title, location, salary, currency, responsibilities,requirements, release_date, expiration_date) VALUES (:title, :location, :salary, :currency, :responsibilities, :requirements, :release_date, :expiration_date)")
        conn.execute(query, {"title": data['title'], "location": data['location'], "salary": data['salary'], "currency": data['currency'], "responsibilities": data['responsibilities'], "requirements": data['requirements'], "release_date": data['release_date'], "expiration_date": data['expiration_date']})
        conn.commit()


def load_jobs_from_db():
    """
    a function which retrives all the data from the data base and
    convert it into dictionary and return the dictionary object
    """
    with engine.connect() as con:
        query = "select * from jobs"
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


def get_job_by_id(job_id):
    """
    a function which retrives   data from the data base based on
    job id and return dictionery object of that data if data is found
    or none if the data is not found 
    """
    with engine.connect() as conn:
        query = text('SELECT * FROM jobs WHERE id = :id')
        result = conn.execute(query, {'id': job_id})
        row = result.fetchone()

        if row:
            return dict(zip(columns, row))
        else:
            return None
        

def update_job_in_db(data, job_id):
    with engine.connect() as conn:
        query = text("""
            UPDATE jobs 
            SET title = :title, 
                location = :location, 
                salary = :salary, 
                currency = :currency, 
                responsibilities = :responsibilities, 
                requirements = :requirements, 
                release_date = :release_date, 
                expiration_date = :expiration_date 
            WHERE id = :job_id
        """)
        conn.execute(query, {
            "title": data['title'], 
            "location": data['location'], 
            "salary": data['salary'], 
            "currency": data['currency'], 
            "responsibilities": data['responsibilities'], 
            "requirements": data['requirements'], 
            "release_date": data['release_date'], 
            "expiration_date": data['expiration_date'], 
            "job_id": job_id
        })
        conn.commit()


def delete_job_from_db(id):
    """Deletes a job from the jobs table using job ID"""
    with engine.connect() as conn:
        res = text("DELETE FROM jobs WHERE id = :id")
        conn.execute(res, {"id": id})
        conn.commit()