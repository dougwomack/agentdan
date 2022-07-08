#!/usr/bin/env python
import config
import requests
import json
import datetime
from pprint import pformat
from Connect import Connect
from ConfigFile import ConfigFile
from Incident import Incident
from Alert import Alert

class PagerDuty:
    """
    .. py:class:: PagerDuty
    
    A class library to enable integration with PagerDuty API
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """    
    def __init__(self):
        """
        .. py:method:: PagerDuty.__init__()

        Instantiate an instance of PagerDuty

        :return: Instance of PagerDuty
        :rtype: obj
        :exception IOError: If AgentDan.conf does not exists, or permission denied
        :exception TypeError: Value type is incorrect for requested key
        :exception Exception: General exception with logged results

        :Example:

        >>> pd = PagerDuty()
        >>> eval(repr(pd))
        PagerDuty()
        """            
        try:
            cf = ConfigFile('Device.conf')
            pdConfig = cf.getConfig('PagerDuty')   
            self.service_key = pdConfig['service_key']
        except IOError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'IOError:', e))
        except TypeError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'TypeError:', e))
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))    
            
    def __getitem__(self, key):
        """
        .. py:method:: PagerDuty.__getitem__(key)

        Returns the value of an instance attribute

        :param key: The attribute name to retrieve
        :type key: str
        :return: The attribute's value
        :rtype: str
        :exception AttributeError: If the attribute name provided does not exists
        :exception Exception: General exception with logged results

        :Example:

        >>> pd = PagerDuty()
        >>> print pd['service_key']
        88fd1c835c374369b81ff95b9e4c07de
        """
        try:
            return getattr(self, key) 
        except AttributeError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e)
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def __setitem__(self, key, value):
        """
        .. py:method:: PagerDuty.__setitem__(key, value)

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

        >>> pd = PagerDuty()
        >>> pd.__setitem__('service_key', 'servicekey')
        'servicekey'
        >>> print pd['service_key']
        servicekey
        """
        try:
            setattr(self, key, value)
            return value
        except AttributeError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e)
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)        
    
    def __str__(self):
        """
        .. py:method:: PagerDuty.__str__()

        Return a readable string representation of an instance

        :return: String representation of PagerDuty instance
        :rtype: str

        :Example:

        >>> pd = PagerDuty()
        >>> print pd
        PagerDuty: { 'service_key': '88fd1c835c374369b81ff95b9e4c07de'}
        """
        return 'PagerDuty: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: PagerDuty.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str

        :Example:

        >>> pd = PagerDuty()
        >>> print repr(pd)
        PagerDuty()
        """
        return 'PagerDuty()'
    
    def trigger(self, incident_key, description, client, url, details):
        """
        .. py:method:: PagerDuty.trigger(incident_key, description, client, url, details)

        Trigger an incident through PagerDuty API via Connect module  

        :param incident_key: A unique string which provides de-duplication
        :type incidient_key: str
        :param description: A detailed description of the incident
        :type description: str
        :param client: Affected device name
        :type client: str
        :param url: URL to affected device adminstrative interface
        :type url: str
        :param details: Full details regarding the initial event that triggered this incident
        :type details: str
        :return: JSON string (JSON string)
        :rtype: str

        :Example:

        >>> #pd = PagerDuty()
        >>> #incident_key = "srv01/HTTP"
        >>> #description = "Channel {0} is currently {1} on {2}".format('21','idle','10.16.27.20')
        >>> #client = "SkyMX Conductor"
        >>> #url = "http://10.16.27.20"
        >>> #details = {"hls-source": "http://10.16.27.221/out/u/skymx_ch21.m3u8","udl-dest1":"udp://230.16.28.20:52101",}
        >>> #trigstat, trigres = pd.trigger(incident_key, description, client, url, details)
        >>> #trigres = json.loads(trigres)
        >>> #print trigres
        {u'status': u'success', u'message': u'Event processed', u'incident_key': u'srv01/HTTP'}
        """
        payload = json.dumps({
            "service_key": self.service_key,
            "incident_key": incident_key,
            "event_type": "trigger",
            "description": description,
            "client": client,
            "client_url": url,
            "details": details,
        })       
        con = Connect('PagerDuty')
        return con.post(payload)
    
    def resolve(self, incident_key, description, details):
        """
        .. py:method:: PagerDuty.resolve(incident_key, description, details)

        Resolve an incident through PagerDuty API via Connect module  

        :param incident_key: A unique string which provides de-duplication
        :type incidient_key: str
        :param description: A detailed description of the resolution
        :type description: str
        :param details: Full details regarding incident resolution
        :type details: str
        :return: JSON string (JSON string)
        :rtype: str

        :Example:

        >>> #pd = PagerDuty()
        >>> #incident_key = "srv01/HTTP"
        >>> #description = "Channel {0} is currently {1} on {2}".format('21','running','10.16.27.20')
        >>> #details = {"Resolved at":"2016-03-18 16:00",}
        >>> #trigstat, trigres = pd.resolve(incident_key, description, details)
        >>> #trigres = json.loads(trigres)
        >>> #print trigres
        {u'status': u'success', u'message': u'Event processed', u'incident_key': u'srv01/HTTP'}
        """
        payload = json.dumps({
            "service_key": self.service_key,
            "incident_key": incident_key,
            "event_type": "resolve",
            "description": description,
            "details": details,
        })       
        con = Connect('PagerDuty')
        return con.post(payload)
    
    def getIncidents(self, days, urgency='', status=''):
        """
        .. py:method:: PagerDuty.getIncidents(days, urgency='', status='')

        Retrieve a list of incidents via PagerDuty API  

        :param days: Number of days to query for results
        :type days: str
        :param urgency: Optional Urgency to query Possible values (high, low)
        :type urgency: str
        :param status: Optional Status to query. Possible values (triggered, acknowledged, resolved)
        :type status: str
        :return: JSON string (JSON string)
        :rtype: str

        :Example:

        >>> pd = PagerDuty()
        >>> incidents = pd.getIncidents(1)
        >>> print type(incidents)
        <type 'list'>
        """
        incidents = []
        path = '/api/v1/incidents'
        since = datetime.datetime.now() - datetime.timedelta(days=days)
        since = since.strftime('%Y-%m-%d')
        until = datetime.datetime.now().strftime('%Y-%m-%d')
        if (urgency == ''):
            urgency == 'high,low'
        if (status == ''):
            status = 'triggered,acknowledged,resolved'
        payload = {
            'since':since,
            'until':until,
            'status':status,
        }
        con = Connect('PagerDuty')
        status, response = con.get(path, payload)
        if (status == 200):
            for i in response['incidents']:
                incident_number = i['incident_number']
                status = i['status']
                urgency = i['urgency']
                pending_actions = i['pending_actions']
                created_on = i['created_on']
                html_url = i['html_url']
                incident_key = i['incident_key']
                service = i['service']
                escalation_policy = i['escalation_policy']
                assigned_to = i['assigned_to']
                last_status_change_by = i['last_status_change_by']
                last_status_change_on = i['last_status_change_on']
                trigger_summary_data = i['trigger_summary_data']
                trigger_details_html_url = i['trigger_details_html_url']
                inc = Incident(incident_number, status, urgency, pending_actions, 
                              created_on, html_url, incident_key, 
                              service, escalation_policy, 
                              assigned_to, 
                              last_status_change_by, 
                              last_status_change_on, 
                              trigger_summary_data, 
                              trigger_details_html_url)
                incidents.append(inc)
        elif (status == 404):
            incidents = response
        elif (status == 500):
            incidents = response
        else:
            incidents = response
        return incidents
    
    def getAlerts(self, days):
        """
        .. py:method:: PagerDuty.getAlerts(days)

        Retrieve a list of alerts via PagerDuty API  

        :param days: Number of days to query for results
        :type days: str
        :return: JSON string (JSON string)
        :rtype: str

        :Example:

        >>> pd = PagerDuty()
        >>> alerts = pd.getAlerts(1)
        >>> print type(alerts)
        <type 'list'>
        """        
        alerts = []
        path = '/api/v1/alerts'
        since = datetime.datetime.now() - datetime.timedelta(days=days)
        since = since.strftime('%Y-%m-%d')
        until = datetime.datetime.now().strftime('%Y-%m-%d')
        payload =  {
            'since':since,
            'until':until,
        }
        con = Connect('PagerDuty')
        status, response = con.get(path, payload)
        if (status == 200):
            for i in response['alerts']:
                alertId = i['id']
                alertType = i['type']
                started_at = i['started_at']
                try:
                    address = i['address']
                except KeyError:
                    address = ''
                user = i['user']
                alert = Alert(alertId, alertType, started_at, address, user)
                alerts.append(alert)
        elif (status == 404):
            alerts = response
        elif (status == 500):
            alerts = response
        else:
            alerts = response                
        return alerts

if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results            