"""
Exports constructed commands and API variables from configuration file based
on input query
"""
# Module Imports
import os
import toml

# Project Directories
this_directory = os.path.dirname(os.path.abspath(__file__))

# TOML Imports
conf = toml.load(os.path.join(this_directory, "configuration.toml"))


def api():
    """Imports & exports configured API parameters from configuration file"""
    a = conf["api"]
    listen_addr = a.get("listen_addr", "*")
    port = a.get("port", 8080)
    key = a.get("key", 0)
    return dict(listen_addr=listen_addr, port=port, key=key)


class command:
    """Imports & exports configured command syntax from configuration file"""

    def __init__(self, query):
        self.cmd = query.get("cmd")
        self.afi = query.get("afi")
        self.source = query.get("source")
        self.target = query.get("target", 0)
        c = conf["commands"][self.afi]
        fc = c.get(self.cmd)
        self.command = fc.format(source=self.source, target=self.target)

    def is_string(self):
        """Returns command as single string"""
        c = self.command
        return c

    def is_split(self):
        """Returns bash command as a list of arguments"""
        c = self.command
        cs = c.split(" ")
        return cs

    def vtysh(self):
        """
        Returns bash command as a list of arguments, with the vtysh command itself as a separate
        list element
        """
        c = self.command
        v = "vtysh -u -c".split(" ")
        v.append(c)
        return v
