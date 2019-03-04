from flask import Blueprint, render_template, request, flash, redirect, url_for
from passlib.hash import sha256_crypt
from flask_login import login_user, logout_user, login_required

from austin import db, User
# from austin.models.user_models import User

from .forms import RegistrationForm
from .utils import user_exsists

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')

    else:
        email = request.form.get('email')
        password_candidate = request.form.get('password')

        # Query for a user with the provided username
        result = User.query.filter_by(email=email).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            login_user(result)

            flash('Successful Login!', 'success')
            return redirect(url_for('main.index'))

        else:
            flash('Incorrect Login!', 'danger')
            return redirect(url_for('main.index'))


@users.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return redirect(url_for('main.index'))


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # Uses WTF to check if POST req and form is valid
    if form.validate_on_submit():
        # Create user object to insert into SQL
        hashed_pass = sha256_crypt.encrypt(str(form.password.data))

        new_user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_pass)

        if user_exsists(new_user.username, new_user.email):
            flash('User already exsists!', 'danger')
            return render_template('users/register.html', form=form)
        else:
            # Insert new user into SQL
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            flash('Account created!', 'success')
            return redirect(url_for('main.index'))

    return render_template('users/register.html', form=form)
