#!/usr/bin/env python3

import subprocess
from logzero import logger


def frr_bgp_route(afi, target):
    command = f"show bgp {afi} unicast {target}"
    frr_output = subprocess.check_output(["vtysh", "-c", command])
    return frr_output


def frr_bgp_dualstack(query):
    cmd = query["cmd"]
    target = query["target"]
    if cmd == "bgp_community":
        command4 = f"show bgp ipv4 unicast community {target}"
        command6 = f"show bgp ipv6 unicast community {target}"
        frr_output = subprocess.check_output(["vtysh", "-c", command4, "-c", command6])
        return frr_output
    elif cmd == "bgp_aspath":
        command4 = f"show bgp ipv4 unicast regexp {target}"
        command6 = f"show bgp ipv6 unicast regexp {target}"
        frr_output = subprocess.check_output(["vtysh", "-c", command4, "-c", command6])
        return frr_output


def linux_ping(query):
    afi = query["afi"]
    source = query["source"]
    target = query["target"]
    if afi == "ipv4":
        output = subprocess.check_output(
            ["ping", "-4", "-c", "5", "-I", source, target]
        )
        return output
    elif afi == "ipv6":
        output = subprocess.check_output(
            ["ping", "-6", "-c", "5", "-I", source, target]
        )
        return output


def linux_traceroute(query):
    afi = query["afi"]
    source = query["source"]
    target = query["target"]
    if afi == "ipv4":
        output = subprocess.check_output(
            ["traceroute", "-4", "-n", "-w", "1", "-q", "2", "-A", "-s", source, target]
        )
        return output
    elif afi == "ipv6":
        output = subprocess.check_output(
            ["traceroute", "-6", "-n", "-w", "1", "-q", "2", "-A", "-s", source, target]
        )
        return output


def execute(query):
    query_type = type(query)
    cmd = query["cmd"]
    if cmd in ["bgp_route"]:
        try:
            return frr_bgp_route(query["afi"], query["target"]), 200
        except:
            raise
            return f"Error running FRRouting command: {query}", 501
    elif cmd in ["bgp_community", "bgp_aspath"]:
        try:
            return frr_bgp_dualstack(query), 200
        except:
            raise
            return f"Error running FRRouting command: {query}", 501
    elif cmd in ["ping"]:
        try:
            return linux_ping(query), 200
        except:
            return f"Error: {query}", 501
    elif cmd in ["traceroute"]:
        try:
            return linux_traceroute(query), 200
        except:
            return f"Error: {query}", 501
