from ..model import Role
from ..util import Config, global_ids
from ..file.common import require_one,attrs,common_search

def read (entity):
    return require_one('Role', search(entity), entity.obj_name)

def search (entity):
    return list(map(lambda e:__unload(e), common_search('role', entity)))

def __unload(entry):
    entity = Role()
    for attr in attrs["search"]["role"] + attrs["search_multi"]["role"] + attrs["extra"]["role"]:
        setattr(entity, attr, entry.get(attr))
    return entity
