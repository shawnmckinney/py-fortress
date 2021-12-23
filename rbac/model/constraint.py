'''
@copyright: 2022 - Symas Corporation
'''

from rbac.util import Config

DELIMITER = Config.get('schema')['raw_delimiter']

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
        # If ldap entity doesn't have constraint, this happens:
        if self.raw is not None and not self.raw:
            pass
        # If ldap entity has constraint:        
        elif self.raw is not None:
            entity_constraint = self.raw.split(DELIMITER)
            entity_constraint = [ val.strip() for val in entity_constraint ]
            if entity_constraint[0] is not None:
                self.name=entity_constraint[0]
            if entity_constraint[1] is not None:
                self.timeout=int(entity_constraint[1])        
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
        # if going the other way, from caller to ldap, this will occur:                            
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
            
    def get_raw(self):
        # Raw format: name$timeout$begin_time$end_time$begin_date$end_date$begin_lock_date$end_lock_date$day_mask
        # Example:
        # oamT12SSD1$30$0000$0000$20090101$21000101$20500101$20500115$1234567
        raw = self.name + DELIMITER
        if self.timeout is not None:
            raw += str(self.timeout)
        else:
            raw += '0'
        raw += DELIMITER
        if self.begin_time is not None:
            raw += self.begin_time
        raw += DELIMITER
        if self.end_time is not None:
            raw += self.end_time
        raw += DELIMITER
        if self.begin_date is not None:
            raw += self.begin_date
        raw += DELIMITER
        if self.end_date is not None:
            raw += self.end_date
        raw += DELIMITER
        if self.begin_lock_date is not None:
            raw += self.begin_lock_date
        raw += DELIMITER
        if self.end_lock_date is not None:
            raw += self.end_lock_date
        raw += DELIMITER
        if self.day_mask is not None:
            raw += self.day_mask     
        return raw       
