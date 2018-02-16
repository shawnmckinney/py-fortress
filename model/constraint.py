'''
Created on Feb 16, 2018

@author: smckinn
'''
# Copyright 2018 - Symas Corporation

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
    entityConstraint = self.raw.split(DELIMITER)
    entityConstraint = [ val.strip() for val in entityConstraint ]
    if entityConstraint[0] is not None:
        self.name=entityConstraint[0]
    if entityConstraint[1] is not None:
        self.timeout=entityConstraint[1]        
    if entityConstraint[2] is not None:
        self.beginTime=entityConstraint[2]
    if entityConstraint[3] is not None:
        self.endTime=entityConstraint[3]
    if entityConstraint[4] is not None:
        self.beginDate=entityConstraint[4]
    if entityConstraint[5] is not None:
        self.endDate=entityConstraint[5]
    if entityConstraint[6] is not None:
        self.beginLockDate=entityConstraint[6]
    if entityConstraint[7] is not None:
        self.endLockDate=entityConstraint[7]
    if entityConstraint[8] is not None:
        self.dayMask=entityConstraint[8]
                
DELIMITER = Config.get('schema')['raw_delimiter']        