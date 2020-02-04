import os
import unittest

from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase

from config import Config
from hahimur import app
from app import db
from app.models import Tournament


class TournamentsTests(TestCase):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TESTING = True

    def create_app(self):
        """Define test variables and initialize app."""
        return app
        
    def setUp(self):
        db.create_all()

    def test_insert(self):
        t = {
            "name": "Euro 2020",
        }
        response = app.test_client().post(
            '/tournaments',
            data=json.dumps(t),
            content_type='application/json'
        )

        # data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response.headers)

    def test_insert_without_name(self):
        t = {
            "no_name": "Euro 2020",
        }
        response = app.test_client().post(
            '/tournaments',
            data=json.dumps(t),
            content_type='application/json'
        )

        self.assert400(response)

    def test_non_existing_tournament(self):
        response = app.test_client().get('/tournaments/2')
        self.assert_404(response)


    def test_existing_tournament(self):
        t = Tournament(name="New Tournament")
        t.insert()
        response = app.test_client().get(f'/tournaments/{t.uid}')
        self.assert_200(response)

    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == "__main__":
    unittest.main()
