#!/usr/bin/env python   
"""

The main AgentDan daemon process

"""
import sys
import json
import time
import AgentDan.config as config
from AgentDan import Conductor
from AgentDan import Delta
from AgentDan import Live
from AgentDan import ConfigFile
from AgentDan import Envivio

# Get logging level from Device.conf and 
# set logger and logging level
cf = ConfigFile('Device.conf')
logConfig = cf.getConfig('logging_level')
level = logConfig['level']      
config.log.setLevel(level)

# Define iteration timer for data collection
cycleConfig = cf.getConfig('cycle_time')
cycle = int(cycleConfig['seconds'])

def run():
    while True:
        
        try:
            ec = Conductor()
            status, results = ec.checkStatus()
            if status == 200:
                config.log.info('{0}: {1}'.format(__name__, results))
        except Exception as e:
            config.log.error('{0}: {1}'.format(__name__, e))
    
        try:
            el = Live()
            status, results = el.checkStatus()
            if status == 200:
                config.log.info('{0}: {1}'.format(__name__, results))
        except Exception as e:
            config.log.error('ERROR: {0}'.format(e))        

        try:
            eh = Envivio()
            status, results = eh.checkStatus()
            if status == 200:
                config.log.info('{0}: {1}'.format(__name__, results))
        except Exception as e:
            config.log.error('{0}: {1}'.format(__name__, e))

        #try:
            #ed = Delta()
            #status, results = ed.checkStatus()
            #if status == 200:
                #config.log.info('{0}: {1}'.format(__name__, results))
        #except Exception as e:
            #config.log.error('ERROR): {0}'.format(e))   
        
        time.sleep(cycle)
        
if __name__ == '__main__':
    run()
