'''
@copyright: 2022 - Symas Corporation
'''

import json
import sys
import os

class Config:
    current = {
        "data": {},
        "filename": None
    }
    
    def load(filename='py-fortress-cfg.json'):
        file_path = os.path.join(sys.path[1], filename )
        with open(file_path) as json_file:
            Config.current["data"] = json.load(json_file)
            Config.current["filename"] = filename

    def get(key):
        return Config.current["data"][key]

    def getDefault(key, default=None):
        return Config.current["data"].get(key, default)

# bootstrap the config:
Config.load()