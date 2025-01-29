from flask import request
from flask_sqlalchemy import SQLAlchemy
import redis
from services import UserService, PaymentService, CacheService

def configure_container(binder):
    from models import db
    cache = redis.Redis(host='localhost', port=6379, db=0)

    # ✅ Bind DB & Cache
    binder.bind(SQLAlchemy, to=db, scope=request)
    binder.bind(redis.Redis, to=cache, scope=request)

    # ✅ Bind Services
    binder.bind(UserService, to=UserService(db), scope=request)
    binder.bind(PaymentService, to=PaymentService(db), scope=request)
    binder.bind(CacheService, to=CacheService(cache), scope=request)
