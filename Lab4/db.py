from sqlalchemy import Integer, String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base
from flask_sqlalchemy import SQLAlchemy

# Create a base class for declarative models
Base = declarative_base()

# Initialize the database
db = SQLAlchemy(model_class=Base)


# Define ORM models using mapped_column and Mapped

class User(Base):
    __tablename__ = 'users'

    # Define columns using mapped_column and Mapped
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=db.func.now())

    # Relationships
    files = db.relationship('File', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)


class Subscription(Base):
    __tablename__ = 'subscriptions'

    # Define columns using mapped_column and Mapped
    subscription_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    max_file_size_mb: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=db.func.now())

    # Relationships
    payments = db.relationship('Payment', backref='subscription', lazy=True)


class File(Base):
    __tablename__ = 'files'

    # Define columns using mapped_column and Mapped
    file_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('users.user_id'), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_mb: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    uploaded_at: Mapped[DateTime] = mapped_column(DateTime, default=db.func.now())


class Payment(Base):
    __tablename__ = 'payments'

    # Define columns using mapped_column and Mapped
    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('users.user_id'), nullable=False)
    subscription_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('subscriptions.subscription_id'),
                                                 nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    payment_date: Mapped[DateTime] = mapped_column(DateTime, default=db.func.now())


# Function to initialize the database and create tables
def initialize_db(app):
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {str(e)}")
