from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.htm')


@main.route('/login')
def login():
    return render_template('users/login.htm')
