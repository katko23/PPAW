# PPAW - A Short Course in USV

## Documentation

### Proiectare

#### Paradigme utilizate
- **MVC (Model-View-Controller)**: Separates the application into three interconnected components to organize the code efficiently.
- **API (Application Programming Interface)**: Exposes endpoints for communication between the frontend and backend.
- **ORM (Object-Relational Mapping)**: Uses SQLAlchemy to interact with the database efficiently, applying Code First principles.

#### De ce au fost alese?
- **MVC** ensures modularity, maintainability, and scalability.
- **API** enables integration with external services and provides flexibility for different client applications.
- **ORM Code First** allows defining database structures through Python models, ensuring better control over migrations and data integrity.

#### Arhitectura aplicației
- **Frontend**: HTML templates rendered by Flask for basic UI interactions.
- **Backend**: Flask application handling requests, user authentication, payments, and file uploads.
- **Database**: MySQL with SQLAlchemy ORM for efficient data management.
- **Cache**: Redis used to store frequently accessed data, reducing database queries.
- **Logging**: Server logs stored in a log file for monitoring and debugging.

### Implementare

#### Business layer
- Handles user management, payments, and file storage logic.
- Implements soft delete mechanisms for reversible deletions.
- Ensures data validation and consistency using ORM constraints.

#### Librarii suplimentare utilizate
- **Flask**: Web framework for handling HTTP requests.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **Redis**: Caching system to improve performance.
- **Werkzeug**: Provides utilities for secure file uploads.
- **Logging**: Built-in Python module for recording server activities.
- **Pymysql**: MySQL adapter for Python to connect with the database.

#### Secțiuni de cod sau abordări deosebite
- **Soft delete implementation**: Instead of deleting records, an `is_deleted` flag is used to allow recovery.
- **Caching with Redis**: Stores user and subscription data for fast retrieval.
- **Secure file uploads**: Uses `secure_filename()` to prevent directory traversal attacks.

### Utilizare

#### Pașii de instalare

##### Instalare și configurare pentru programator
1. Clonează repository-ul: `git clone <https://github.com/katko23/PPAW>`
2. Instalează dependințele: `pip install -r requirements.txt`
3. Configurează baza de date MySQL și actualizează `SQLALCHEMY_DATABASE_URI` în `config.py`.
4. Rulează migrațiile: `flask db upgrade`
5. Pornește aplicația: `python app.py`

##### Instalare și configurare la beneficiar
1. Descarcă aplicația și instalează Python 3.
2. Configurează baza de date MySQL cu schema necesară.
3. Rulează aplicația folosind `python app.py`.
4. Accesează interfața web la `http://localhost:5000/`.

#### Mod de utilizare
- **Adăugare utilizatori**: Accesează `/users/add` și completează formularul.
- **Adăugare plăți**: Accesează `/payments/add` și selectează utilizatorul și abonamentul.
- **Vizualizare fișiere**: Accesează `/api/files` pentru a lista fișierele încărcate.
- **Upload fișiere**: Accesează `/upload` și selectează fișierul dorit.
