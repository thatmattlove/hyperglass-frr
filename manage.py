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


@main.command("generate-key", help="Generate API key & hash")
@click.option(
    "-l", "--length", "string_length", type=int, default=16, show_default=True
)
def generatekey(string_length):
    """Generates 16 character API Key for hyperglass-frr API, and a corresponding PBKDF2 SHA256 Hash"""
    ld = string.ascii_letters + string.digits
    api_key = "".join(random.choice(ld) for i in range(string_length))
    key_hash = pbkdf2_sha256.hash(api_key)
    click.secho(
        f"""
Your API Key is: {api_key}
Place your API Key in the `configuration.toml` of your API module. For example, in: `hyperglass-frr/hyperglass_frr/configuration.toml`

Your Key Hash is: {key_hash}
Use this hash as the password for the device using the API module. For example, in: `hyperglass/hyperglass/configuration/devices.toml`
"""
    )


if __name__ == "__main__":
    main()
