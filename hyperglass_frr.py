#!/usr/bin/env python3

import os
import sys
import json
from flask import Flask, request, Response, jsonify, flash

import execute

app = Flask(__name__)


@app.route("/frr", methods=["POST"])
def frr():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == "test1234":
        query_json = request.get_json()
        query = json.loads(query_json)
        try:
            frr_response = execute.execute(query)
            frr_output = frr_response[0]
            frr_status = frr_response[1]
            if frr_status == 200:
                return jsonify(frr_output), frr_status
            else:
                return jsonify({"message": "Error: Not Found"}), 404
        except:
            raise
    else:
        return jsonify({"message": "Error: Unauthorized"}), 401