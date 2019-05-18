#!/usr/bin/env python3

import os
import sys
import json
from logzero import logger


def execute(query):
    cmd = str(query["command"])
    logger.debug(cmd)
    try:
        frr_output = os.system(cmd)
        return frr_output, 200
    except:
        raise
