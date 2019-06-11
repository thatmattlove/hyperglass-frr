"""
Exports constructed commands and API variables from configuration file based \
on input query
"""
# Standard Imports
import os
import logging

# Module Imports
import toml
import logzero
from logzero import logger

# Project Directories
this_directory = os.path.dirname(os.path.abspath(__file__))

# TOML Imports
conf = toml.load(os.path.join(this_directory, "configuration.toml"))


def debug_state():
    """Returns string for logzero log level"""
    state = conf.get("debug", False)
    return state


# Logzero Configuration
if debug_state():
    logzero.loglevel(logging.DEBUG)
else:
    logzero.loglevel(logging.INFO)


def api():
    """Imports & exports configured API parameters from configuration file"""
    api_dict = {
        "listen_addr": conf["api"].get("listen_addr", "*"),
        "port": conf["api"].get("port", 8080),
        "key": conf["api"].get("key", 0),
    }
    return api_dict


class Command:
    """Imports & exports configured command syntax from configuration file"""

    def __init__(self, query):
        self.query_type = query.get("query_type")
        self.afi = query.get("afi")
        self.source = query.get("source")
        self.target = query.get("target", 0)
        raw_command = conf["commands"][self.afi].get(self.query_type)
        self.command = raw_command.format(source=self.source, target=self.target)
        logger.debug(
            f"Command class initialized with paramaters:\nQuery Type: {self.query_type}\nAFI: \
            {self.afi}\nSource: {self.source}\nTarget: {self.target}\nConstructed command: \
            {self.command}"
        )

    def is_string(self):
        """Returns command as single string"""
        command_string = self.command
        logger.debug(f"Constructed command as string: {command_string}")
        return command_string

    def is_split(self):
        """Returns bash command as a list of arguments"""
        command_split = self.command.split(" ")
        logger.debug(f"Constructed bash command as list: {command_split}")
        return command_split

    def vtysh(self):
        """Returns bash command as a list of arguments, with the vtysh command itself as a \
        separate list element"""
        vtysh_pre = "vtysh -u -c".split(" ")
        logger.debug(f"vtysh command & argument list: {vtysh_pre}")
        vtysh_pre.append(self.command)
        logger.debug(f"vtysh command & argument list with command: {vtysh_pre}")
        return vtysh_pre
