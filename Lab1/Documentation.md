# **Entities, UML Diagrams, and System Design**

## **Entities and Descriptions**

### **User**:
Represents a user in the system.
- Attributes:
  - `user_id` (Primary Key): Unique identifier for the user.
  - `username`: The user's name.
  - `email`: The user's email address.
  - `password_hash`: Encrypted password for authentication.
  - `created_at`: Timestamp of user creation.

### **Subscription**:
Represents a subscription plan.
- Attributes:
  - `subscription_id` (Primary Key): Unique identifier for the subscription.
  - `name`: Name of the subscription plan.
  - `price`: Price of the subscription.
  - `max_file_size_mb`: Maximum file size allowed for the plan.
  - `created_at`: Timestamp of plan creation.

### **File**:
Represents a file uploaded by a user.
- Attributes:
  - `file_id` (Primary Key): Unique identifier for the file.
  - `user_id` (Foreign Key): ID of the user who uploaded the file.
  - `file_name`: Name of the file.
  - `file_size_mb`: Size of the file in megabytes.
  - `uploaded_at`: Timestamp of when the file was uploaded.

### **Payment**:
Represents a payment transaction.
- Attributes:
  - `payment_id` (Primary Key): Unique identifier for the payment.
  - `user_id` (Foreign Key): ID of the user making the payment.
  - `subscription_id` (Foreign Key): ID of the subscription purchased.
  - `amount`: Amount paid.
  - `payment_date`: Timestamp of the payment.

## **UML Diagrams**

### **Class Diagram**
```plaintext
+-----------------+        +---------------------+        +---------------+
|     User        |        |    Subscription     |        |    Payment    |
+-----------------+        +---------------------+        +---------------+
| user_id (PK)    |        | subscription_id (PK)|        | payment_id (PK)|
| username        |        | name               |        | user_id (FK)  |
| email           |        | price              |        | subscription_id|
| password_hash   |        | max_file_size_mb   |        | amount         |
| created_at      |        | created_at         |        | payment_date   |
+-----------------+        +---------------------+        +---------------+
         |                            |
         |                            |
         +----------------------------+        +-------------------+
                                        --->   |      File         |
                                               +-------------------+
                                               | file_id (PK)      |
                                               | user_id (FK)      |
                                               | file_name         |
                                               | file_size_mb      |
                                               | uploaded_at       |
                                               +-------------------+
```

### **Use Case Diagram 1: User Subscription Management**
- Actors: User, System
- Description: A user selects a subscription plan and completes a payment.
```plaintext
[User] --> (Choose Subscription)
(Choose Subscription) --> (Complete Payment)
(Complete Payment) --> [System]

```
(images\img.png)

### **Use Case Diagram 2: File Upload Management**
- Actors: User, System
- Description: A user uploads a file within the allowed size limit of their subscription plan.
```plaintext
[User] --> (Login)
(Login) --> (Upload File)
(Upload File) --> (Check File Size)
(Check File Size) --> [System]
```
(images\img_1.png)

### **Use Case Diagram 3: ORM, API, and Cache Integration**
- Actors: User, System, Redis Cache
```plaintext
[User] --> (Send API Request)
(Send API Request) --> (Flask App)
(Flask App) --> (Query ORM via SQLAlchemy)
(Query ORM via SQLAlchemy) --> (Check Redis Cache)
(Check Redis Cache) --> [Redis Cache]
(Query ORM via SQLAlchemy) --> (Fetch from Database)
(Fetch from Database) --> (Update Redis Cache)
```
(images\img_2.png)


## **Database Structure**

### `users` Table:
```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash CHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `subscriptions` Table:
```sql
CREATE TABLE subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    max_file_size_mb INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `files` Table:
```sql
CREATE TABLE files (
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size_mb DECIMAL(10, 2) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### `payments` Table:
```sql
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subscription_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);
```

## **ORM and API Details**

### **ORM Integration (SQLAlchemy)**
- Define SQLAlchemy models for each entity (User, Subscription, File, Payment).
- Use Flask SQLAlchemy to interact with the database.
- Example:
```python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_payment'
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

```

### **API Implementation (Flask)**
- Use Flask to create RESTful endpoints.
- Example:
```python
from flask import Flask, jsonify, request

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'user_id': u.user_id,
        'username': u.username,
        'email': u.email
    } for u in users])

if __name__ == '__main__':
    app.run(debug=True)
```

### **Redis Cache Integration**
- Use Redis for caching database queries.
- Example:
```python
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/api/files', methods=['GET'])
def get_files():
    cached_files = cache.get('files')
    if cached_files:
        return jsonify(eval(cached_files))  # Cached response

    files = File.query.all()
    file_list = [{
        'file_id': f.file_id,
        'file_name': f.file_name,
        'file_size_mb': f.file_size_mb
    } for f in files]
    cache.set('files', str(file_list))  # Cache result
    return jsonify(file_list)
```

## **System Setup**

1. **Framework**:
   - Install Flask:
     ```bash
     pip install flask flask-sqlalchemy redis
     ```

2. **Web Server**:
   - Install and configure a web server like Nginx or Apache.

3. **Database Server**:
   - Install MySQL Server and set up the `db_payment` database.

4. **Redis**:
   - Install Redis for caching.
     ```bash
     sudo apt update
     sudo apt install redis
     ```

5. **Testing**:
   - Test the application using the provided Flask APIs.

---


