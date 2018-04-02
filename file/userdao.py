import uuid
from model import User
from util import Config, global_ids
from file.common import require_one,attrs,common_search

def read (entity):
    return require_one('User', search(entity), entity.uid)

def authenticate (entity):
    raise FortressError(msg="file backend does not support authentication")

def search (entity):
    return map(lambda e:__unload(e), common_search('user', entity))

def __unload(entry):
    entity = User()
    entry["dn"] = __dn_from_entry(entry)
    for attr in attrs["search"]["user"] + attrs["search_multi"]["user"] + attrs["extra"]["user"]:
        setattr(entity, attr, entry.get(attr))
    return entity

def __dn_from_entry(entry):
    return "uid={},ou=People,{}".format(entry['uid'], Config.get("dit")["suffix"])

