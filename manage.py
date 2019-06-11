#!/usr/bin/env python3
import click
import random
import string
from logzero import logger
from passlib.hash import pbkdf2_sha256


@click.group()
def main():
    pass


@main.command("dev-server", help="Start Flask development server")
@click.option("-h", "--host", type=str, default="0.0.0.0", help="Listening IP")
@click.option("-p", "--port", type=int, default=5000, help="TCP Port")
def dev_server(host, port):
    try:
        from hyperglass_frr import hyperglass_frr
        from hyperglass_frr import configuration

        debug_state = configuration.debug_state()
        hyperglass_frr.app.run(host="0.0.0.0", debug=True, port=8080)
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
