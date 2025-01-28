from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from db import db, initialize_db, User, File, Payment, Subscription  # Import from db.py
from sqlalchemy.orm import joinedload

# Set up logging for SQLAlchemy queries
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Initialize Flask app and configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sininkii2305200@localhost/db_payment_codefirst'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging

# Initialize the database with app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Fetch data using Eager Loading
@app.route('/eager_users')
def fetch_users_eager():
    users = User.query.options(joinedload(User.files)).all()
    result = [{
        'user_id': user.user_id,
        'username': user.username,
        'files': [{'file_name': f.file_name, 'file_size_mb': float(f.file_size_mb)} for f in user.files]
    } for user in users]
    return result

# Fetch data using Lazy Loading
@app.route('/lazy_users')
def fetch_users_lazy():
    users = User.query.all()
    result = [{
        'user_id': user.user_id,
        'username': user.username,
        'files': [{'file_name': f.file_name, 'file_size_mb': float(f.file_size_mb)} for f in user.files]  # Lazy-loaded here
    } for user in users]
    return result

# Function to add user
def add_user(username, email, password_hash):
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

# Function to fetch all users
def fetch_all_users():
    users = User.query.all()
    return [{
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
    } for user in users]

# Main function to run the Flask app
if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
