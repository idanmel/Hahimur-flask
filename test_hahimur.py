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

    def create_app(self):
        """Define test variables and initialize app."""
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        app.config["TESTING"] = True
        os.environ["NO_AUTH"] = "1"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TournamentsTests(ApiTest):

    ##################
    ### POST TESTS ###
    ##################
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
        t = Tournament(name="New Tournament")
        t.insert()
        response = app.test_client().get(f'/tournaments')
        self.assert200(response)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "New Tournament")


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

    #################
    ### GET TESTS ###
    #################
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


class RolesTests(ApiTest):
    admin_headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wTTBOamhHUVRoRVJVUTVOVUpGUWtFMk5USkNOVEJCTURRelJFUkNNVGRGT0VWRE1rSTJOQSJ9.eyJpc3MiOiJodHRwczovL2lkYW5tZWwuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA4NDI2ODEzNDI4NDAyMjA2OTkyIiwiYXVkIjpbImh0dHBzOi8vaGFoaW11ci5jb20iLCJodHRwczovL2lkYW5tZWwuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4MTc2NjM0MSwiZXhwIjoxNTgxODUyNzQxLCJhenAiOiJMMlIzalVGaVRaRkptYXZ3VGNWUktxaDdMOUVPU0xETiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dG91cm5hbWVudHMiLCJnZXQ6dGVhbXMiLCJnZXQ6dG91cm5hbWVudHMiLCJwYXRjaDp0ZWFtcyIsInBvc3Q6dGVhbXMiLCJwb3N0OnRvdXJuYW1lbnRzIl19.r4dU7V19g7MiHhRW4VlvMHdnPJA7XmhFu-YfVdfavouF-W36hVVpwGb7vWgAd0jpKJow3fQ9YaOHDOjmLQ-m-FE8XDj3lxWuMi9xEAWQFMiWrWGx0BDdPcCwE7KXDBWQB37A_0Tq1IGz3xwbZXvpIB5A0l4OfL4vPTWnU0waR4-iuxtNe8xppzs10gVmka1kytwauqoL6gkI0OMFKjjmYQfvTYtgCMbYMVI8sPCokMKuBaPmcbRcNgV_-1mQ93Ti_59kX3kPvxVtY5zbJJ64k_2Sau7avOe2s4iYkBtBPn_h5A6fhyqaoBbwuyVTCAtEkXP3oPeqX55pqB3ON8chgA"}
    user_headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik4wTTBOamhHUVRoRVJVUTVOVUpGUWtFMk5USkNOVEJCTURRelJFUkNNVGRGT0VWRE1rSTJOQSJ9.eyJpc3MiOiJodHRwczovL2lkYW5tZWwuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE3NTQ1MTIzMTkzMzc3NDQzOTQxIiwiYXVkIjpbImh0dHBzOi8vaGFoaW11ci5jb20iLCJodHRwczovL2lkYW5tZWwuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4MTc2NjQzMCwiZXhwIjoxNTgxODUyODMwLCJhenAiOiJMMlIzalVGaVRaRkptYXZ3VGNWUktxaDdMOUVPU0xETiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6dGVhbXMiLCJnZXQ6dG91cm5hbWVudHMiXX0.q7Tn261EH9ES3JXCNU5SmD_xVEJmGAXPO3nXDMgs4mdcBcuGt4GBiVGgItb9Y4llPRqYnljfUmWHhUlzgDNBol_yxW69j8nrTek4ynibTFxGg266vNLaz6dJIXO-BkJcKXo3vJvQxcT0cJXreRSvYdMqWJZSetE5Hg1irG5S0BQdd_yUeqMaoQYQHc0dk-iL_gvLKoyd4G4B2VWrUs_8moawW8FmtvDSAJDXCO-1pSVjimv4kfzeYgfCZ0gXSi78fjYnVtu-25RjTnpuwC-r_xQJqZ0D-f2m9nI7YdJDqxXsd3yGAqo2fiOZokRxYEyHHUuhxrz8-2itx7_C_zjq-g"}

    def create_app(self):
        """Define test variables and initialize app."""
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        app.config["TESTING"] = True
        os.environ["NO_AUTH"] = "1"
        del os.environ["NO_AUTH"]
        return app

    def test_admin_can_get_tournaments(self):
        t = Tournament(name="New Tournament")
        t.insert()
        response = app.test_client().get(
            f'/tournaments',
            headers=self.admin_headers
        )
        self.assert200(response)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "New Tournament")

    def test_admin_can_insert_team(self):
        """Inserting successfully should return 200 and the correct location
        header"""
        team = {
            "name": "England",
            "flag": "http://usrl_to_flag.png"
        }
        response = app.test_client().post(
            '/teams',
            data=json.dumps(team),
            content_type='application/json',
            headers=self.admin_headers
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response.headers)
        self.assertEqual(
            response.headers["Location"], f"http://localhost/teams/1"
        )

    def test_user_can_get_tournaments(self):
        t = Tournament(name="New Tournament")
        t.insert()
        response = app.test_client().get(
            f'/tournaments',
            headers=self.user_headers
        )
        self.assert200(response)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "New Tournament")

    def test_user_fails_to_insert_team(self):
        """Inserting successfully should return 200 and the correct location
        header"""
        team = {
            "name": "England",
            "flag": "http://usrl_to_flag.png"
        }
        response = app.test_client().post(
            '/teams',
            data=json.dumps(team),
            content_type='application/json',
            headers=self.user_headers
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn('Location', response.headers)


if __name__ == "__main__":
    unittest.main()
