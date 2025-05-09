# PaperlessTranform

This REST API serves a PaperlessTranform and Machine Learning Development

## Requirements

Ensure you have the following installed:

- [Python 3.6+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

___

## Setup Project

1. **Create a virtual environment:**
    ```bash
    python3 -m venv env 
    or 
    python -m venv env
    ```

2. **Activate the virtual environment:**
    ```bash
    source env/bin/activate
    ```

3. **Install app dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

___

## Running the Application

1. **Start the database (PostgreSQL:alpine3.14):**
    ```bash
    docker-compose up
    ```

2. **Start the application:**
    ```bash
    export PYTHONDONTWRITEBYTECODE=1
    uvicorn app.main:app --reload
    ```

3. **Run a unit test:**
    ```bash
    python -m unittest development.tests.test_for
    ```

### Note:

You can configure the database using an environment variable:

```bash
export DB_URL="postgresql://user-name:password@host-name/database-name"
```

## Accessing the Application Locally

- The application will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc Documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Database Adminer: [http://127.0.0.1:9000](http://127.0.0.1:9000) (credentials: skatesham/skatesham-github)

If required, add the following headers for authentication on routes:

- `token`: my-jwt-token
- `x_token`: fake-super-secret-token

___

## Source Documentation

- [FastAPI](https://fastapi.tiangolo.com/)
- [Bigger Application](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy by FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/#sql-relational-databases)
- [SQLAlchemy 1.4](https://docs.sqlalchemy.org/en/14/tutorial/engine.html)
- [FastAPI "Real World Example App"](https://github.com/nsidnev/fastapi-realworld-example-app)

___