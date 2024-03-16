# Event Manager API (POC)

## Description
This is a proof of concept application than manages events the simplest way,
using Django and Rest Framework, currently working only in development/debug environment.

## Getting Started

### Dependencies
- Python
- Pip
- Pipenv

### Setup

#### Basic
Create Pipenv virtual environment with Python dependencies:
```shell
pipenv install --dev
```

Run migrations:
```shell
python src/manage.py migrate
```

Create superuser (for accessing admin):
```shell
python src/manage.py createsuperuser
```

### Test

Run tests:
```shell
pytest ./src
```

### Usage

#### Basic
Run server:
```shell
python src/manage.py runserver
```

Browse admin on Django page:
```
http://localhost:8000/admin/
```

Browse endpoints on API doc page:
```
http://localhost:8000/docs/
```

#### API

Register a new user:
```
POST /api/v1/users/
```

Obtain access/refresh token:
```
POST /api/v1/jwt/create/
```

Refresh a token:
```
POST /api/v1/jwt/refresh/
```

Verify a token:
```
POST /api/v1/jwt/verify/
```

Finally, manage events consuming the endpoints under the `events` group.
