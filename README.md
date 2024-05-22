# FastAPI Base Project

This project aims to build a base project to build RESTful APIs for production application using FastAPI. It's highly inspired by [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master).

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) for Python backend API.
  - [Pydantic](https://docs.pydantic.dev/) for data validation and settings management.
  - PostgreSQL as the SQL database
  - [Alembic](https://github.com/sqlalchemy/alembic) for database migration
- Tests with [Pytest](https://docs.pytest.org/en/8.0.x/).

## Get Started

0. Prerequisite:

- Install Postgresql by following [Set up database](#set-up-database)
- Install [Poetry](https://python-poetry.org/docs/#installation). Poetry is a tool for dependency management and packaging in Python.
- Install [Postico 2](https://eggerapps.at/postico2/) for easily visualizing PostgreSQL tables.

1. Clone the repository

```bash
git clone git@github.com:eclipsegst/fastapi.git
```

2. Create `.env`

Copy `.env.example` and rename to `.env`, update the values. Make sure the database name is same as the one you set up in [Set up database](#set-up-database) and also in `setup.sh`.

```bash
cp .env.example .env
```

3. Configuration

Install dependencies and initial database migration

```bash
./setup.sh
```

4. Run the app

```
./run.sh
```

or

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

If you get error,

```
ERROR:    [Errno 48] Address already in use
```

The server is running at port 8000, you can kill the process and try again.

Find pid for 8000

```bash
lsof -i tcp:8000
```

Kill the process,

```bash
kill -9 pid_from_above_step
```

Note: `poetry run` will run under poetry virtualenv.

6. Check it at http://127.0.0.1:8000
   You will get response like,

```
{
  "message": "Hello World"
}
```

7. Play CRUD operation through API docs

- http://127.0.0.1:8000/docs (use this)
  - http://127.0.0.1:8000/redoc

**Examples**

Step 1: Expand `/api/v1/users/register` to see user sign up endpoint

Step 2: Click `Try it out` and fill in the form, and click `Execute`

```json
{
  "password": "password",
  "email": "user01@example.com",
  "full_name": "user 01"
}
```

You will have response like,

```json
{
  "email": "user01@example.com",
  "is_active": true,
  "is_superuser": false,
  "name": null,
  "created_at": "2024-05-03T09:40:15.328062-07:00",
  "id": 11
}
```

Step 3: login `/api/v1/login/access-token`

Fill in username and password from above

You will get response like,

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU0NDU4MTUsInN1YiI6IjExIn0.F1IgIz15BUXsDP7V4AmZxaLpSCLTg2UibZxQoVYgHLQ",
  "token_type": "bearer"
}
```

Note: You might need to add `export PYTHONPATH=$(pwd):$PYTHONPATH` to `~/.bash_profile` if you get an error like "Cannot import or no app module".

## Manage dependencies

If you want to add a new package, add it to `pyproject.toml` and run

```bash
poetry lock
poetry install
```

## Set up database

Install postgresql

```
brew install postgresql
brew services start postgresql
brew services stop postgresql
```

Check if it's running,

```
~/$ ps -ef | grep postgres
  501 47222     1   0 10:11PM ??         0:00.03 /opt/homebrew/opt/postgresql@14/bin/postgres -D /opt/homebrew/var/postgresql@14
  501 47225 47222   0 10:11PM ??         0:00.00 postgres: checkpointer
  501 47226 47222   0 10:11PM ??         0:00.02 postgres: background writer
  501 47227 47222   0 10:11PM ??         0:00.01 postgres: walwriter
  501 47228 47222   0 10:11PM ??         0:00.00 postgres: autovacuum launcher
  501 47229 47222   0 10:11PM ??         0:00.00 postgres: stats collector
  501 47230 47222   0 10:11PM ??         0:00.00 postgres: logical replication launcher
  501 47400 47222   0 10:11PM ??         0:00.02 postgres: postgres abcxyz_db 127.0.0.1(51770) idle
  501 50722 13415   0 10:13PM ttys007    0:00.00 grep postgres
```

or use

```
$ brew services list
```

if it's running you will gets something like,

```
Name Status User File
postgresql@14 started root ~/Library/LaunchAgents/homebrew.mxcl.postgresql@14.plist
unbound none
```

If you get error like,

```
Error: Failure while executing; `/bin/launchctl bootstrap gui/501 /Users/hntlabs/Library/LaunchAgents/homebrew.mxcl.postgresql@14.plist` exited with 5.
```

find and remove the `postmaster.pid`

```bash
rm /opt/homebrew/var/postgresql@14/postmaster.pid
rm /usr/local/var/postgres@14/postmaster.pid
```

Step 1: create a database user `postgres`

Create user with password

```

createuser -U postgres -W

```

Step 2: Create database with name `fastapi_db`

```bash
createdb -U postgres -w fastapi_db
```

Step 3: Initial database migration

```bash
alembic upgrade head

python -m app.init_db
```

Note: You can also run the script to step 2 and step 3.

```
./setup.sh
```

### Database Migration

This project has initial migration set up, in `alembic` folder, if you want to set up from scrach, you can delete the folder and use the follow steps;

**Set up alembic**

```bash
alembic init alembic
```

it will produce,

- alembic/env.py:
  - where you 1) set up dabasebase connection and 2) provide models(tables) info to alembic. You can check that more details for the setup.
- alembic.ini

**Important:** if you set up alembic from scratch, you need to make sure those two lines or equivalent are in `alembic/env.py`, otherwise, the initial migration file won't identify existing models (tables).

```
from app.database import Base
from app import models  # noqa
```

**Initial migration**

Step 2: create a migration file

```bash
alembic revision --autogenerate -m "Initial migration"
```

It will create a new migration file in alembic/versions folder.

Step 3: run migration and push the version to alembic_version table.

```bash
alembic upgrade head
```

**Further Development**

If you add a new model in `app/models` and `app/models/__init__.py`, you need to run the following command to generate a new migration file.

```
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

## Testing

For a simple local test, we need to set up a separate database for test, e.g. `fastapi_db_test`.

**Steps**

- Change db name to `fastapi_db_test` in `.env`
- Run `./setup` to set up initial migration
- Create `.env.test.local` by copying `.env`
  - It will be loaded when running test in `app/core/config.py`
- Change back to original database name in `.env`
- Run `./scripts/test.sh`

Note: We can also use docker for setting up test environment.

## Run with Docker (Advanced)

1. Build image

```bash
docker build -t fastapi-image .
```

2. Run a container

```bash
docker run -d --name fastapi-container -p 80:80 fastapi-image
```

check container status,

```bash
docker logs -f fastapi-container
```

Some useful docker commands:

- docker container ls
- docker container stop container_id
- docker rm /fastapi-container
- docker image ls
- docker image rm image_id
- docker logs -f fastapi-container

3. Check it here:

- http://127.0.0.1
- API docs:
  - http://127.0.0.1/docs
  - http://127.0.0.1/redoc

## Notes

[1]: [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)

[2]: [uvicorn-gunicorn-fastapi-docker ](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/tree/master#quick-start)

[3]: [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master)

## License

FastAPI Base Project is licensed under the terms of the MIT license.
