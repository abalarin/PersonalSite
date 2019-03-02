from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from passlib.hash import sha256_crypt

from austin.models.user_models import User

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.htm')

    else:
        email = request.form.get('email')
        password_candidate = request.form.get('password')

        # Query for a user with the provided username
        result = User.query.filter_by(email=email).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            session['logged_in'] = True
            session['user_id'] = result.id
            session['username'] = result.username
            session['admin'] = result.admin

            flash('Successful Login!', 'success')
            return redirect(url_for('users.dashboard'))

        else:
            flash('Incorrect Login!', 'danger')
            return redirect(url_for('main.index'))
