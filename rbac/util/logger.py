'''
@copyright: 2022 - Symas Corporation
'''

import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import datetime
from ..util import Config

LOGGER = 'logger'
ctr = 1

def setup(ctr):
    """Function setup as many loggers as you want"""    
    now = datetime.datetime.now()
    name = Config.get(LOGGER)['file_name']
    handler = logging.FileHandler(
    #handler = logging.StreamHandler(        
        name + '-' 
        + now.strftime("%Y-%m-%d") 
        + '.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    mlog = logging.getLogger( name )
    mlog.setLevel( level_ )
    
    if Config.get(LOGGER)['console_out']:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        mlog.addHandler(consoleHandler)    

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
    logger, handler_ = setup(ctr)    
    is_log = True

    
my_handlers = [handler_]
logging.basicConfig(handlers=my_handlers, level=level_)