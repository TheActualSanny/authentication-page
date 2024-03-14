from flask import Flask, render_template, redirect, url_for, request 
from database import db_manager
from configparser import ConfigParser

manager = db_manager()
main_app = Flask(__name__)
starter_username = 'TestingName'
starter_pass = 'TestingPass'
login_name = 'TestingLoginName'
login_pass = 'TestingLoginPage'


@main_app.route('/login', methods = ['GET', 'POST'])
def login_page():
    context = {
        'start_user' : login_name,
        'start_pass' : login_pass
    }
    return render_template('login_input.html', **context)

@main_app.route('/', methods = ['GET', 'POST'])
def main_page():
    context = {
        'user' : starter_username,
        'pass' : starter_pass
    }
    return render_template('sign_up.html', **context)

@main_app.route('/success', methods=['GET', 'POST'])
def submit_click():
    username = request.form['username']
    password = request.form['password']
    credentials = {
        'username' : username,
        'password' : password
    }
    if manager.checker(username):
        return redirect(url_for('exists_screen'))
    else:
        manager.insert_data(username, password)
        return render_template('success.html', **credentials)

@main_app.route('/exists', methods=['GET', 'POST'])
def exists_screen():
    return render_template('exists.html')

@main_app.route('/login_success', methods=['GET', 'POST'])
def login_click():
    username = request.form['login_username']
    password = request.form['login_password']
    given = {
        'username' : username,
        'password' : password
    }
    if manager.account_checker(username, password):
        return render_template('login_success.html', **given)
    else:
        return redirect(url_for('login_failed'))
    
@main_app.route('/login_failed', methods=['GET', 'POST'])
def login_failed():
    return render_template('login_failed.html')
