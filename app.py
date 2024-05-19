from flask import Flask, render_template, redirect
from flask import request, flash
from sqlalchemy import text
from models.user import engine, insert_into_users
from models.user import view_user_by_id, view_users
from models.user import update_users_in_db,delete_user_from_db


app = Flask(__name__)
app.secret_key="ikebolleh"

############################################################
"""root page api"""
############################################################


@app.route('/')
def home():
    return render_template('home.html')

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
""" Job Registration PAge"""
##############################################################


@app.route('/reg_job')
def reg_job():
    """
    renders the job_post web page, which is the page used
    to post job
    """
    return render_template('job-post.html')

#############################################################
""" staff api (admin user api)"""
#############################################################


@app.route('/sign_up')
def sign_up():
    """
    renders the job_post web page, which is the page used
    to post job
    """
    return render_template('sign-up.html')

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
    dataa = request.form
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