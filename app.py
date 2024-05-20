from flask import Flask, render_template, redirect
from flask import request, flash
from sqlalchemy import text

import bcrypt
from models.user import engine, insert_into_users
from models.user import view_user_by_id, view_users
from models.user import update_users_in_db,delete_user_from_db

from datetime import datetime, timedelta, date

from dotenv import load_dotenv
import os

from models.jobs import load_jobs_from_db, get_job_by_id, update_job_in_db
from models.jobs import insert_into_job, delete_job_from_db

from models.sign_up import insert_into_sign_up, view_all_member
from models.sign_up import view_reg_applicant_by_job_id,search_applicant_by_userid
from models.sign_up import check_existing_user, hash_password

from models.applications import get_user_id_from_request, insert_application
from models.applications import view_all_applicant, view_applicant_by_job_id


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


############################################################
"""root page api"""
############################################################

@app.route('/')
def home():
    jobs = load_jobs_from_db()
    today_date = date.today()
    active_jobs = [job for job in jobs if job['expiration_date'] >= today_date]
    return render_template('home.html', jo=active_jobs, today=today_date)

############################################################
""" API end point to Render Admin page"""
############################################################


@app.route('/admin')
def admin():
    return render_template('admin.html')

############################################################
""" About us page"""
############################################################


@app.route('/about')
def about():
    return render_template('about.html')

############################################################
"""Login page Api """
#############################################################


@app.route('/login')
def login():
    """
    renders the login web page
    """
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def main():
    """api route retrive json data from html form and from,
    database table checks if both value matches, if so
    allows the user to navigate into home page"""
    username = request.form['username']
    password = request.form['password']
  
    try:
        with engine.connect() as conn:
            query = text(
                "SELECT * FROM users WHERE username = :username AND password = :password")
            result = conn.execute(
                query, {"username": username, "password": password})
            credentials = result.fetchone()
            if credentials:
                """Redirect the user to the Admin home page"""
                return redirect('/admin')
            else:
                """invalid credentials, Redirect the user to the login page"""
                return render_template(
                    'login.html', error_message='Invalid username or password')
    except Exception as e:
        """Display an error message for any exception"""
        return render_template('login.html', error_message=str(e))

##############################################################
""" Job Api"""
##############################################################


@app.route('/reg_job')
def reg_job():
    """
    renders the job_post web page, which is the page used
    to post job
    """
    return render_template('job-post.html')


jo=[]
@app.route('/post_job', methods=['post'])
def post_new_job():
    """
    posts a new job using html form
    """
    title = request.form['title']
    location = request.form['location']
    salary = request.form['salary']
    currency = request.form['currency']
    responsibilities = request.form['responsibilities']
    requirements = request.form['requirements']
    released_date = request.form['released_date']
    expiration_date = request.form['expiration_date']
    released_date = datetime.strptime(released_date, '%Y-%m-%d')
    expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
    data = {
        'title': title,
        'location': location,
        'salary': salary,
        'currency': currency,
        'responsibilities': responsibilities,
        'requirements': requirements,
        'release_date': released_date,
        'expiration_date': expiration_date
    }
    jo.append(data)
    insert_into_job(data)
    """
    to return json file use'return jsonify(job_list)
    '"""
    return redirect("/job")


@app.route('/job')
def list_job():
    """
    returns all the listed jobs from the database
    and displays on view-jobs.html web page
    """
    jobs = load_jobs_from_db()
    return render_template('view-jobs.html', job=jobs)


@app.route("/job/<int:id>")
def search_job(id):
    """
    retrives a job item from the database using
    job id
    """
    job = get_job_by_id(id)
    if job:
        return render_template("job-detail.html", job=job)
    else:
        return ("Job not found")


@app.route('/search_job')
def job_search():
    """
    renders search-job.html page
    """
    return render_template('search-job.html')


@app.route("/job_search", methods=["GET"])
def get_job():
    """
    Retrieves a job item from the database using job id.
    """
    job_id = request.args.get('id', type=int)
    if job_id is not None:
        job = get_job_by_id(job_id)
        if job:
            return render_template("view-single-job.html", job=job)
        else:
            return "Job not found", 404
    else:
        return "Invalid job ID", 400


@app.route('/update_job_form')
def update_job_form():
    job_id = request.args.get('id')
    job = get_job_by_id(job_id)
    if job:
        return render_template('update-job.html', job=job)
    else:
        flash('Job not found', 'error')
        return redirect('/job')


