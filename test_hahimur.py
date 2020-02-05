import os
import unittest

from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase

from config import Config
from hahimur import app
from app import db
from app.models import Tournament, Team


class ApiTest(TestCase):
    """The class which all test case classes should inherit from"""
    TESTING = True

    def create_app(self):
        """Define test variables and initialize app."""
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TournamentsTests(ApiTest):

    ####################
    ### INSERT TESTS ###
    ####################
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

    ####################
    ### DELETE TESTS ###
    ####################
    def test_deletion(self):
        """Deleting should return an empty body and 204"""
        t = Tournament(name="Euro 2020")
        t.insert()
        response = app.test_client().delete(
            f'/tournaments/{t.uid}',
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')

    def test_wrong_deletion(self):
        """Deleting a non existing uid returns 422"""
        response = app.test_client().delete(
            '/tournaments/1',
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json["message"], "unprocessable entity")

    #################
    ### GET TESTS ###
    #################
    def test_existing_tournament(self):
        t = Tournament(name="New Tournament")
        t.insert()
        response = app.test_client().get(f'/tournaments/{t.uid}')
        self.assert200(response)

    def test_non_existing_tournamen(self):
        response = app.test_client().get(f'/tournamen/1')
        self.assert404(response)

    def test_get_tournaments(self):
        response = app.test_client().get(f'/tournaments')
        self.assert200(response)


class TeamsTests(ApiTest):

    ####################
    ### INSERT TESTS ###
    ####################
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

    def test_insert_with_bad_data(self):
        """Bad post data should return a 400"""
        team = {
            "no_name": "England",
            "no_flag": "http://usrl_to_flag.png"
        }
        response = app.test_client().post(
            '/teams',
            data=json.dumps(team),
            content_type='application/json'
        )

        self.assert400(response)
        self.assertEqual(response.json["message"], "Bad Request")

    ##################
    ### PATCH TEST ###
    ##################
    def test_patch_team(self):
        team = Team(name="England", flag="http://url_to_flag.png")
        team.insert()

        new_flag = {"flag": "http://different_url_to_flag.png"}
        response = app.test_client().patch(
            f'/teams/{team.uid}',
            data=json.dumps(new_flag),
            content_type='application/json'
        )

        team = Team.query.get_or_404(team.uid)

        self.assertEqual(team.flag, "http://different_url_to_flag.png")
        self.assertEqual(response.status_code, 204)

    def test_patch_non_existing_team(self):
        team = Team(name="England", flag="http://url_to_flag.png")
        team.insert()

        new_flag = {"flag": "http://different_url_to_flag.png"}
        response = app.test_client().patch(
            f'/teams/{team.uid + 1}',
            data=json.dumps(new_flag),
            content_type='application/json'
        )

        self.assert404(response)

    def test_get_team(self):
        team = Team(name="England", flag="http://url_to_flag.png")
        team.insert()

        response = app.test_client().get(f'/teams/{team.uid}')

        self.assert_200(response)
        self.assertEqual(team.name, response.json['name'])
        self.assertEqual(team.flag, response.json['flag'])

    def test_non_existing_team(self):
        response = app.test_client().get(f'/teams/1')
        self.assert404(response)


class ErrorsTests(ApiTest):

    def test_non_existing_page(self):
        response = app.test_client().get('/nothing-to-see-here')
        self.assert404(response)

    def test_method_not_allowed(self):
        response = app.test_client().post(f'/tournaments/1')
        self.assert405(response)


if __name__ == "__main__":
    unittest.main()
