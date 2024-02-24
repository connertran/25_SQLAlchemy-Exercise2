"""Blogly application."""
"""In order the app to work, please create a blogly database before using the app"""

from flask import Flask,request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chicken123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def show_home_page():
    """List all the users"""
    users = User.query.all()
    return render_template('index.html', users = users)

@app.route('/users/new', methods = ["GET"])
def show_form():
    """Show add user form"""
    return render_template('new-user.html')
@app.route('/users/db', methods=['POST'])
def saving_user_info():
    """saving user's info to the data base and show the user's profile"""
    first_name = request.form['first-name']
    last_name= request.form['last-name']
    img_url = request.form['img-url']

    if not img_url:
        img_url = "https://cdn.vectorstock.com/i/preview-1x/61/88/user-icon-human-person-symbol-avatar-login-sign-vector-28996188.jpg"

    new_user = User(first_name = first_name, last_name= last_name, image_url = img_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/user/{new_user.id}")

@app.route('/user/<int:user_id>')
def show_details(user_id):
    """showing detail page"""
    individual_user= User.query.get_or_404(user_id)
    return render_template('profile.html', user_info = individual_user)

@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """deleting a user from the db"""
    user = User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect('/')

@app.route('/user/edit/<int:user_id>', methods =['POST'])
def change_form_info(user_id):
    """show form for editing info"""
    user = User.query.get(user_id)
    return render_template("edit-form.html", user = user)
@app.route('/user/changed/<int:user_id>', methods = ['POST'])
def change_user_info(user_id):
    """Update user's info in the database"""
    user = User.query.get(user_id)

    first_name = request.form['first-name']
    last_name= request.form['last-name']
    img_url = request.form['img-url']

    user.first_name =first_name
    if last_name:
        user.last_name = last_name
    if img_url:
        user.image_url = img_url

    db.session.add(user)
    db.session.commit()
    return redirect(f'/user/{user.id}')