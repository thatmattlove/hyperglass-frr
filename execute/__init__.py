#!/usr/bin/env python3

# import os
# import sys
# import json
import subprocess
from logzero import logger


# def execute(query):
#     cmd = str(query["command"])
#     logger.debug(cmd)
#     try:
#         frr_output = os.system(cmd)
#         return frr_output, 200
#     except:
#         raise


def frr(target):
    logger.debug(target)
    command = subprocess.check_output(["vtysh", "-c", target])
    logger.debug(command)
    return command


def connectivity(target):
    logger.debug(target)
    target_args = target.split(" ")
    command = subprocess.check_output(target_args)
    logger.debug(command)
    return command


def execute(query):
    """
    Format:
    {'cmd': 'bgp_route', 'target': '1.1.1.0/24'}
    """
    cmd = query["cmd"]
    target = query["target"]
    if cmd in ["bgp_route", "bgp_aspath", "bgp_community"]:
        try:
            return frr(target), 200
        except:
            raise
            return f"Error running FRRouting command: {target}", 501
    elif cmd in ["ping", "traceroute"]:
        try:
            return connectivity(target), 200
        except:
            return f"Error running command: {target}", 501
