#!/usr/bin/env python
import config
import os
import sys
import json
from pprint import pformat
from collections import defaultdict
from Connect import Connect
from ConfigFile import ConfigFile
from PagerDuty import PagerDuty

class MediaExcel:
    """
    .. py:class:: MediaExcel
    
    A generic class library to create an instance of MediaExcel for monitoring and configuration
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """       
    def __init__(self):
        """
        .. py:method:: MediaExcel.__init__()

        Instantiate an instance of MediaExcel

        :return: Instance of MediaExcel
        :rtype: obj
        
        :Example:

        >>> me = MediaExcel()
        >>> eval(repr(me))
        MediaExcel()
        """
            
    def __str__(self):
        """
        .. py:method:: MediaExcel.__str__()

        Return a readable string representation of an instance

        :return: String representation of MediaExcel instance
        :rtype: str
        
        :Example:
        
        >>> me = MediaExcel()
        >>> print me
        MediaExcel: { }
        """
        return 'MediaExcel: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: MediaExcel.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> me = MediaExcel()
        >>> print repr(me)
        MediaExcel()
        """
        return 'MediaExcel()'
        
    def getMediaExcels(self):
        """
        .. py:method:: MediaExcel.getMediaExcels()

        Returns the device names and addresses from the configuration file section defined for [Elemental MediaExcel]

        :return: A list of device ips
        :rtype: list
        :exception Exception: General exception with logged results
        
        :Example:
            
        >>> me = MediaExcel()
        >>> print me.getMediaExcels()
        {'10.1.1.1': '[]'}
        """
        try:
            MediaExcels = {}
            cf = ConfigFile('Device.conf')
            for device, address in cf.getConfig('MediaExcel').iteritems():
                MediaExcels[device] = address               
            return MediaExcels
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)

if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results        
