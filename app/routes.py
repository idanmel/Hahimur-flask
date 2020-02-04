import os
from app import app
from flask import jsonify, json, request, abort
from app.models import Tournament


@app.route("/tournaments", methods=["GET"])
def get_tournaments():
    tournaments = [t.to_dict() for t in Tournament.query.all()]
    return jsonify(tournaments)


@app.route("/tournaments", methods=["POST"])
def create_tournament():
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
def get_tournament(uid):
    t = Tournament.query.get_or_404(uid)
    return jsonify(t.to_dict())


@app.route("/tournaments/<int:uid>", methods=["DELETE"])
def delete_tournament(uid):
    t = Tournament.query.filter_by(uid=uid).first()
    try:
        t.delete()
    except:
        abort(422)

    return jsonify({}), 204


def error_handler(status_code, message):
    return jsonify({
        "error": status_code,
        "message": message,
    }), status_code


@app.errorhandler(400)
def bad_request(error):
    return error_handler(400, "Bad Request")


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
