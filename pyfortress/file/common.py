from json import load,dump
import re

from ..util import Config
from ..util.fortress_error import FortressError
from ..file.fileex import NotFound,NotUnique

def require_one(label='thing', entity_list=[], query=''):
    el = list(entity_list)
    if len(el) == 0:
        raise NotFound(msg="{} Read not found, query={}".format(label, query),
                       id=None)
    elif len(el) > 1:
        raise NotUnique(msg="{} Read not unique, query={}".format(label, query),
                        id=None)
    else:
        return el[0]

attrs = {
    "extra": {
        "user": ["password"],
        "perm": ["abstract_name","internal_id","type"],
        "role": ["internal_id"]
    },
    "search": {
        "user": ["uid","cn","sn","description"],
        "perm": ["obj_name","op_name","obj_id","description"],
        "role": ["name","description"]
    },
    "search_multi": {
        "user": ["roles"],
        "perm": ["roles"],
        "role": ["members"]
    }
}

def __make_wild_re (wild):
    return "^{}$".format(re.escape(wild).replace(r'\*','.*').replace(r'\?','.'))

def common_search (etype, entity):
    matches = list()
    for e in __read_all(etype):
        matched = False
        for attr in attrs["search"][etype]:
            av = getattr(entity, attr, None)
            uv = e.get(attr, '')
            if av and uv and re.fullmatch(__make_wild_re(av), uv):
                matched = True
        for attr in attrs["search_multi"][etype]:
            avs = getattr(entity, attr, [])
            if avs is None:
                avs = []
            uvs = e.get(attr, [])
            for av in avs:
                av_re = re.compile(__make_wild_re(av))
                if not any(map(lambda uv: av_re.fullmatch(uv) is not None, uvs)):
                    matched = False
                    break
        if matched:
            matches.append(e)
    return matches

def __read_all(etype):
    try:
        with open(Config.get('file')[etype], 'r') as f:
            return load(f)
    except FileNotFoundError as e:
        return []
