# Hahimur-flask
Backend for Hahimur

## Installation

Clone the repository, then create a virtualenv, preferably with python3.7.6, install all the dependencies.

```
git clone git@github.com:idanmel/Hahimur-flask.git
cd Hahimur-flask
virtualenv --python=/usr/bin/python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
touch .env
```

Create an sql database for Hahimur to work with.

The .env file is where you will place all your environment variables. For example:
```
FLASK_APP=hahimur.py
FLASK_ENV=development
SECRET_KEY=TOP_secret
DATABASE_URL=postgresql://hahimur:hahimur@localhost/hahimur
```