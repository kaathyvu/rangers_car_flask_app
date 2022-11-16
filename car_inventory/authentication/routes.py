from flask import Blueprint, render_template, request, redirect, url_for, flash
from car_inventory.forms import UserSignUpForm, UserSignInForm
from car_inventory.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder="auth_templates")

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    signupform = UserSignUpForm()
    try:
        if request.method == "POST" and signupform.validate_on_submit():
            email = signupform.email.data
            first_name = signupform.first_name.data
            last_name = signupform.last_name.data
            password = signupform.password.data

            user = User(email, first_name, last_name, password=password)
            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account: {email}")
            return redirect(url_for('auth.signin'))
    except:
        raise Exception("Invalid form data. Please check your form.")
    return render_template("signup.html", signupform=signupform)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    signinform = UserSignInForm()
    try:
        if request.method == "POST" and signinform.validate_on_submit():
            email = signinform.email.data
            password = signinform.password.data

            logged_user = User.query.filter(User.email == email). first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
            
                flash(f"You have successfully logged in.", 'auth-success')
                return redirect(url_for('site.home'))
            
            else:
                flash("Your email or password was entered incorrectly. Please try again.", "auth-failed")
                return redirect(url_for('auth.signin'))
    except:
        raise Exception("Invalid form data. Please try again.")

    return render_template("signin.html", signinform=signinform)