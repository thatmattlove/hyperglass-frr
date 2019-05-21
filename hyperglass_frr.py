#!/usr/bin/env python3

import json
from waitress import serve
from logzero import logger
from passlib.hash import pbkdf2_sha256
from flask import Flask, request, Response, jsonify, flash

import configuration
import execute

app = Flask(__name__)

api_listen_addr = getattr(configuration, "api_listen_addr", "*")
api_port = getattr(configuration, "api_port", 8080)
api_key_hash = getattr(configuration, "api_key_hash")


@app.route("/frr", methods=["POST"])
def frr():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if pbkdf2_sha256.verify(auth, api_key_hash) is True:
        query_string = request.get_json()
        query = json.loads(query_string)
        try:
            frr_response = execute.execute(query)
            frr_output = frr_response[0]
            frr_status = frr_response[1]
            return Response(frr_output, frr_status)
        except:
            raise
    else:
        return jsonify({"message": "Error: Unauthorized"}), 401


if __name__ == "__main__":
    serve(app, host=api_listen_addr, port=api_port)
