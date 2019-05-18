#!/usr/bin/env python3

import os
import sys
import click
from logzero import logger
import hyperglass_frr

@click.group()
def main():
    pass


@main.command()
def testserver():
    try:
        hyperglass_frr.app.run(host="0.0.0.0", debug=True, port=5000)
        logger.error("Started test server.")
    except:
        logger.error("Failed to start test server.")
        raise

if __name__ == "__main__":
    main()

