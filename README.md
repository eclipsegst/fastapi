# FastAPI Base Project
This project aims to build a base project to build RESTful APIs for production application using FastAPI. It's highly inspired by [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master).

## Get Started
1. Clone the repository
```bash
git clone git@github.com:eclipsegst/fastapi.git
```

2. Install dependencies
```bash
poetry lock
poetry install
```
Add a new dependency to `pyproject.toml`

3. Create `.env`

Here is an example,
```
SERVER_NAME=your_server_name
SERVER_HOST=http://localhost
PROJECT_NAME=your_project_name

FIRST_SUPERUSER=your_superuser_email@example.com
FIRST_SUPERUSER_PASSWORD=your_superuser_password

POSTGRES_HOST=localhost
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db_name
POSTGRES_PORT=5432

SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=""
SMTP_PASSWORD=""
EMAILS_FROM_EMAIL="info@example.com"
```
4. [Set up database](#set-up-database)

5. Run the app
```
./run.sh
```
or
```bash
poetry run uvicorn app.main:app --reload
```
6. Check it
- http://127.0.0.1:8000
- API docs: 
  - http://127.0.0.1:8000/docs
  - http://127.0.0.1:8000/redoc

## Docker

1. Build image
```bash
docker build -t fastai-image .
```
2. Run a container

```bash
docker run -d --name fastai-container -p 80:80 fastai-image
```
3. Check it here: 
  - http://127.0.0.1
  - API docs: 
    - http://127.0.0.1/docs
    - http://127.0.0.1/redoc

## Set up database
Install postgresql
```
brew install postgresql
brew services start postgresql
brew services stop postgresql
```
Check if it's running
```
ps -ef | grep postgres
```
Create user with password
```
createuser -U postgres -W
```
Create database with name `fastapi_db`
```
createdb -U postgres -w fastapi_db
```
Set up initial data
```
./setup.sh
```
### Database Migration

Initial migration
```
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

Further Developing
```
alembic revision --autogenerate -m "description of your change"
alembic upgrade head
```

## Testing

For a simple local test, we need to set up a separate database for test, e.g. `fastapi_db_test`.

## Steps
- Change db name to `fastapi_db_test` in `.env`
- Run `./setup` to set up initial migration
- Create `.env.test.local` by copying `.env`
  - It will be loaded when running test in `app/core/config.py`
- Change back to original database name in `.env`
- Run `./scripts/test.sh`

Note: We can also use docker for setting up test environment.

## Notes
[1]: [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)

[2]: [uvicorn-gunicorn-fastapi-docker ](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/tree/master#quick-start)

[3]: [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master)
