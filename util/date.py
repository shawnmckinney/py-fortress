'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger

class Date(Validator):
        
    def validate(self, constraint, now):      
        #logger.debug('name=' + constraint.name + ',len=' + str(len(constraint.begin_date)))
          
        if not constraint.begin_date or constraint.begin_date is None or not constraint.end_date or constraint.end_date is None:
            return True        
        elif constraint.begin_date == 'none' or constraint.end_date == 'none':
            return True        
        elif constraint.begin_date <= now.date <= constraint.end_date:
            return True
        else:            
            return False        
        