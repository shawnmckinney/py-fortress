'''
Created on Mar 2, 2018

@author: smckinn
'''
class FortressError(Exception):
 def __init__(self, id=None, msg=None, prev=None):
      self.id = id
      self.msg = msg
      self.prev = prev