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

    def test_insert_trounament(self):
        """Inserting successfully should return 200 and the correct location
        header"""
        t = {
            "name": "Euro 2020",
        }
        response = app.test_client().post(
            '/tournaments',
            data=json.dumps(t),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response.headers)
        self.assertEqual(
            response.headers["Location"], f"http://localhost/tournaments/1"
        )

    def test_deletion(self):
        """Deleting should return an empty body and 204"""
        t = Tournament(name="Euro 2020")
        t.insert()
        response = app.test_client().delete(
            f'/tournaments/{t.uid}',
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')

    def test_existing_tournament(self):
        t = Tournament(name="New Tournament")
        t.insert()
        response = app.test_client().get(f'/tournaments/{t.uid}')
        self.assert_200(response)

    def test_get_tournaments(self):
        response = app.test_client().get(f'/tournaments')
        self.assert_200(response)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TeamsTests(TestCase):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    def create_app(self):
        """Define test variables and initialize app."""
        return app

    def setUp(self):
        db.create_all()

    def test_insert_team(self):
        """Inserting successfully should return 200 and the correct location
        header"""
        team = {
            "name": "England",
            "flag": "http://usrl_to_flag.png"
        }
        response = app.test_client().post(
            '/teams',
            data=json.dumps(team),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response.headers)
        self.assertEqual(
            response.headers["Location"], f"http://localhost/teams/1"
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class ErrorsTests(TestCase):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TESTING = True

    def create_app(self):
        """Define test variables and initialize app."""
        return app

    def setUp(self):
        db.create_all()

    def test_non_existing_page(self):
        response = app.test_client().get('/tournaments/5')
        self.assert_404(response)

    def test_method_not_allowed(self):
        response = app.test_client().post(f'/tournaments/1')
        self.assert_405(response)

    def test_wrong_deletion(self):
        """Deleting a non existing uid returns 422"""
        response = app.test_client().delete(
            '/tournaments/1',
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json["message"], "unprocessable entity")

    def test_insert_with_bad_data(self):
        """Bad post data should return a 400"""
        t = {
            "no_name": "Euro 2020",
        }
        response = app.test_client().post(
            '/tournaments',
            data=json.dumps(t),
            content_type='application/json'
        )

        self.assert400(response)
        self.assertEqual(response.json["message"], "Bad Request")

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
