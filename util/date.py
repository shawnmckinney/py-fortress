'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger
from util.global_ids import ACTV_FAILED_DATE, SUCCESS

class Date(Validator):
        
    def validate(self, constraint, now):      
        #logger.debug('name=' + constraint.name + ',len=' + str(len(constraint.begin_date)))
          
        if not constraint.begin_date or constraint.begin_date is None or not constraint.end_date or constraint.end_date is None:
            return SUCCESS        
        elif constraint.begin_date == 'none' or constraint.end_date == 'none':
            return SUCCESS        
        elif constraint.begin_date <= now.date <= constraint.end_date:
            return SUCCESS
        else:            
            return ACTV_FAILED_DATE        
        