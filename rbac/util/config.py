'''
@copyright: 2022 - Symas Corporation
'''

import json
import os
from . fortress_error import RbacError
from . import global_ids

# config file ENV VAR:
PYFORTRESS_CONF = "PYFORTRESS_CONF"
DATA = 'data'
FILENAME = 'filename'

class Config:
    current = {
        DATA: {},
        FILENAME: None
    }
    
    def load(filename='py-fortress-cfg.json'):
        found = False
        for loc in os.curdir, os.path.expanduser("~"), "/etc/pyfortress", os.getenv(PYFORTRESS_CONF):
            file = os.path.join(loc, filename)
            if os.path.isfile(file):
                print("opening config file: " + file)
                with open(os.path.join(loc, filename)) as json_file:
                    Config.current[DATA] = json.load(json_file)
                    Config.current[FILENAME] = filename
                    found = True
                    break

        if not found:
            msg = "Could not locate py-fortress-cfg.json. Was it added to current directory or user home directory or /etc/pyfortress or env var: " + PYFORTRESS_CONF
            print(msg)
            raise RbacError(msg="Configuration error=" + msg, id=global_ids.CONFIG_BOOTSTRAP_FAILED)

    def get(key):
        return Config.current[DATA][key]

    def getDefault(key, default=None):
        return Config.current[DATA].get(key, default)

# bootstrap the config:
Config.load()