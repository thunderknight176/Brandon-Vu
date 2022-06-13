from flask import Blueprint, render_template, request, flash, redirect, url_for,sessions
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime 

auth = Blueprint('auth', __name__)
@auth.route('/database')
def database():
    return render_template('index.html',user=current_user,values=User.query.all())
@auth.route('/clear',methods=['GET', 'POST'])
def clear():
    clear_db=User.query.all()
    db.session.delete(clear_db)
    db.session.commit()

@auth.route('/delete/<int:id>')
def delete(id):
    delete=User.query.get_or_404(id)
    db.session.delete(delete)
    db.session.commit()
    our_users = User.query.order_by(User.date_added)
    flash('Success')
    return redirect(url_for('auth.database'))
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        found_user= User.query.filter_by(username=username).first()
        user=User.query.filter_by(username=username).first()
        if user:
            if user.password==password:         #check_password_hash(user.password, password):
                flash('Logged In',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password',category='error')
        else:
            flash('Username Does not exist',category='error')
    return render_template('login.html',user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user=User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists',category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 6 characters.', category='error')
        else:
            new_user=User(username=username,password=password)  
            #generate_password_hash(
            #    password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account has been created',category='success')
            return redirect(url_for('views.home'))
        our_users = User.query.order_by(User.date_added)
    return render_template('signup.html',user=current_user)