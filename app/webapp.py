from flask import Blueprint,redirect,render_template,request,url_for,flash
from app import dask_apps
from app.extensions import bcrypt
from flask_login import login_user, current_user, logout_user, login_required
# from werkzeug.urls import url_parse
from app.forms import LoginForm
from app.models import User

server_bp = Blueprint('main', __name__)

@login_required
@server_bp.route('/')
def index():
    return dask_apps[0].index()
    # return render_template("index.html", title='Home Page', graph=dask_apps[0].index() )

# Login Page
@server_bp.route("/login", methods=['GET','POST'])
def login():

    # If user already is logged in return to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm() # Initialize Login Form and pass it to html template
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # If a user with given email exists and password is correct login
        if user and bcrypt.check_password_hash(user.password,form.password.data):
             login_user(user, remember=form.remember.data)   # FLaskLogin 
            #  flash(f'Logged in succesfully', 'success')
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
             flash(f'The combination of Email and Password is not correct, Try again', 'danger')

    return render_template('login.html', title='Login', form=form)

# Logout Route
@server_bp.route("/logout")
def logout():
    logout_user()
    flash(f'Logged out succesfully', 'info')
    return redirect(url_for('main.login'))