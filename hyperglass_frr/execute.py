"""
Execute the constructed command
"""
# Standard Imports
import logging
import subprocess

# Module Imports
import logzero
from logzero import logger

# Project Imports
from hyperglass_frr import configuration

# Logzero Configuration
if configuration.debug_state():
    logzero.loglevel(logging.DEBUG)
else:
    logzero.loglevel(logging.INFO)


def execute(query):
    """Gets constructed command string and runs the command via subprocess"""
    logger.debug(f"Received query: {query}")
    query_type = query.get("query_type")
    try:
        command = configuration.Command(query)
        if query_type in ["bgp_route", "bgp_community", "bgp_aspath"]:
            logger.debug(f'Running vtysh command "{command}"')
            output = subprocess.check_output(command.vtysh())
            status = 200
        if query_type in ["ping", "traceroute"]:
            logger.debug(f'Running bash command "{command}"')
            output = subprocess.check_output(command.is_split())
            status = 200
    except subprocess.CalledProcessError as error_exception:
        output = f'Unable to reach {query["target"]}.'
        status = 504
        logger.debug(f"{output} Error:\n{ping_error}")
    return (output, status)
