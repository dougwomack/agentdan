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

class Conductor:
    """
    .. py:class:: Conductor
    
    A generic class library to create an instance of Conductor for monitoring and configuration
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """       
    def __init__(self):
        """
        .. py:method:: Conductor.__init__()

        Instantiate an instance of Conductor

        :return: Instance of Conductor
        :rtype: obj
        
        :Example:
        
        >>> ec = Conductor()
        >>> eval(repr(ec))
        Conductor()
        """
            
    def __str__(self):
        """
        .. py:method:: Conductor.__str__()

        Return a readable string representation of an instance

        :return: String representation of Conductor instance
        :rtype: str
        
        :Example:
        
        >>> ec = Conductor()
        >>> print ec
        Conductor: { }
        """
        return 'Conductor: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: Conductor.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> ec = Conductor()
        >>> print repr(ec)
        Conductor()
        """
        return 'Conductor()'
        
    def getConductors(self):
        """
        .. py:method:: Conductor.getConductors()

        Returns the device names and addresses from the configuration file section defined for [Elemental Conductor]

        :return: A dictionary of device ips and list of monitored channels
        :rtype: dict
        :exception Exception: General exception with logged results

        :Example:
            
        >>> ec = Conductor()
        >>> print ec.getConductors()
        {'10.16.27.20': '[5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]'}
        """
        try:
            conductors = {}
            cf = ConfigFile('Device.conf')
            for device, address in cf.getConfig('Elemental Conductor').iteritems():
                conductors[device] = address               
            return conductors
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def getChannels(self):
        """
        Class method to retrieve list of channel from all configured Elemental Conductors

        :return: A dictionary for each Conductor containing a dictionary of each channels details
        :rtype: dict
        :exception Exception: General exception with logged results

        :Example:
        
        >>> ec = Conductor()
        >>> results = ec.getChannels()
        >>> print results['10.16.27.20'][0]
        200
        """
        try:
            ec = self.getConductors()
            path = '/channels?metacounts=true'
            payload = ''
            channels = {}
            for address, chanList in ec.iteritems():
                con = Connect('Conductor')
                channels[address] = con.get(path, payload, address)
            return channels
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def getChannel(self):
        """
        Class method to retrieve individual channel attributes
        
        :return: A dictionary for each Conductor containing a dictionary of a channels details
        :rtype: dict
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> ec = Conductor()
        >>> results = ec.getChannel()
        >>> print type(results)
        <type 'dict'>
        """
        try:
            results = {}
            ec = self.getConductors()
            for address,chanList in ec.iteritems():
                channels = {}                
                for chan in json.loads(chanList):
                    path = '/channels/{0}?metacounts=true'.format(chan)
                    payload = ''
                    con = Connect('Conductor')
                    channels[chan] = con.get(path, payload, address)
                results[address] = channels
            return results
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def checkStatus(self):
        """
        Class method to retrieve individual channels from Conductor and
        compare last state to current state. Based on comparison, trigger
        or resolve alerts based on incident_key
        
        :return: A list containing a status code and status message
        :rtype: list
        :exception Exception: General exception with logged results

        :Example:
        
        >>> ec = Conductor()
        >>> status, results = ec.checkStatus()
        >>> print results
        Conductor: Check completed successfully!
        """        
        # Instantiate Conductor and PagerDuty
        pd = PagerDuty()
        cf = ConfigFile('conductor.json')
        
        # Get previous state
        lastState = cf.getState()

        # Get channels with current status
        channels = self.getChannel()
        
        # If request was successful, iterate over channels checking current status.
        # For all status results that are not currently running trigger a PagerDuty 
        # incident
        currentState = defaultdict(dict)
        try:
            for server, response in channels.iteritems():
                for status, channels in response.iteritems():
                    details = {}
                    channel = channels[1]['channel']
                    incident_key = '{0} state change'.format(channel['name'])
                    description = "Channel {0} is currently {1} on {2}".format(channel['name'], channel['status'], server)
                    client = server
                    url = 'http://{0}'.format(server)
                    for value in channel['channel_params']['channel_param']:
                        details[value['name']] = value['value']
                    currentState[server][channel['id']['#text']] = channel['status']
                    if len(lastState) != 0:
                        for lastId, lastStatus in lastState[server].iteritems():
                            if channel['id']['#text'] == lastId:
                                if channel['status'] != lastStatus:
                                    # Status: Active, Complete, Error, Idle, Pending, Postprocessing, Preprocessing, Running
                                    # Started, Starting, Stopping, Suspended, Unknown, Unreachable
                                    if channel['status'] == 'running':
                                        # Current state is running so resolve PagerDuty
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
                return [200, 'Conductor: Check completed successfully!']
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return [500, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)]      

if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results        
