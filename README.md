# PaperlessTranform

This REST API serves a PaperlessTranform Service and Machine Learning Development

## Requirements

Ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Ollama](https://ollama.com/)

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