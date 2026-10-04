from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from .db import SessionLocal

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  else:
    username = request.form['username'].strip()
    password = request.form['password']
    if len(username) < 3 or len(username) > 50:
      flash('Username must be between 3 and 50 characters long.')
      return redirect(url_for('auth.register'))
    if len(password) < 8:
      flash('Password must be at least 8 characters long.')
      return redirect(url_for('auth.register'))
    if username == "demo":
      flash('Username "demo" is reserved.')
      return redirect(url_for('auth.register'))
    if username == "DEMO":
      flash('Username "DEMO" is reserved.')
      return redirect(url_for('auth.register'))
    if username == "Demo":
      flash('Username "Demo" is reserved.')
      return redirect(url_for('auth.register')) 

    with SessionLocal() as db:
      if db.query(User).filter_by(username=username).first():
        flash('Username already exists.')
        return redirect(url_for('auth.register'))
      else:
        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.add(new_user)
        db.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():      
  if request.method == 'GET':
    return render_template('login.html')
  else:
    username = request.form['username'].strip()
    password = request.form['password']

    with SessionLocal() as db:
      user = db.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
      login_user(user)
      return redirect(url_for('index'))
    else:
      flash('Invalid username or password.')
      return redirect(url_for('auth.login'))

@bp.route('/logout')
def logout():
  logout_user()
  flash('You have been logged out.')
  return redirect(url_for('auth.login'))

@bp.route('/demo', methods=['POST'])
def demo():
  with SessionLocal() as db:
    demo_user = db.query(User).filter_by(is_demo=True).first()
    if demo_user:
      login_user(demo_user)
      return redirect(url_for('index'))
    else:
      flash('Demo user not found. Please contact support.')
      return redirect(url_for('auth.login'))

    