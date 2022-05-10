# FastAPI template

## How to set environment

Create the virtualenv inside the project’s root directory.

```
poetry config virtualenvs.in-project true
poetry config virtualenvs.create true
```

[virtualenvs.in-project](https://python-poetry.org/docs/configuration/#virtualenvsin-project)

The shell command spawns a shell, according to the $SHELL environment variable, within the virtual environment. If one doesn’t exist yet, it will be created.

```
poetry shell
```

The install command reads the pyproject.toml file from the current project, resolves the dependencies, and installs them.

```
poetry install
```

if Installing mysqlclient: Failed

```
sudo apt-get install python3.9-dev libmysqlclient-dev
```

database

```
docker-compose -f docker/docker-compose.yml up -d
```

## How to use it

```
poetry run alembic revision --autogenerate -m "[description]"
poetry run alembic upgrade head
```

```
poetry run start
```
