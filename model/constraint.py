'''
Created on Feb 16, 2018

@author: smckinn
'''
# Copyright 2018 - Symas Corporation

from util import Config

class Constraint:    
    "Fortess Constraint"
    
    def __init__(
            self,
            raw  
            ):
    
        self.raw = raw
        if self.raw is not None:
            entityConstraint = self.raw.split(Config.get('schema')['raw_delimiter'])
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