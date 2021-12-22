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
        for loc in os.curdir, os.path.expanduser("~"), "/etc/py-fortress", os.environ.get(PYFORTRESS_CONF):
            try:
                with open(os.path.join(loc, filename)) as json_file:
                    Config.current["data"] = json.load(json_file)
                    Config.current["filename"] = filename
                    found = True
            except IOError as e:
                # Keep looking
                pass
            if not found:
                msg = "Could not locate py-fortress-cfg.json. Was it added to user home directory or /etc/py-fortress or env var:" + PYFORTRESS_CONF
                print(msg)
                raise RbacError(msg="Configuration error=" + msg, id=global_ids.CONFIG_BOOTSTRAP_FAILED)

    def get(key):
        return Config.current["data"][key]

    def getDefault(key, default=None):
        return Config.current["data"].get(key, default)

# bootstrap the config:
Config.load()