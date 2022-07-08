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

class Live:
    """
    .. py:class:: Live
    
    A generic class library to create an instance of Live for monitoring and configuration
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """       
    def __init__(self):
        """
        .. py:method:: Live.__init__()

        Instantiate an instance of Live

        :return: Instance of Live
        :rtype: obj
        
        :Example:

        >>> ed = Live()
        >>> eval(repr(ed))
        Live()
        """
            
    def __str__(self):
        """
        .. py:method:: Live.__str__()

        Return a readable string representation of an instance

        :return: String representation of Live instance
        :rtype: str
        
        :Example:
        
        >>> ed = Live()
        >>> print ed
        Live: { }
        """
        return 'Live: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: Live.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> ed = Live()
        >>> print repr(ed)
        Live()
        """
        return 'Live()'
        
    def getLives(self):
        """
        .. py:method:: Live.getLives()

        Returns the device names and addresses from the configuration file section defined for [Elemental Live]

        :return: A dictionary of device ips and list of monitored channels
        :rtype: dict
        :exception Exception: General exception with logged results
        
        :Example:
            
        >>> ed = Live()
        >>> print ed.getLives()
        {'10.16.27.21': '[246,248,249,251,252,253,254,255,256,258]', '10.16.27.22': '[256,261,262,263,264,265,266,267,268,269]', '10.16.27.23': '[]'}
        """
        try:
            Lives = {}
            cf = ConfigFile('Device.conf')
            for device, address in cf.getConfig('Elemental Live').iteritems():
                Lives[device] = address  
            return Lives
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)

    def getChannels(self):
        """
        Class method to retrieve list of channel from all configured Elemental Lives

        :return: A dictionary for each Live containing a dictionary of each channels details
        :rtype: dict
        :exception Exception: General exception with logged results

        :Example:
        
        >>> ed = Live()
        >>> results = ed.getChannels()
        >>> print results['10.16.27.21'][0]
        200
        """
        try:
            ed = self.getLives()
            path = '/api/live_events?page=1&per_page=20'
            payload = ''
            channels = {}
            for address, chanList in ed.iteritems():
                con = Connect('Live')
                channels[address] = con.get(path, payload, address)
            return channels
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
    
    def getChannel(self):
        """
        Class method to retrieve individual channel attributes
        
        :return: A dictionary for each Live containing a dictionary of a channels details
        :rtype: dict
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> ed = Live()
        >>> results = ed.getChannel()
        >>> print type(results)
        <type 'dict'>
        """
        try:
            results = {}
            ed = self.getLives()
            for address,chanList in ed.iteritems():
                channels = {}
                for chan in json.loads(chanList):
                    path = '/api/live_events/{0}'.format(chan)
                    payload = ''
                    con = Connect('Live')
                    channels[chan] = con.get(path, payload, address)
                results[address] = channels
            return results
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def checkStatus(self):
        """
        Class method to retrieve individual channels from Live and
        compare last state to current state. Based on comparison, trigger
        or resolve alerts based on incident_key
        
        :return: A list containing a status code and status message
        :rtype: list
        :exception Exception: General exception with logged results

        :Example:
        
        >>> ed = Live()
        >>> results = ed.checkStatus()
        >>> print results
        [200, 'Live: Check completed successfully!']
        """        
        # Instantiate Live and PagerDuty
        pd = PagerDuty()
        cf = ConfigFile('live.json')
        
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
                    channel = channels[1]['live_event']
                    incident_key = '{0} state change'.format(channel['name'])
                    description = "Channel {0} is currently {1} on {2}".format(channel['name'], channel['status'], channel['node'])
                    client = server
                    url = 'http://{0}'.format(server)
                    input_name = '{0}: {1}'.format('Input', channel['input']['id'])
                    details[input_name]= channel['input']['network_input']['uri']
                    for value in channel['output_group']['output']:
                        output_name = '{0}: {1}'.format('Output', value['id'])
                        details[output_name] = value['full_uri']
                    currentState[server][channel['input']['id']] = channel['status']
                    if len(lastState) != 0:
                        for lastId, lastStatus in lastState[server].iteritems():
                            if channel['id'] == lastId:
                                if channel['status'] != lastStatus:
                                    # Status: Active, Complete, Error, Idle, Pending, Postprocessing, Preprocessing, Running
                                    # Started, Starting, Stopping, Suspended, Unknown, Unreachable
                                    if channel['status'] == 'running':
                                        #Current state is running so resolve PagerDuty
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
                return [200, 'Live: Check completed successfully!']
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return [500, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)]      
        
if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results        
