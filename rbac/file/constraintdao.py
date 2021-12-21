'''
@copyright: 2022 - Symas Corporation
'''

from ..model import Role
from ..file.common import require_one,attrs,common_search

def read (entity):
    return require_one('Constraint', search(entity), entity.obj_name)

def search (entity):
    return list(map(lambda e:__unload(e), common_search('constraint', entity)))

def __unload(entry):
    entity = Role()
    for attr in attrs["search"]["role"] + attrs["search_multi"]["role"] + attrs["extra"]["role"]:
        setattr(entity, attr, entry.get(attr))
    return entity
