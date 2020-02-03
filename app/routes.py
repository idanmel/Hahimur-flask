import os
from app import app
from flask import jsonify, json, request
from app.models import Tournament


@app.route("/tournaments", methods=["GET"])
def get_tournaments():
    tournaments = [t.to_dict() for t in Tournament.query.all()]
    return jsonify(tournaments)


@app.route("/tournaments", methods=["POST"])
def create_tournament():
    name = request.json["name"]
    t = Tournament(name=name)
    t.insert()
    return jsonify({
        "nice": "well done"
    })
