'''
@copyright: 2022 - Symas Corporation
'''

class Session:    
    "Fortress Session"
    def __init__(
            self,
            user=None,
            is_authenticated=False,
            session_id=None,
            last_access=None,
            timeout=None,
            error_id=None,
            expiration_seconds=None,
            grace_logins=None,
            message=None,
            warnings=None
            ):
        self.user=user
        self.is_authenticated=is_authenticated
        self.session_id=session_id
        self.last_access=last_access
        self.timeout=timeout
        self.error_id=error_id
        self.expiration_seconds=expiration_seconds
        self.grace_logins=grace_logins
        self.message=message
        self.warnings=warnings