import uuid
from model import Perm
from util import Config, global_ids
from file.common import require_one,attrs,common_search

def read (entity):
    return require_one('Perm', search(entity), entity.obj_name)

def search (entity):
    return list(map(lambda e:__unload(e), common_search('perm', entity)))

def __unload(entry):
    entity = Perm()
    entry["dn"] = __dn_from_entry(entry)
    for attr in attrs["search"]["perm"] + attrs["search_multi"]["perm"] + attrs["extra"]["perm"]:
        setattr(entity, attr, entry.get(attr))
    return entity

def __dn_from_entry(entry):
    return "{}ftOpNm={},ou=Perm,{}".format(
        "ftObjId={}+".format(entry['obj_id']) if entry['obj_id'] is not None else "",
        entry['op_name'],
        Config.get("dit")["suffix"])

