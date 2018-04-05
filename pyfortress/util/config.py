'''
Created on Feb 11, 2018

@author: smckinney
@copyright: 2018 - Symas Corporation
'''

import json

class Config:
    current = {
        "data": {},
        "filename": None
    }
    
    def load(filename='py-fortress-cfg.json'):                
        with open(filename) as json_file:
            Config.current["data"] = json.load(json_file)
            Config.current["filename"] = filename

    def get(key):
        return Config.current["data"][key]

    def getDefault(key, default=None):
        return Config.current["data"].get(key, default)

# bootstrap the config:
Config.load()