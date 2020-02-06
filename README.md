# Hahimur-flask
Backend for Hahimur

## Why "Hahimur"?
On every major football tournament, my friends and I are trying to predict the outcomes.
We usually use excel sheets to do it, and I decided to create a website for us.
For the front-end I'm using Elm, and you can see the first part of it, where you can start creating you predictions, [here](https://hahimur.com).

## Live URL
https://hahimur-api.herokuapp.com/

## Installation

Clone the repository, create a virtualenv, preferably with python3.7.6, and install all the dependencies.

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


## Tokens for calling the live site:

#### Admin Token
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wTTBOamhHUVRoRVJVUTVOVUpGUWtFMk5USkNOVEJCTURRelJFUkNNVGRGT0VWRE1rSTJOQSJ9.eyJpc3MiOiJodHRwczovL2lkYW5tZWwuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA4NDI2ODEzNDI4NDAyMjA2OTkyIiwiYXVkIjpbImh0dHBzOi8vaGFoaW11ci5jb20iLCJodHRwczovL2lkYW5tZWwuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4MDk0ODQ5MCwiZXhwIjoxNTgxMDM0ODkwLCJhenAiOiJMMlIzalVGaVRaRkptYXZ3VGNWUktxaDdMOUVPU0xETiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dG91cm5hbWVudHMiLCJnZXQ6dGVhbXMiLCJnZXQ6dG91cm5hbWVudHMiLCJwYXRjaDp0ZWFtcyIsInBvc3Q6dGVhbXMiLCJwb3N0OnRvdXJuYW1lbnRzIl19.RUOwEBioIPgZwIjz82uSwLVyJJXbDqEYOaa0ZKBbyhCAL3XZkjVoEKJTCyPfy9CJ52YoPX6BQukiyTZzbgq6REQ90uRtrCy_ZyX8ZkEDBQDXh7uuaNvYmTMCCBB86i_OGFLkvAQlUoxKTfnr8QHa5JR2SjNg9Q5ZBOzNB6RslRLT0UH8TiKuEOmRYYR-fVZHb06rSefSISjzQiNkhKB2ls1KDAQooKSfRaCnKxuJk8JQZGGvTRHkD56UF-_wWiFHqa6cIcc6lUGXzO4RRKiLQZFLlnXLzeFaJZ9Q0hr-z9c5CgV9kcB7oWlFtUxS1pQC6SpKm8hjQoqPaSYr6vAVSg
```

#### User Token
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wTTBOamhHUVRoRVJVUTVOVUpGUWtFMk5USkNOVEJCTURRelJFUkNNVGRGT0VWRE1rSTJOQSJ9.eyJpc3MiOiJodHRwczovL2lkYW5tZWwuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NTQ1MTIzMTkzMzc3NDQzOTQxIiwiYXVkIjpbImh0dHBzOi8vaGFoaW11ci5jb20iLCJodHRwczovL2lkYW5tZWwuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4MDk0OTAwOCwiZXhwIjoxNTgxMDM1NDA4LCJhenAiOiJMMlIzalVGaVRaRkptYXZ3VGNWUktxaDdMOUVPU0xETiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6dGVhbXMiLCJnZXQ6dG91cm5hbWVudHMiXX0.QZohgLbFoW7xS7fe80Pq-BzOZA-917188qs2fLH6ktOKNUpGFBwBhK5k122D1GjCz2zUrrCEAZsf8_2eTjvObSAJyNVww6CKZIXY4AwiuHF76rnREDyaOqhF7R2Ns2h8BDPLC8RwbrprI4pBMhvXXfnK3h6BhkrlaYta63RTNzjD8POpbBLnL5-ypm54eNdqaoUA5Fuc6Q8ZSL6ooQ7Cpwh_9YJNlOoYXSPuTsozyV0KWWwAT1kaWrrS4Ql3Vo83H3_6Ev3TJRF2b_iL9b7H8q1Um-J8XaOgpFn1zDJKPJVuVouz97GQE5PgMdmeFLgwQKLVYsq0olJF1AHHRuVbpA
```