@app.route('/update_job/<int:job_id>', methods=['POST'])
def update_job(job_id):
    data = {
        'title': request.form['title'],
        'location': request.form['location'],
        'salary': request.form['salary'],
        'currency': request.form['currency'],
        'responsibilities': request.form['responsibilities'],
        'requirements': request.form['requirements'],
        'release_date': request.form['release_date'],
        'expiration_date': request.form['expiration_date']
    }
    try:
        update_job_in_db(data, job_id)
        flash('Job updated successfully', 'success')
    except Exception as e:
        flash(f'Error updating job: {str(e)}', 'error')
    return redirect('/job')


@app.route('/delete_job', methods=['POST'])
def delete_job_fun():
    """Deletes a job based on the provided job ID"""
    job_id = request.form.get('id')
    if job_id:
        try:
            delete_job_from_db(job_id)
            flash('Job deleted successfully', 'success')
        except Exception as e:
            flash(f'Error deleting job: {str(e)}', 'error')
    else:
        flash('Job ID not found!', 'error')
    return redirect('/job')



#############################################################
""" applicant Api for sign up"""
#############################################################


@app.route('/sign_up')
def sign_up():
    """
    renders the job_post web page, which is the page used
    to post job
    """
    return render_template('sign-up.html')


@app.route('/sign_up', methods=['POST'])
def user_sign_up():
    """
    a function aalows applicants to register first
    before applying for job
    """
    username = request.form['username']
    age = request.form['age']
    address = request.form['address']
    email = request.form['email']
    password = request.form['password']
    password=hash_password(password)
    data = {
        'username': username,
        'age': age,
        'address': address,
        'email': email,
        'password': password
    }
    if check_existing_user(username, email):
        flash('User with the same username or email already exists', 'error')
        return redirect('/sign_up')  
    if insert_into_sign_up(data):
        flash('User registered successfully', 'success')
    else:
        flash('Error registering user', 'error')
    return redirect('/')


@app.route('/view_member')
def view_all_member_route():
    members = view_all_member()
    if members:
        return render_template('view-all-member.html', members=members)
    else:
        return "Empty!"

    
###########################################################
""" user api"""
###########################################################


@app.route('/reg_user')
def user_registration():
    """
    renders the user.html web page, which is the staff
    user registration form
    """
    return render_template('user.html')


@app.route('/register', methods=['POST'])
def user():
    """
    inserts (user name and password) data into users table
    """
    username=request.form.get('username')
    pasword=request.form.get('password')
    dataa = {
        'username':username,
        'password':pasword
    }
    insert_into_users(dataa)
    return redirect("/reg_user")


@app.route('/view_user')
def view_user():
    """
    displays all list of Staff users in a table
    """
    users = view_users()
    return render_template('view-user.html', users=users)


@app.route('/view_user/<int:user_id>')
def view_single_user(user_id):
    """
    Displays a single user based on the user ID
    """
    user = view_user_by_id(user_id)
    if user:
        return render_template('view-single-user.html', user=user)
    else:
        flash('User not found', 'error')
        return redirect('/view_user')


@app.route('/update_user')
def update_user():
    user_id = request.args.get('user_id')
    if user_id:
        user = view_user_by_id(user_id)
        if user:
            return render_template('update-user.html', user=user)
        else:
            flash('User not found', 'error')
    else:
        flash('No user ID provided', 'error')
    return redirect('/view_user')


@app.route('/update_users/<int:user_id>', methods=['POST'])
def update_users(user_id):
    """Updates a user using user id and redirects the user to the view user page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        data = {
            'id': user_id,
            'username': username,
            'password': password,
        }
        try:
            update_users_in_db(data)
            flash('User updated successfully', 'success')
            return redirect('/view_user')
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'error')
            return redirect(f'/view_user/{user_id}')




@app.route('/delete_user', methods=['POST'])
def delete_user_fun():
    """Deletes a user based on the provided user ID"""
    user_id = request.form.get('id')
    if user_id:
        try:
            delete_user_from_db(user_id)
            flash('User deleted successfully', 'success')
        except Exception as e:
            flash(f'Error deleting user: {str(e)}', 'error')
    else:
        flash('User ID not found !', 'error')
    return redirect('/view_user')



if __name__ == '__main__':
    app.run(debug=True)