'''
Created on Feb 16, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util import Config

class Constraint:    
    "Fortress Constraint"
    
    def __init__(
            self,
            raw=None,
            name=None,
            timeout=None,
            begin_time=None,
            end_time=None,
            begin_date=None,
            end_date=None,
            begin_lock_date=None,
            end_lock_date=None,
            day_mask=None 
            ):
    
        self.raw = raw
        if self.raw is not None:
            entity_constraint = self.raw.split(Config.get('schema')['raw_delimiter'])
            entity_constraint = [ val.strip() for val in entity_constraint ]
            if entity_constraint[0] is not None:
                self.name=entity_constraint[0]
            if entity_constraint[1] is not None:
                self.timeout=entity_constraint[1]        
            if entity_constraint[2] is not None:
                self.begin_time=entity_constraint[2]
            if entity_constraint[3] is not None:
                self.end_time=entity_constraint[3]
            if entity_constraint[4] is not None:
                self.begin_date=entity_constraint[4]
            if entity_constraint[5] is not None:
                self.end_date=entity_constraint[5]
            if entity_constraint[6] is not None:
                self.begin_lock_date=entity_constraint[6]
            if entity_constraint[7] is not None:
                self.end_lock_date=entity_constraint[7]
            if entity_constraint[8] is not None:
                self.day_mask=entity_constraint[8]            
        else:
            self.name = name
            self.timeout = timeout
            self.begin_time = begin_time
            self.end_time = end_time
            self.begin_date = begin_date
            self.end_date = end_date
            self.begin_lock_date = begin_lock_date
            self.end_lock_date = end_lock_date
            self.day_mask = day_mask