'''
@copyright: 2022 - Symas Corporation
'''
from ..util import RbacError
from ..util.global_ids import USER_PW_INVLD,USER_PW_CHK_FAILED


class NotFound(RbacError):
    pass

class NotUnique(RbacError):
    pass

class AuthFail(RbacError):
    def __init__(self,msg="Authentication fail",id=USER_PW_INVLD, **kw):
        super().__init__(msg=msg,id=id,**kw)

class AuthError(RbacError):
    def __init__(self,msg="Authentication error",id=USER_PW_CHK_FAILED, **kw):
        super().__init__(msg=msg,id=id,**kw)

