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

class Delta:
    """
    .. py:class:: Delta
    
    A generic class library to create an instance of Delta for monitoring and configuration
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """       
    def __init__(self):
        """
        .. py:method:: Delta.__init__()

        Instantiate an instance of Delta

        :return: Instance of Delta
        :rtype: obj
        
        :Example:
        
        >>> ec = Delta()
        >>> eval(repr(ec))
        Delta()
        """
            
    def __str__(self):
        """
        .. py:method:: Delta.__str__()

        Return a readable string representation of an instance

        :return: String representation of Delta instance
        :rtype: str
        
        :Example:
        
        >>> ec = Delta()
        >>> print ec
        Delta: { }
        """
        return 'Delta: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: Delta.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> ec = Delta()
        >>> print repr(ec)
        Delta()
        """
        return 'Delta()'
        
    def getDeltas(self):
        """
        .. py:method:: Delta.getDeltas()

        Returns the device names and addresses from the configuration file section defined for [Elemental Delta]

        :return: A dictionary of device ips and list of monitored channels
        :rtype: dict
        :exception Exception: General exception with logged results

        :Example:
        
        >>> ec = Delta()
        >>> print ec.getDeltas()
        {'10.16.255.21': '[364,366]', '10.16.255.22': '[68]'}
        """
        try:
            conductors = {}
            cf = ConfigFile('Device.conf')
            for device, address in cf.getConfig('Elemental Delta').iteritems():
                conductors[device] = address               
            return conductors
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def getChannels(self):
        """
        Class method to retrieve list of channel from all configured Elemental Deltas

        :return: A dictionary for each Delta containing a dictionary of each channels details
        :rtype: dict
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> ec = Delta()
        >>> results = ec.getChannels()
        >>> print results['10.16.27.20'][0]
        200
        """
        try:
            ec = self.getDeltas()
            path = '/contents'
            payload = ''
            channels = {}
            for address, chanList in ec.iteritems():
                con = Connect('Delta')
                channels[address] = con.get(path, payload, address)
            return channels
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def getChannel(self):
        """
        Class method to retrieve individual channel attributes
        
        :return: A dictionary for each Delta containing a dictionary of a channels details
        :rtype: dict
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> ec = Delta()
        >>> results = ec.getChannel()
        >>> print type(results)
        <type 'dict'>
        """
        try:
            results = {}
            ec = self.getDeltas()
            for address,chanList in ec.iteritems():
                channels = {}                
                for chan in json.loads(chanList):
                    path = '/contents/{0}'.format(chan)
                    payload = ''
                    con = Connect('Delta')
                    channels[chan] = con.get(path, payload, address)
                results[address] = channels
            return results
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def checkStatus(self):
        """
        Class method to retrieve individual channels from Delta and
        compare last state to current state. Based on comparison, trigger
        or resolve alerts based on incident_key
        
        :return: A list containing a status code and status message
        :rtype: list
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> ec = Delta()
        >>> results = ec.checkStatus()
        >>> print results
        [200, 'Delta: Check completed successfully!']
        """        
        # Instantiate Delta and PagerDuty
        pd = PagerDuty()
        cf = ConfigFile('delta.json')
        
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
                                            config.log.info('Resolve: {0} with Incident Key: {1} {2}fully!'.format(rret['message'], rret['incident_key'], rret['status']))
                                        else:
                                            config.log.warn('Resolve: {0} with Incident Key: {1} {2}!'.format(rret['message'], rret['incident_key'], rret['status']))
                                    else:
                                        # Current state is not running trigger PagerDuty
                                        tstatus, tresult = pd.trigger(incident_key, description, client, url, details)
                                        tret = json.loads(tresult)
                                        if tstatus == 200:
                                            config.log.info('Trigger: {0} with Incident Key: {1} {2}fully!'.format(tret['message'], tret['incident_key'], tret['status']))
                                        else:
                                            config.log.warn('Trigger: {0} with Incident Key: {1} {2}!'.format(tret['message'], tret['incident_key'], tret['status']))
            retStatus, retState = cf.setState(currentState)
            if retStatus == 200:
                config.log.info('Status: {0} - {1}'.format(retStatus, retState))
                return [200, 'Delta: Check completed successfully!']
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return [500, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)]    

if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results        
