#!/usr/bin/env python3

import json
from logzero import logger
from flask import Flask, request, Response, jsonify, flash

import execute

app = Flask(__name__)


@app.route("/frr", methods=["POST"])
def frr():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == "test1234":
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
