# Initiating a Database Using Migrations and Python Code

## Requirements

Before starting, I install the required packages:

```bash
pip install flask flask_sqlalchemy alembic pymysql
```

### 1. Set Up the Flask Application and Database Models

Create a file named `app.py` to define my application and models.

```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Database URI configuration (adjust the credentials as needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy object
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

```

### 2. Initialize Alembic

Alembic helps manage database migrations.
To configure Alembic I run the following command in my terminal:

```bash
alembic init alembic
```

This creates an `alembic` directory and the configuration file `alembic.ini`.

### 3. Configure Alembic for Flask App

In the `alembic.ini` file, configure the SQLAlchemy URL to point to the database:

```ini
# alembic.ini

[alembic]
script_location = alembic
sqlalchemy.url = mysql+pymysql://root:password@localhost/db_name  # Adjust this
```

Then, modify the `env.py` file inside the `alembic` directory to work with Flask’s `SQLAlchemy`:

```python
# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app import db  # Import the SQLAlchemy instance

# Get the target metadata
target_metadata = db.metadata

# Configuration for the database connection
config = context.config
fileConfig(config.config_file_name)
connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool
)

# Run migrations online
def run_migrations_online():
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if __name__ == '__main__':
    run_migrations_online()
```

### 4. Create a Migration

I generate a migration script by running the following Alembic command:

```bash
alembic revision --autogenerate -m "Initial migration"
```

This generate a migration file inside the `alembic/versions` directory.

### 5. Apply the Migration

To apply the migration to the database, I run:

```bash
alembic upgrade head
```

This has applied all pending migrations and create the tables defined in the models.

### 6. Run the Application

To run the Flask app and initiate the database along with some data:

```bash
python app.py
```

This will create the necessary tables and add initial data to the database.

