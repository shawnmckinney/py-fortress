from util.fortress_error import FortressError
from util.global_ids import USER_PW_INVLD,USER_PW_CHK_FAILED
class NotFound(FortressError):
    pass

class NotUnique(FortressError):
    pass

class AuthFail(FortressError):
    def __init__(self,msg="Authentication fail",id=USER_PW_INVLD, **kw):
        super().__init__(msg=msg,id=id,**kw)

class AuthError(FortressError):
    def __init__(self,msg="Authentication error",id=USER_PW_CHK_FAILED, **kw):
        super().__init__(msg=msg,id=id,**kw)

