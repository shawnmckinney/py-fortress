'''
@copyright: 2022 - Symas Corporation
'''
from ..model import Perm
from ..file.common import require_one,attrs,common_search

def read (entity):
    return require_one('Perm', search(entity), entity.obj_name)

def search (entity):
    return list(map(lambda e:__unload(e), common_search('perm', entity)))

def __unload(entry):
    entity = Perm()
    for attr in attrs["search"]["perm"] + attrs["search_multi"]["perm"] + attrs["extra"]["perm"]:
        setattr(entity, attr, entry.get(attr))
    return entity

def search_on_roles (roles):
    return search (Perm(roles=roles))
