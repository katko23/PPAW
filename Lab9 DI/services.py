import json
from injector import inject
from flask_sqlalchemy import SQLAlchemy
import redis
from models import User, Payment

class UserService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_users(self):
        users = User.query.all()
        result = [{'user_id': u.user_id, 'username': u.username, 'email': u.email} for u in users]
        return result

    def add_user(self, username, email, password_hash):
        new_user = User(username=username, email=email, password_hash=password_hash)
        self.db.session.add(new_user)
        self.db.session.commit()

    def delete_user(self, user_id):
        user = User.query.get(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()

class PaymentService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_payments(self):
        payments = Payment.query.all()
        return [{'payment_id': p.payment_id, 'user_id': p.user_id, 'amount': float(p.amount)} for p in payments]

    def add_payment(self, user_id, subscription_id, amount):
        new_payment = Payment(user_id=user_id, subscription_id=subscription_id, amount=amount)
        self.db.session.add(new_payment)
        self.db.session.commit()

    def delete_payment(self, payment_id):
        payment = Payment.query.get(payment_id)
        if payment:
            self.db.session.delete(payment)
            self.db.session.commit()

class CacheService:
    @inject
    def __init__(self, cache: redis.Redis):
        self.cache = cache

    def get_or_cache(self, key, fetch_function):
        cached_data = self.cache.get(key)
        if cached_data:
            return json.loads(cached_data)
        data = fetch_function()
        self.cache.set(key, json.dumps(data))
        return data

    def clear(self, key):
        self.cache.delete(key)
