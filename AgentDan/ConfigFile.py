#!/usr/bin/env python
import config
import sys
import os
import json
import ConfigParser
from pprint import pformat

class ConfigFile:
    """
    .. py:class:: ConfigFile
    
    A class library to create an instance of ConfigFile for configuration information
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """        
    def __init__(self, fp):
        """
        .. py:method:: ConfigFile.__init__(fp)

        Instantiate an instance of ConfigFile

        :param fp: Real path and filename to AgentDan.conf
        :type fp: str
        :return: Instance of ConfigFile
        :rtype: obj
        :exception IOError: If AgentDan.conf does not exists, or permission denied
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> cf = ConfigFile('AgentDan.conf')
        >>> eval(repr(cf))
        ConfigFile('AgentDan.conf')
        """
        self.fp = fp

    def __getitem__(self, key):
        """
        .. py:method:: ConfigFile.__getitem__(key)
    
        Returns the value of an instance attribute
    
        :param key: The attribute name to retrieve
        :type key: str
        :return: The attribute's value
        :rtype: str
        :exception AttributeError: If the attribute name provided does not exists
        
        :Example:
        
        >>> cf = ConfigFile('AgentDan.conf')
        >>> print cf['fp']
        AgentDan.conf
        """
        try:
            return getattr(self, key) 
        except AttributeError as e:
            config.log.error('{0} : {1}'.format('AttributeError:', e))
            return 'AttributeError: {0}'.format(e)
        except Exception as e:
            config.log.error('{0} : {1}'.format('Error:', e))        
            return 'Error: {0}'.format(e)
        
    def __setitem__(self, key, value):
        """
        .. py:method:: ConfigFile.__setitem__(key, value)
    
        Sets the value of an instance attribute
    
        :param key: The attribute name to set
        :type key: str
        :param value: The value to assign to the attribute
        :type value: str
        :return: The attribute's new value
        :rtype: str
        :exception AttributeError: If the attribute name provided does not exists
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> cf = ConfigFile('AgentDan.conf')
        >>> cf.__setitem__('fp', 'Device.conf')
        'Device.conf'
        >>> print cf['fp']
        Device.conf
        """
        try:
            setattr(self, key, value)
            return value
        except AttributeError as e:
            config.log.error('{0} : {1}'.format('AttributeError:', e))
            return 'AttributeError: {0}'.format(e)
        except Exception as e:
            config.log.error('{0} : {1}'.format('Error:', e))        
            return 'Error: {0}'.format(e)
    
    def __str__(self):
        """
        .. py:method:: ConfigFile.__str__()

        Return a readable string representation of an instance

        :return: String representation of ConfigFile instance
        :rtype: str
        
        :Example:
        
        >>> cf = ConfigFile('AgentDan.conf')
        >>> print cf
        ConfigFile: { 'fp': 'AgentDan.conf'}
        """
        return 'ConfigFile: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: ConfigFile.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> cf = ConfigFile('AgentDan.conf')
        >>> print repr(cf)
        ConfigFile('AgentDan.conf')
        """
        return 'ConfigFile(\'{0}\')'.format(self.fp)
    
    def getConfig(self, section):
        """
        .. py:method:: ConfigFile.getConfig(section)
        
        Return a dictionary of config name and config value within provided section  

        :param section: Section within configuration file to retrieve key/value pair
        :type section: str
        :return: Dictionary containing config item name and value
        :rtype: dict{'item key','item value'}
        :exception ConfigParser.NoSectionError: Section does not exists in configuration file
        :exception NameError: Key does not exists in section of configuration file
        :exception TypeError: Value type is incorrect for requested key
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> Config = ConfigFile('Device.conf')
        >>> pdConfig = Config.getConfig('PagerDuty')
        >>> subdomain = pdConfig['subdomain']
        >>> print subdomain
        encompass-digital-media
        """   
        # Return a dict of the requested section from self.fp
        configFile = '{0}{1}'.format(config.configDir, self.fp)
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(configFile)
            dictSection = {}
            options = Config.options(section)
            for option in options:
                dictSection[option] = Config.get(section, option)
                if dictSection[option] == -1:
                    DebugPrint("skip: %s" % option)
            return dictSection
        except ConfigParser.NoSectionError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'NoSectionError:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'NoSectionError:', e)
        except NameError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'NameError:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'NameError:', e)
        except TypeError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'TypeError:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'TypeError:', e)            
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)            
        
    def getState(self):
        """
        .. py:method:: ConfigFile.getState()
        
        Return a dictionary created from a JSON file containing 
        channel and previous states for devices and monitored channels 
        defined in Device.conf

        :return: JSON string containing read from JSON file
        :rtype: str
        :exception IOError: JSON file does not exists, so create it and return empty lastState dictionary
        :exception ValueError: JSON string in file is mailformed or empty, so return empty lastState dictionary
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> cf = ConfigFile('conductor.json')
        >>> lastState = cf.getState()
        >>> print lastState
        {u'10.16.27.20': {u'11': u'running', u'10': u'running', u'13': u'running', u'12': u'running', u'15': u'running', u'14': u'running', u'17': u'running', u'16': u'running', u'19': u'running', u'18': u'running', u'6': u'running', u'22': u'running', u'5': u'running', u'8': u'running', u'7': u'running', u'24': u'running', u'9': u'running', u'20': u'running', u'23': u'running', u'21': u'running'}}
        """           
        # Get State file
        stateFile = '{0}{1}'.format(config.runDir, self.fp)

        # Read JSON data from stateFile, if empty, set lastState to empty dict in value exception
        # If doesn't exists, create empty file
        try:
            with open(stateFile, 'r+') as jf:
                lastState = json.load(jf)
        except IOError as e:
            # stateFile doesn't exists, so create and write empty dict
            lastState = ''
            fd = open(stateFile,'w+')
            fd.write(lastState)
            fd.close()
            config.log.info('IOError: {0} does not exists, creating!'.format(stateFile))
            return lastState
        except ValueError as e:
            lastState = {}
            config.log.info('{0}:{1}:{2} {3}'.format(sys.argv[0], sys.exc_info()[-1].tb_lineno, 'ValueError:', e))
            config.log.info('{0}:{1}:{2} {3}'.format(sys.argv[0], sys.exc_info()[-1].tb_lineno, 'ValueError:', 'Returning empty dict.'))
            return lastState
        except Exception as e:
            lastState = {}
            config.log.error('{0}:{1}:{2} {3}'.format(sys.argv[0], sys.exc_info()[-1].tb_lineno, 'Exception:', e))             
            return lastState
        return lastState
        
    def setState(self, currentState):
        """
        .. py:method:: ConfigFile.setState()
        
        Write a dictionary to a JSON file containing 
        channel and previous states for devices and monitored channels 
        defined in Device.conf

        :return: List contain status code and status message of state write to file
        :rtype: list
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> cf = ConfigFile('conductor.json')
        >>> lastState = cf.getState()
        >>> print lastState
        {u'10.16.27.20': {u'11': u'running', u'10': u'running', u'13': u'running', u'12': u'running', u'15': u'running', u'14': u'running', u'17': u'running', u'16': u'running', u'19': u'running', u'18': u'running', u'6': u'running', u'22': u'running', u'5': u'running', u'8': u'running', u'7': u'running', u'24': u'running', u'9': u'running', u'20': u'running', u'23': u'running', u'21': u'running'}}
        """                   
        self.currentState = currentState
        # Get State file
        stateFile = '{0}{1}'.format(config.runDir, self.fp)
        with open(stateFile, 'w+') as fp:
            try:        
                json.dump(self.currentState, fp, sort_keys=True, indent=4)
            except Exception as e:
                config.log.error('{0}:{1}:{2} {3}'.format(sys.argv[0], sys.exc_info()[-1].tb_lineno, 'Exception:', e))
                return [500, '{0}:{1}:{2} {3}'.format(sys.argv[0], sys.exc_info()[-1].tb_lineno, 'Exception:', e)] 
            return [200, 'State saved!']
    
if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results
