# Financial Transactions Management API

## Overview

This project implements a REST API for managing financial transactions between participants. It allows users to:
- **Transaction Management**: API to create financial transactions specifying the total amount, senders, receivers, and their respective shares.
- **Balance Retrieval**: Get the balance of any user, considering all their previous transactions.
- **Balance History**: View the change in balance within a specified date range.

## Technology Stack
- **Backend Framework**: Django_5.1.1 with Django REST Framework (DRF)
- **Database**: PostgreSQL (for production), SQLite (for local development)
- **Authentication**: Django's default authentication (can be extended to use JWT or OAuth)
- **Containerization**: Docker (for production deployment)
- **Environment Management**: Python `venv`, `pipenv`, or `poetry`
- **Deployment**: Docker Compose (for production setup), Gunicorn, Nginx
- **Transaction Safety**: Atomic operations for database transactions

## Prerequisites
- Python 3.8 or higher
- PostgreSQL (for production)
- Docker & Docker Compose (for production)
- Git

## Local Development Setup

### 1. Clone the repository
```bash
$ git clone https://github.com/yourusername/finmanager.git
$ cd finmanager
```
### 2. Crate virtual environment & Install dependencies
```bash
$ python3 -m venv venv
$ source venv/bin/activate 
$ pip install -r requirements.txt
```

### 3. Setup .ENV, example of .ENV file is included in project directory

    DEBUG=True
    SECRET_KEY=your_secret_key_here

If everything is configured fine, you can now migrate and start DEV server
```bash
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

### 4. Access the API 
The API can be tested using tools like Postman or curl you can also check it from browser
http://127.0.0.1:8000/

## Production environment setup
### 1. Set up the environment variables for production +
Copy/rename and update .env_sample file in project root dir to .env, with same folder as 
settings.py, below the example setup, you can add more settings
```aiignore
DEBUG=False
SECRET_KEY=your_secure_secret_key
DATABASE_URL=postgres://username:password@hostname:port/dbname
```
### 2. Setup Docker & Build/Run Containers
```bash
  $ git clone https://github.com/ashyrbaew/csv_to_db.git
  $ docker-compose build .
  $ docker-compose up
```
