from flask import Flask, render_template, redirect
from flask import request
from sqlalchemy import text
from models.user import engine




app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/admin')
def admin():
    return render_template('admin.html')


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


@app.route('/reg_job')
def reg_job():
    """
    renders the job_post web page, which is the page used
    to post job
    """
    return render_template('job-post.html')


@app.route('/sign_up')
def sign_up():
    """
    renders the job_post web page, which is the page used
    to post job
    """
    return render_template('sign-up.html')

@app.route('/reg_user')
def user_registration():
    """
    renders the job_post web page, which is the page used
    to post job
    """
    return render_template('user.html')



if __name__ == '__main__':
    app.run(debug=True)