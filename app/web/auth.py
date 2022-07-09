from app.models import User
from app.web import auth_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
from bcrypt import checkpw


@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    # form = UserForm()
    if request.method == 'POST':
        email = request.form.get('email')  # args取get方式参数

        password = request.form.get('password')
        # password = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
        user = User.query.filter_by(email=email).first()
        is_pw_ok = False
        if not user:
            hashed = user.password
            is_pw_ok = checkpw(password.encode('utf8'), hashed.encode('utf8'))
        if is_pw_ok:
            flash('Welcome back.', 'info')
            login_user(user)
            return redirect(url_for('h5_qu.get_quizs'))
        else:
            flash('Invalid username or password.', 'warning')
            return render_template('login.html')
    elif request.method == 'GET':
        return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
