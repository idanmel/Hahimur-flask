import os
from app import app
from flask import jsonify, json, request
from app.models import Tournament


@app.route("/tournaments", methods=["GET"])
def get_tournaments():
    tournaments = [t.to_dict() for t in Tournament.query.all()]
    return jsonify(tournaments)


@app.route("/tournaments/<int:uid>", methods=["GET"])
def get_tournament(uid):
    t = Tournament.query.get_or_404(uid)
    return jsonify({
        "id": t.uid,
        "name": t.name
    })


@app.route("/tournaments", methods=["POST"])
def create_tournament():
    name = request.json["name"]
    t = Tournament(name=name)
    t.insert()
    response = jsonify()
    response.status_code = 201
    response.headers["location"] = f"/tournaments/{t.uid}"
    return response


def error_handler(status_code=404, message=""):
    return jsonify({
        "error": status_code,
        "message": message,
    }), status_code


@app.errorhandler(404)
def not_found(error):
    return error_handler(404, "resource not found")


@app.errorhandler(500)
def server_error(error):
    return error_handler(500, "internal server error")
