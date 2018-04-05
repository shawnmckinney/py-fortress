from os import environ,replace
from json import load,dump
from collections import OrderedDict

filename = 'test/py-fortress-cfg.json'

with open(filename, 'r') as f:
    config = load(f, object_pairs_hook=OrderedDict)

config['ldap']['port'] = int(environ['CONTAINER_PORT'])

with open('{}.new'.format(filename), 'w') as f:
    dump(config, f, indent=2)

replace('{}.new'.format(filename), filename)
