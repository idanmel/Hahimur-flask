# Hahimur-flask
Backend for Hahimur

## Why "Hahimur"?
On every major football tournament, my friends and I are trying to predict the outcomes.
We usually use excel sheets to do it, and I decided to create a website for us.
For the front-end I'm using Elm, and you can see the first part of it, the form to fill, [here](https://hahimur.com).

## Live URL
https://hahimur-api.herokuapp.com/

## Installation

Clone the repository, then create a virtualenv, preferably with python3.7.6, install all the dependencies.

```bash
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
AUTH0_DOMAIN=confidentioal
API_AUDIENCE=confidentioal
ALGORITHMS=confidentioal
```

## Running the server locally
```bash
cd Hahimur-flask
source venv/bin/activate
flask run
```

## Running the tests locally
```
cd Hahimur-flask
source venv/bin/activate
python test_hahimur.py
```

The tests include JWT tokens for the two roles.


## RBAC roles
Here are the roles and their permissions

#### User
- get:tournaments
- get:teams

#### Admin
- get:tournaments
- post:tournaments
- delete:tournaments
- get:teams
- post:teams
- patch:teams

## API Endpoints
```
GET    '/tournaments'
POST   '/tournaments'
DELETE '/tournaments/<int>'
GET    '/teams/<int>'
POST   '/teams/'
Patch  '/teams/<int>'
```


#### GET '/tournaments'
- Fetches a list of tournaments
- Request Arguments: None
- Returns: A list of objects of {id: int, name: text}. 
```json
[
    {"uid": 1, "name": "Euro 2020"},
    {"uid": 2, "name": "World Cup 2022"},
    {"uid": 3, "name": "Euro 2024"},
    ...
]
```
#### POST '/tournaments'
- Creates a new tournament
- ContentType: 'application/json'
- Data: {"name": text}
- Returns: 201 with a "Location" header containing the URL of the created tournament and an empty body

#### DELETE '/tournaments/<int>'
- Deletes a tournament
- Request Arguments: Tournament UID
- Returns on success: 204 with an empty body
- Returns 422 when given the wrong UID

#### GET '/teams/<int>'
- Fetches a team
- Request Argument: Team UID
- Returns an object of {"uid": int, "name": text, "flag": text}
- Returns 404 when given the wrong uid
```json
{
    "uid": 1,
    "name": "Brazil",
    "flag": "url_of_flag"
}
``` 

#### POST '/teams/'
- Creates a new team
- ContentType: 'application/json'
- Data: {"name": text, "flag": text}
- Returns: 201 with a "Location" header containing the URL of the created team and an empty body

#### Patch '/teams/<int>'
- Changes an existing Team
- ContentType: 'application/json'
- Data: an object containing "name", "flag", or both.
- Returns: 204 with an empty body
