## Backend API build and configuration

API source code. Written on python using FastAPI, SQLITE, SQLAlchemy, Alembic, PyTest, JWT

### Requirements

1. Python 3.10 
2. Python PIP ([https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/))
3. Python venv module ([https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/))


### Installation

1. Clone code from the repository to the local machine

```bash
$ git clone git@github.com:Slavian2015/FastAPIPostAuth.git path_on_locahost
```

2. CD into the project folder
3. Create python virtual environment

```bash
$ python3 -m venv ./venv
```

4. Activate virtual environment


```bash
$ source ./venv/bin/activate
```

5. Install application dependencies


```bash
$ pip install -r requirements.txt
```

### Configuration

1. Copy .env.dist file to the .env file


```bash
$ cp .env.dist .env
```

2. Configure .env file
- AUTH_SECRET - Random string that will be used as a key for the hashing
- NUMBER_OF_USERS - Random integer that will be used in test db users creation
- MAX_POSTS_PER_USER - Random integer that will be used in test db post creation
- MAX_LIKES_PER_USER - Random integer that will be used in test db likes creation

### Database migration

1. Copy .env.dist file to the .env file


```bash
$ alembic upgrade head
```

### Testing

1. Unit test suite

```bash
$ python3 -m pytest tests/unit
```

2. Functional test suite

```bash
$ python3 -m pytest tests/functional
```
All tests should pass successfully to consider setup is finished and works

### Running local server

1. Start uvicorn service

```bash
$ uvicorn src.api.application:api --host=localhost --port=8080
```

### Create DB test data

1. Run python bot

```bash
$ python3 demo_db/bot.py
```
