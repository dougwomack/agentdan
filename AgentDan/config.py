#!/usr/bin/env python
"""
.. py:module:: config
    
A generic class library to create an instance of Conductor for monitoring and configuration
    
.. moduleauthor:: Doug Womack <dwomack@encompass.tv>

Example:

>>> print baseDir
c:\\Users\\dwomack\\mobaxterm\\home\\Code\\Python\\agentdan\\AgentDan
>>> print runDir
c:\\Users\\dwomack\\mobaxterm\\home\\Code\\Python\\agentdan\\AgentDan\\..\\run\\
>>> print configDir
c:\\Users\\dwomack\\mobaxterm\\home\\Code\\Python\\agentdan\\AgentDan\\..\\conf\\
>>> print logDir
c:\\Users\\dwomack\\mobaxterm\\home\\Code\\Python\\agentdan\\AgentDan\\..\\log\\
>>> print configFile
c:\\Users\\dwomack\\mobaxterm\\home\\Code\\Python\\agentdan\\AgentDan\\..\\conf\\AgentDan.conf
>>> print logFile
c:\\Users\\dwomack\\mobaxterm\\home\\Code\\Python\\agentdan\\AgentDan\\..\\log\\AgentDan.log
"""          
import os
import sys
import logging
import logging.config

# Get the right directory based on execution location
# if running doctest, or running in root of AgentDan
# if running anywhere other than root of AgentDan
baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
if ('conf' not in baseDir) and ('AgentDan' not in baseDir) and ('agentdan' in baseDir):
    runDir = '{0}{1}run{2}'.format(baseDir,os.sep,os.sep)
    configDir = '{0}{1}conf{2}'.format(baseDir,os.sep,os.sep)
    logDir = '{0}{1}log{2}'.format(baseDir,os.sep,os.sep)
elif ('agentdan' not in baseDir):
    baseDir = os.getcwd()
    runDir = '{0}{1}run{2}'.format(baseDir,os.sep,os.sep)
    configDir = '{0}{1}conf{2}'.format(baseDir,os.sep,os.sep)
    logDir = '{0}{1}log{2}'.format(baseDir,os.sep,os.sep)   
else:
    runDir = '{0}{1}{2}{3}run{4}'.format(baseDir,os.sep,os.pardir,os.sep,os.sep)
    configDir = '{0}{1}{2}{3}conf{4}'.format(baseDir,os.sep,os.pardir,os.sep,os.sep)
    logDir = '{0}{1}{2}{3}log{4}'.format(baseDir,os.sep,os.pardir,os.sep,os.sep)       

configFile = '{0}{1}'.format(configDir, 'AgentDan.conf')
logFile = '{0}{1}'.format(logDir, 'AgentDan.log')
logging.config.fileConfig(configFile, defaults={'iniLogFilePath': logFile})   
log = logging.getLogger('root')

if __name__ == '__main__':
    import doctest
    results = doctest.testmod(verbose=True)
    print results
