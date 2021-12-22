'''
@copyright: 2022 - Symas Corporation
'''

import json
import os
from ..util.global_ids import PYFORTRESS_CONF
from ..util.fortress_error import RbacError
from ..util import global_ids

class Config:
    current = {
        "data": {},
        "filename": None
    }
    
    def load(filename='py-fortress-cfg.json'):
        found = False
        for loc in os.curdir, os.path.expanduser("~"), "/etc/pyfortress", os.getenv(PYFORTRESS_CONF):
            file = os.path.join(loc, filename)
            print("try config file: " + file)
            if os.path.isfile(file):
                with open(os.path.join(loc, filename)) as json_file:
                    Config.current["data"] = json.load(json_file)
                    Config.current["filename"] = filename
                    found = True
                    break

        if not found:
            msg = "Could not locate py-fortress-cfg.json. Was it added to current directory or user home directory or /etc/pyfortress or env var: " + PYFORTRESS_CONF
            print(msg)
            raise RbacError(msg="Configuration error=" + msg, id=global_ids.CONFIG_BOOTSTRAP_FAILED)

    def get(key):
        return Config.current["data"][key]

    def getDefault(key, default=None):
        return Config.current["data"].get(key, default)

# bootstrap the config:
Config.load()