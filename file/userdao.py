import uuid
from model import User, Constraint
from util import Config, global_ids
from util.fortress_error import FortressError
from os import listdir
from json import load,dump

def read (entity):
    userList = search(entity)
    if userList is None or len(userList) == 0:
        raise NotFound(msg="User Read not found, uid=" + entity.uid, id=global_ids.USER_NOT_FOUND)
    elif len(userList) > 1:
        raise NotUnique(msg="User Read not unique, uid=" + entity.uid, id=global_ids.USER_READ_FAILED)
    else:
        return userList[0]


def authenticate (entity):
    __validate(entity, "User Bind")
    raise FortressError(msg="file backend does not support authentication")


attrs = {
    "extra": {
        "user": ["userPassword", "dn"]
    },
    "search": {
        "user": ["uid","cn","sn","description"]
    },
    "search_multi": {
        "user": ["roles"]
    }
}
#perm
#objname opname objid desc roles


def search (entity):
    __validate(entity, "User Search")
    matches = list()
    for u in __read_all():
        matched = False
        for attr in attrs["search"]["user"]:
            av = getattr(entity, attr, None)
            uv = u.get(attr, '')
            if av is not None and av == uv:
                matched = True
        for attr in attrs["search_multi"]["user"]:
            avs = getattr(entity, attr, [])
            if avs is None:
                avs = []
            uvs = u.get(attr, [])
            if not all(map(lambda av: av in uvs, avs)):
                matched = False
        if matched:
            matches.append(u)
    return map(lambda e:__unload(e), matches)


def __unload(entry):
    entity = User()
    entry["dn"] = __dn_from_uid(entry["uid"])
    for attr in attrs["search"]["user"] + attrs["search_multi"]["user"] + attrs["extra"]["user"]:
        setattr(entity, attr, entry.get(attr))
    return entity


def __validate(entity, op):
    if entity.uid is None or len(entity.uid) == 0 :
        __raise_exception(op, global_ids.UID, global_ids.USER_ID_NULL)


def __raise_exception(operation, field, id):
    raise FortressError(msg='userdao.' + operation + ' required field missing:' + field, id=id)


def __dn_from_uid(uid):
    return "uid={},ou=People,{}".format(uid, Config.get("dit")["suffix"])


def __read_all():
    try:
        with open(Config.get('file')['filename'], 'r') as f:
            return load(f)["users"]
    except FileNotFoundError as e:
        return []

