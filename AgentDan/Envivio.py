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

class Envivio:
    """
    .. py:class:: Envivio
    
    A generic class library to create an instance of Envivio for monitoring and configuration
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """       
    def __init__(self):
        """
        .. py:method:: Envivio.__init__()

        Instantiate an instance of Envivio

        :return: Instance of Envivio
        :rtype: obj
        
        :Example:

        >>> eh = Envivio()
        >>> eval(repr(eh))
        Envivio()
        """
            
    def __str__(self):
        """
        .. py:method:: Envivio.__str__()

        Return a readable string representation of an instance

        :return: String representation of Envivio instance
        :rtype: str
        
        :Example:
        
        >>> eh = Envivio()
        >>> print eh
        Envivio: { }
        """
        return 'Envivio: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: Envivio.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> eh = Envivio()
        >>> print repr(eh)
        Envivio()
        """
        return 'Envivio()'
        
    def getEnvivios(self):
        """
        .. py:method:: Envivio.getEnvivios()

        Returns the device names and addresses from the configuration file section defined for [Elemental Envivio]

        :return: A list of device ips
        :rtype: list
        :exception Exception: General exception with logged results
        
        :Example:
            
        >>> eh = Envivio()
        >>> print eh.getEnvivios()
        defaultdict(<type 'dict'>, {'10.16.27.42': '["Channel 03", "Channel 04"]', '10.16.27.41': '["Channel 01", "Channel 02"]'})
        """
        try:
            Envivios = defaultdict(dict)
            cf = ConfigFile('Device.conf')
            for device, address in cf.getConfig('Envivio Halo').iteritems():
                Envivios[device] = address               
            return Envivios
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)

    def getChannels(self):
        """
        Class method to retrieve list of channel from all configured Envivio Halos

        :return: A dictionary for each Halo containing a dictionary of each channel
        :rtype: dict
        :exception Exception: General exception with logged results

        :Example:
        
        >>> eh = Envivio()
        >>> results = eh.getChannels()
        >>> print results['10.16.27.41'][0]
        200
        """
        try:
            con = Connect('Envivio')
            eh = self.getEnvivios()
            path = '/api/services'
            payload = ''
            channels = defaultdict(dict)
            results = defaultdict(dict)
            for address, chanList in eh.iteritems():
                channels[address] = con.get(path, payload, address)
            return channels
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
   
    def getChannel(self):
        """
        Class method to retrieve individual channel attributes
        
        :return: A dictionary for each Envivio Halo containing a dictionary of a channels details
        :rtype: dict
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> eh = Envivio()
        >>> results = eh.getChannel()
        >>> print type(results)
        <type 'collections.defaultdict'>
        """
        try:
            con = Connect('Envivio')
            eh = self.getEnvivios()
            channels = self.getChannels()
            results = defaultdict(dict)
            for address, channel in channels.iteritems():
                details = defaultdict(dict)
                for attr in channel[1]['services']['service']:
                    for server, chanList in eh.iteritems():
                        for title in json.loads(chanList):
                            if address == server:
                                if title == attr['@title']:
                                    path = attr['@href']
                                    payload = ''
                                    details[title] = con.get(path, payload, address)
                                    results[address] = details
            return results
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def checkStatus(self):
        """
        Class method to retrieve individual channels from Envivio Halo and
        compare last state to current state. Based on comparison, trigger
        or resolve alerts based on incident_key

        :return: A list containing a status code and status message
        :rtype: list
        :exception Exception: General exception with logged results

        :Example:

        >>> eh = Envivio()
        >>> status, results = eh.checkStatus()
        >>> print results
        Envivio: Check completed successfully!
        """        
        # Instantiate Conductor and PagerDuty
        con = Connect('Envivio')
        pd = PagerDuty()
        cf = ConfigFile('envivio.json')
    
        # Get previous state
        lastState = cf.getState()
    
        # Get channels with current status
        channels = self.getChannel()
    
        # If request was successful, iterate over channels checking current status.
        # For all status results that are not currently running trigger a PagerDuty 
        # incident
        currentState = defaultdict(dict)        
        try:
            for address, service in channels.iteritems():
                for title, channel in service.iteritems():
                    for name, outputs in channel[1]['service']['outputs'].iteritems():
                        for output in outputs:
                            if type(output) is dict:
                                path = '{0}{1}'.format(output['@href'], 'status')
                                payload = ''
                                response = con.get(path, payload, address)
                                outputName = output['@title']
                                outputType = output['@type']
                                status = response[1]['output']['state']
                                incident_key = '{0}({1}) state change on {2}'.format(title, outputType, address)
                                description = '{0}({1}) is currently {2} on {3}'.format(outputName, outputType, status, address)
                                client = address
                                url = 'http://{0}:8080'.format(address)
                                chanOutput = '{0}|{1}'.format(title, outputType)
                                currentState[address][chanOutput] = status
                                if len(lastState) != 0:
                                    for lastId, lastStatus in lastState[address].iteritems():
                                        currentId = '{0}|{1}'.format(title, outputType)
                                        #lastTitle, lastType = lastId.split('|')
                                        if currentId == lastId:
                                            if status != lastStatus:
                                                # Status: Active, Complete, Error, Idle, Pending, Postprocessing, Preprocessing, Running
                                                # Started, Starting, Stopping, Suspended, Unknown, Unreachable
                                                if status == 'started':
                                                    #Current state is running so resolve PagerDuty
                                                    rstatus, rresult = pd.resolve(incident_key, description, details)
                                                    rret = json.loads(rresult)
                                                    if rstatus == 200:
                                                        config.log.info('Resolve: {0} with Incident Key: {1} {2}ful!'.format(rret['message'], rret['incident_key'], rret['status']))
                                                    else:
                                                        config.log.warn('Resolve: {0} with Incident Key: {1} {2}!'.format(rret['message'], rret['incident_key'], rret['status']))
                                                else:
                                                    # Current state is not running trigger PagerDuty
                                                    tstatus, tresult = pd.trigger(incident_key, description, client, url, details)
                                                    tret = json.loads(tresult)
                                                    if tstatus == 200:
                                                        config.log.info('Trigger: {0} with Incident Key: {1} {2}ful!'.format(tret['message'], tret['incident_key'], tret['status']))
                                                    else:
                                                        config.log.warn('Trigger: {0} with Incident Key: {1} {2}!'.format(tret['message'], tret['incident_key'], tret['status']))
            retStatus, retState = cf.setState(currentState)
            if retStatus == 200:
                config.log.info('Status: {0} - {1}'.format(retStatus, retState))
                return [200, 'Envivio: Check completed successfully!']
            else:
                return [500, 'shit']
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results        
