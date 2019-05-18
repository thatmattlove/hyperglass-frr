#!/usr/bin/env python3

import os
import sys
import json
from logzero import logger

def execute(query):
    logger.debug(query)
    cmd = str(query["command"])
    logger.debug(cmd)
    try:
        frr_output = os.system(cmd)
        return frr_output, 200
    except:
        raise


# if __name__ == '__main__':
#    execute('vtysh -c "show bgp ipv4 unicast 1.1.1.0/24"')
