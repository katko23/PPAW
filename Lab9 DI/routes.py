from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from injector import inject
from services import UserService, PaymentService, CacheService

api = Blueprint('api', __name__)

# ✅ Home Page (Renders HTML)
@api.route('/')
def home(user_service: UserService = inject(UserService)):
    users = user_service.get_all_users()
    return render_template('index.html', users=users)

# ✅ User Management Pages
@api.route('/users/add', methods=['GET', 'POST'])
def add_user_page(user_service: UserService = inject(UserService)):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_service.add_user(username, email, password)
        flash('User added successfully!', 'success')
        return redirect(url_for('api.home'))
    return render_template('add_user.html')

# ✅ Payments Page
@api.route('/payments/add', methods=['GET', 'POST'])
def add_payment_page(payment_service: PaymentService = inject(PaymentService)):
    if request.method == 'POST':
        user_id = request.form['user_id']
        subscription_id = request.form['subscription_id']
        amount = request.form['amount']
        payment_service.add_payment(user_id, subscription_id, amount)
        flash('Payment added successfully!', 'success')
        return redirect(url_for('api.home'))
    return render_template('payment_form.html')

# ✅ API: Fetch All Users
@api.route('/api/users', methods=['GET'])
def get_users(user_service: UserService = inject(UserService), cache_service: CacheService = inject(CacheService)):
    users = cache_service.get_or_cache('users', user_service.get_all_users)
    return jsonify(users)

# ✅ API: Add User
@api.route('/api/users', methods=['POST'])
def add_user(user_service: UserService = inject(UserService), cache_service: CacheService = inject(CacheService)):
    data = request.json
    user_service.add_user(data['username'], data['email'], data['password_hash'])
    cache_service.clear('users')
    return jsonify({'message': 'User added successfully'}), 201

# ✅ API: Fetch All Payments
@api.route('/api/payments', methods=['GET'])
def get_payments(payment_service: PaymentService = inject(PaymentService), cache_service: CacheService = inject(CacheService)):
    payments = cache_service.get_or_cache('payments', payment_service.get_all_payments)
    return jsonify(payments)

# ✅ API: Add Payment
@api.route('/api/payments', methods=['POST'])
def add_payment(payment_service: PaymentService = inject(PaymentService), cache_service: CacheService = inject(CacheService)):
    data = request.json
    payment_service.add_payment(data['user_id'], data['subscription_id'], data['amount'])
    cache_service.clear('payments')
    return jsonify({'message': 'Payment added successfully'}), 201

# ✅ API: Delete User
@api.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id, user_service: UserService = inject(UserService), cache_service: CacheService = inject(CacheService)):
    user_service.delete_user(user_id)
    cache_service.clear('users')
    return jsonify({"message": "User deleted successfully"}), 200

# ✅ API: Delete Payment
@api.route('/api/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id, payment_service: PaymentService = inject(PaymentService), cache_service: CacheService = inject(CacheService)):
    payment_service.delete_payment(payment_id)
    cache_service.clear('payments')
    return jsonify({"message": "Payment deleted successfully"}), 200
