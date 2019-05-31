"""
Execute the constructed command
"""
# Module Imports
import subprocess
from logzero import logger

# Project Imports
from hyperglass_frr import configuration


def execute(query):
    """Gets constructed command string and runs the command via subprocess"""
    cmd = query.get("cmd")
    try:
        c = configuration.command(query)
        if cmd in ["bgp_route", "bgp_community", "bgp_aspath"]:
            output = subprocess.check_output(c.vtysh())
            return (output, 200)
        if cmd in ["ping", "traceroute"]:
            output = subprocess.check_output(c.is_split())
            return (output, 200)
    except subprocess.CalledProcessError as e:
        msg = "Error running query for %s. Error: %s" % (query, e)
        logger.error(msg)
    return (msg, 501)
