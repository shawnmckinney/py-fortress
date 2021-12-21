'''
@copyright: 2022 - Symas Corporation
'''
class RbacError(Exception):
 def __init__(self, id=None, msg=None, prev=None):
      self.id = id
      self.msg = msg
      self.prev = prev