'''
Created on Feb 16, 2018

@author: smckinn
'''

from util import Config

Config.load('py-fortress-cfg.json')

class Constraint:    
    "Fortess Constraint"
    def __init__(
            self,
            raw=None,  
            name=None,        
            timeout=None,  
            beginTime=None,
            endTime=None,
            beginDate=None,
            endDate=None,
            beginLockDate=None,
            endLockDate=None,
            dayMask=None
            ):
        self.raw = raw
        self.name = name
        self.timeout = timeout        
        self.beginTime = beginTime
        self.endTime = endTime
        self.beginDate = beginDate
        self.endDate = endDate
        self.beginLockDate = beginLockDate        
        self.endLockDate = endLockDate        
        self.dayMask = dayMask
    def load( self ):
        if self.raw is not None:
            parseIt( self )        
        
def parseIt ( self ):
    userConstraint = self.raw.split(DELIMITER)
    userConstraint = [ val.strip() for val in userConstraint ]
    if userConstraint[0] is not None:
        self.name=userConstraint[0]
    if userConstraint[1] is not None:
        self.timeout=userConstraint[1]        
    if userConstraint[2] is not None:
        self.beginTime=userConstraint[2]
    if userConstraint[3] is not None:
        self.endTime=userConstraint[3]
    if userConstraint[4] is not None:
        self.beginDate=userConstraint[4]
    if userConstraint[5] is not None:
        self.endDate=userConstraint[5]
    if userConstraint[6] is not None:
        self.beginLockDate=userConstraint[6]
    if userConstraint[7] is not None:
        self.endLockDate=userConstraint[7]
    if userConstraint[8] is not None:
        self.dayMask=userConstraint[8]
                
DELIMITER = Config.get('schema')['raw_delimiter']        