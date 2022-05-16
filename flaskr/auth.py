import functools
import traceback
from json import dumps
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,make_response
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        type = request.form['type']
        db = get_db()
        error = None

        if not account:
            error = 'account is required.'
        elif not password:
            error = 'Password is required.'
        elif not type:
            error = 'type is required.'

        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO car_sys.login (account, password,type) VALUES ('{}', '{}','{}')".format(account,generate_password_hash(password),type)
                )
                
            except Exception as e:
                traceback.print_exc()
                error = f"User {account} is already registered."
                response = make_response(dumps(error),404)
            else:
                response = make_response(dumps('register {} successfully'.format(account)), 200)
                # return redirect(url_for("auth.login"))
        else:
            response = make_response(dumps(error),400)
        flash(error)
        return response
    else:
        return render_template('auth/register.html')

    # return render_template('auth/register.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.prepare(
            "SELECT * FROM car_sys.user WHERE username = '{}'".format(username)
        )

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user()[0]['password'],password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_name'] = user()[0]['username']
            return redirect(url_for('index'))

        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',(user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view