import os
from app import app
from flask import jsonify, json, request, abort
from app.models import Tournament, Team
from app.auth import requires_auth, AuthError


@app.route("/tournaments", methods=["GET"])
@requires_auth('get:tournaments')
def get_tournaments(permission):
    tournaments = [t.to_dict() for t in Tournament.query.all()]
    return jsonify(tournaments)


@app.route("/tournaments", methods=["POST"])
@requires_auth('post:tournaments')
def create_tournament(permission):
    try:
        name = request.json["name"]
    except KeyError:
        abort(400)
    t = Tournament(name=name)
    t.insert()
    response = jsonify()
    response.status_code = 201
    response.headers["location"] = f"/tournaments/{t.uid}"
    return response


@app.route("/tournaments/<int:uid>", methods=["GET"])
@requires_auth('get:tournaments')
def get_tournament(permission, uid):
    t = Tournament.query.get_or_404(uid)
    return jsonify(t.to_dict())


@app.route("/tournaments/<int:uid>", methods=["DELETE"])
@requires_auth('delete:tournaments')
def delete_tournament(permission, uid):
    t = Tournament.query.filter_by(uid=uid).first()
    try:
        t.delete()
    except:
        abort(422)

    return jsonify({}), 204


@app.route("/teams", methods=["POST"])
@requires_auth('post:teams')
def insert_team(permission):
    try:
        name = request.json["name"]
        flag = request.json["flag"]
    except KeyError:
        abort(400)

    team = Team(name=name, flag=flag)
    team.insert()
    response = jsonify()
    response.status_code = 201
    response.headers["location"] = f"/teams/{team.uid}"
    return response


@app.route("/teams/<int:uid>", methods=["GET"])
@requires_auth('get:teams')
def get_team(permission, uid):
    team = Team.query.get_or_404(uid)
    return jsonify(team.to_dict())


@app.route("/teams/<int:uid>", methods=["PATCH"])
@requires_auth('patch:teams')
def update_team(permission, uid):
    team = Team.query.get_or_404(uid)
    name = request.json.get("name")
    flag = request.json.get("flag")

    team.update(name=name, flag=flag)

    return jsonify({}), 204


def error_handler(status_code, message):
    return jsonify({
        "error": status_code,
        "message": message,
    }), status_code


@app.errorhandler(400)
def bad_request(error, message="Bad Request"):
    return error_handler(400, message)


@app.errorhandler(401)
def unauthorized(error, message="Unauthorized"):
    return error_handler(401, message)


@app.errorhandler(405)
def method_not_allowed(error):
    return error_handler(405, "method now allowed")


@app.errorhandler(404)
def not_found(error):
    return error_handler(404, "resource not found")


@app.errorhandler(422)
def unprocessable_entity(error):
    return error_handler(422, "unprocessable entity")


@app.errorhandler(500)
def server_error(error):
    return error_handler(500, "internal server error")


@app.errorhandler(AuthError)
def auth_error(ae):
    return error_handler(status_code=ae.status_code,
                         message=ae.error.get("description", ""))
