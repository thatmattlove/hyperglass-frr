#!/usr/bin/env python3

import os
import sys
import click
import random
import string
from logzero import logger
from passlib.hash import pbkdf2_sha256

import hyperglass_frr


@click.group()
def main():
    pass


@main.command()
def testserver():
    try:
        hyperglass_frr.app.run(host="0.0.0.0", debug=True, port=80)
        logger.error("Started test server.")
    except:
        logger.error("Failed to start test server.")
        raise


@main.command()
def generatekey(string_length=16):
    ld = string.ascii_letters + string.digits
    api_key = "".join(random.choice(ld) for i in range(string_length))
    key_hash = pbkdf2_sha256.hash(api_key)
    click.echo(f"Your API Key is: {api_key}\nYour Key Hash is: {key_hash}")


if __name__ == "__main__":
    main()
