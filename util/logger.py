'''
Created on Feb 23, 2018

@author: smckinn
'''

import datetime
from util.config import Config
import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

LOGGER = 'logger'

def setup():
    """Function setup as many loggers as you want"""
    now = datetime.datetime.now()
    name = Config.get(LOGGER)['file_name']
    handler = logging.FileHandler(
        name + '-' 
        + now.strftime("%Y-%m-%d") 
        + '.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    mlog = logging.getLogger( name )
    mlog.setLevel( level_ )
    mlog.addHandler(handler)
    return [mlog, handler]

level_str_ = Config.get(LOGGER)['level']

if level_str_ == 'DEBUG' :
    level_ = DEBUG
elif level_str_ == 'INFO' :
    level_ = INFO
elif level_str_ == 'WARNING' :
    level_ = WARNING
elif level_str_ == 'ERROR' :
    level_ = ERROR
elif level_str_ == 'CRITICAL' :
    level_ = CRITICAL
 
is_log = False
if is_log is False:
    log, handler_ = setup()    
    is_log = True
    
my_handlers = [handler_]
logging.basicConfig(handlers=my_handlers, level=level_)