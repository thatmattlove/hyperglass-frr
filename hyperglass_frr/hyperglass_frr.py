"""API Controller"""
# Module Imports
import json
from waitress import serve
from logzero import logger
from passlib.hash import pbkdf2_sha256
from flask import Flask, request, Response, jsonify

# Project Imports
from hyperglass_frr import execute
from hyperglass_frr import configuration

app = Flask(__name__)

api = configuration.api()


@app.route("/frr", methods=["POST"])
def frr():
    """
    Main Flask route ingests JSON parameters and API key hash from hyperglass and passes it to
    execute module for execution
    """
    headers = request.headers
    api_key_hash = headers.get("X-Api-Key")
    # Verify API key hash against plain text value in configuration.py
    if pbkdf2_sha256.verify(api["key"], api_key_hash) is True:
        query_json = request.get_json()
        query = json.loads(query_json)
        frr_response = execute.execute(query)
        return Response(frr_response[0], frr_response[1])
    msg = "Validation of API key failed. Hash: %s" % api_key_hash
    logger.error(msg)
    return jsonify({"message": "Error: Unauthorized"}), 401


# Simple Waitress WSGI implementation
if __name__ == "__main__":
    serve(app, host=api["listen_addr"], port=api["port"])
