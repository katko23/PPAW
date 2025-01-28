import json
import secrets
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import redis
from datetime import datetime
from flask import render_template, redirect, url_for, flash

# Initialize Flask app and configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sininkii2305200@localhost/db_payment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Set a secure secret key


# Initialize database and Redis cache
db = SQLAlchemy(app)
cache = redis.Redis(host='localhost', port=6379, db=0)

# Define ORM models
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    subscription_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    max_file_size_mb = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

class File(db.Model):
    __tablename__ = 'files'
    file_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_size_mb = db.Column(db.Numeric(10, 2), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.now())

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.subscription_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.now())

# Function to serialize datetime objects into strings
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to string (ISO format)
    raise TypeError(f"Type {type(obj)} not serializable")

# Function to deserialize datetime strings back to datetime objects
def custom_deserializer(obj):
    if 'created_at' in obj and isinstance(obj['created_at'], str):
        obj['created_at'] = datetime.fromisoformat(obj['created_at'])  # Convert string to datetime
    return obj

@app.route('/')
def home():
    return render_template('index.html')  # The main page where users and payments are listed

@app.route('/users/add')
def add_user_page():
    return render_template('add_user.html')  # The page for adding a new user

@app.route('/payments/add')
def add_payment_page():
    return render_template('payment_form.html')  # The page for adding a new payment

# Fetch all users
@app.route('/api/users', methods=['GET'])
def get_users():
    cached_users = cache.get('users')
    if cached_users:
        try:
            # Load cached data and convert back datetime strings to datetime objects
            users_data = json.loads(cached_users)
            users_data = [custom_deserializer(user) for user in users_data]
            return jsonify(users_data)  # Return cached data
        except json.JSONDecodeError:
            # Handle JSON decoding error (this shouldn't happen if we're using proper JSON)
            return jsonify({"error": "Failed to decode cached data"}), 500

    users = User.query.all()
    user_list = [{
        'user_id': u.user_id,
        'username': u.username,
        'email': u.email,
        'created_at': u.created_at  # This will be a datetime object
    } for u in users]

    # Cache the result (convert datetime objects to strings)
    cache.set('users', json.dumps(user_list, default=custom_serializer))  # Use custom_serializer to handle datetime objects
    return jsonify(user_list)


# Add a new user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password_hash']
    )
    db.session.add(new_user)
    db.session.commit()
    cache.delete('users')  # Clear the cache
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    cached_subscriptions = cache.get('subscriptions')
    if cached_subscriptions:
        subscriptions_data = json.loads(cached_subscriptions)
        subscriptions_data = [custom_deserializer(sub) for sub in subscriptions_data]
        return jsonify(subscriptions_data)

    subscriptions = Subscription.query.all()
    subscription_list = [{
        'subscription_id': s.subscription_id,
        'name': s.name,
        'price': float(s.price),
        'max_file_size_mb': s.max_file_size_mb,
        'created_at': s.created_at
    } for s in subscriptions]

    # Cache the result
    cache.set('subscriptions', json.dumps(subscription_list, default=custom_serializer))
    return jsonify(subscription_list)

# Add a file upload
@app.route('/api/files', methods=['POST'])
def upload_file():
    data = request.json
    new_file = File(
        user_id=data['user_id'],
        file_name=data['file_name'],
        file_size_mb=data['file_size_mb']
    )
    db.session.add(new_file)
    db.session.commit()
    cache.delete('files')  # Clear the cache
    return jsonify({'message': 'File uploaded successfully'}), 201

# Fetch all files
@app.route('/api/files', methods=['GET'])
def get_files():
    cached_files = cache.get('files')
    if cached_files:
        return jsonify(eval(cached_files))

    files = File.query.all()
    file_list = [{
        'file_id': f.file_id,
        'file_name': f.file_name,
        'file_size_mb': float(f.file_size_mb)
    } for f in files]
    cache.set('files', str(file_list))
    return jsonify(file_list)

# Add a payment
@app.route('/api/payments', methods=['POST'])
def add_payment():
    data = request.json
    new_payment = Payment(
        user_id=data['user_id'],
        subscription_id=data['subscription_id'],
        amount=data['amount']
    )
    db.session.add(new_payment)
    db.session.commit()
    cache.delete('payments')  # Clear the cache
    return jsonify({'message': 'Payment added successfully'}), 201


# Fetch all payments
@app.route('/api/payments', methods=['GET'])
def get_payments():
    cached_payments = cache.get('payments')
    if cached_payments:
        return jsonify(eval(cached_payments))

    payments = Payment.query.all()
    payment_list = [{
        'payment_id': p.payment_id,
        'user_id': p.user_id,
        'subscription_id': p.subscription_id,
        'amount': float(p.amount),
        'payment_date': p.payment_date.isoformat()  # Serialize datetime to string
    } for p in payments]

    # Cache the result (string representation of the list)
    cache.set('payments', str(payment_list))
    return jsonify(payment_list)

# Fetch all subscriptions for the form dropdown
@app.route('/payment', methods=['GET'])
def payment_form():
    subscriptions = Subscription.query.all()  # Get all subscriptions
    return render_template('payment_form.html', subscriptions=subscriptions)

# Handle the payment form submission
@app.route('/payment/submit', methods=['POST'])
def submit_payment():
    # Retrieve form data
    user_id = request.form.get('user_id')
    subscription_id = request.form.get('subscription_id')
    amount = request.form.get('amount')

    # Ensure the data is valid and user exists
    user = User.query.get(user_id)
    subscription = Subscription.query.get(subscription_id)

    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('payment_form'))

    if not subscription:
        flash('Subscription not found!', 'error')
        return redirect(url_for('payment_form'))

    # Create the new payment record
    new_payment = Payment(
        user_id=user_id,
        subscription_id=subscription_id,
        amount=amount
    )

    try:
        db.session.add(new_payment)
        db.session.commit()
        flash('Payment processed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error processing payment: {str(e)}', 'error')

    return redirect(url_for('payment_form'))


# Update an existing user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json

    # Find the user in the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update user fields
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.password_hash = data.get('password_hash', user.password_hash)

    # Commit changes to the database
    db.session.commit()

    # Clear cache to reflect changes
    cache.delete('users')

    return jsonify({
        'message': 'User updated successfully',
        'user': {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
    })


# Update an existing payment
@app.route('/api/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    data = request.json

    # Find the payment in the database
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    # Update payment fields
    payment.amount = data.get('amount', payment.amount)

    # Commit changes to the database
    db.session.commit()

    # Clear cache to reflect changes
    cache.delete('payments')

    return jsonify({
        'message': 'Payment updated successfully',
        'payment': {
            'payment_id': payment.payment_id,
            'user_id': payment.user_id,
            'subscription_id': payment.subscription_id,
            'amount': float(payment.amount),
            'payment_date': payment.payment_date
        }
    })


# Șterge un utilizator
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    # Clear the cache
    cache.delete('users')

    return jsonify({"message": "User deleted successfully"})

# Șterge o plată
@app.route('/api/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    db.session.delete(payment)
    db.session.commit()

    # Clear the cache
    cache.delete('payments')

    return jsonify({"message": "Payment deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
