from flask import Blueprint, render_template, request, session, flash, redirect, url_for

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.htm')
