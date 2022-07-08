#!/usr/bin/env python
import config
import os
import sys
import json
import requests
import xmltodict
from pprint import pformat
from ConfigFile import ConfigFile

class Connect:
    """
    .. py:class:: Connect
    
    A generic class library to support connections to various RESTful APIs 
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """    
    def __init__(self, service=''):
        """
        .. py:method:: Connect.__init__(service='PagerDuty')
        
        Instantiate an instance of Connect
        
        :param service: The name of the service to connect too
        :type service: PagerDuty|Conductor
        :return: Instance of Connect
        :rtype: obj
        :exception IOError: If AgentDan.conf does not exists, or permission denied
        :exception TypeError: Value type is incorrect for requested key
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> con = Connect('PagerDuty')
        >>> eval(repr(con))
        Connect('PagerDuty')
        """
        try:
            self.service = service
            if self.service == 'PagerDuty':
                cf = ConfigFile('Device.conf')
                pdConfig = cf.getConfig('PagerDuty')
                self.subdomain = pdConfig['subdomain']
                self.key = pdConfig['api_key']
        except IOError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'IOError:', e))
        except TypeError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'TypeError:', e))
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            # Need to exit here in daemon mode
            
    def __getitem__(self, key):
        """
        .. py:method:: Connect.__getitem__(key)
        
        Returns the value of an instance attribute
        
        :param key: The attribute name to retrieve
        :type key: str
        :return: The attribute's value
        :rtype: str
        :exception AttributeError: If the attribute name provided does not exists
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> con = Connect('PagerDuty')
        >>> print con['service']
        PagerDuty
        """
        try:
            return getattr(self, key) 
        except AttributeError:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e)
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)    
        
    def __setitem__(self, key, value):
        """
        .. py:method:: Connect.__setitem__(key, value)
        
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
        
        >>> con = Connect()
        >>> con.__setitem__('service', 'Conductor')
        'Conductor'
        >>> print con['service']
        Conductor
        """
        try:
            setattr(self, key, value)
            return value
        except AttributeError:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e)
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def __str__(self):
        """
        .. py:method:: Connect.__str__()
        
        Return a readable string representation of an instance
        
        :return: String representation of Connect instance
        :rtype: str
        
        :Example:
        
        >>> con = Connect('PagerDuty')
        >>> print con
        Connect: { 'key': 'yz8bPMfGX1GBqV6yqVkT',
          'service': 'PagerDuty',
          'subdomain': 'encompass-digital-media'}
        """
        return 'Connect: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))        

    def __repr__(self):
        """
        .. py:method:: Connect.__repr__()
        
        Return a string representation readable by the interpreter  
        
        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> from Connect import Connect
        >>> con = Connect('PagerDuty')
        >>> print repr(con)
        Connect('PagerDuty')
        """
        return 'Connect(\'{0}\')'.format(self.service)
    
    def get(self, path, payload, address=''):
        """
        .. py:method:: Connect.get(path, payload, address=)
        
        Returns a json string containing the results of the API query
        
        :param path: URL path to the API resource
        :type path: str
        :param payload: JSON formatted API parameters
        :type payload: str
        :return: Status code of request and the JSON formatted response from API
        :rtype: dict{'status_code','JSON string'}
        :exception ConnectionError: In case of network problem (e.g. DNS failure, refused connection, etc)
        :exception HTTPError: In the event of the rare invalid HTTP response
        :exception TooManyRedirects: If a request times out, a Timeout exception is raised. If a request exceeds the configured number of maximum redirections
        :exception Exception: General exception with logged results

        .. Todo:: Handle Connection, HTTP and Redirects exceptions.
        
        :Example:
        
        >>> import requests
        >>> import json
        >>> import datetime
        >>> from Connect import Connect
        >>> days = 1
        >>> path = '/api/v1/incidents'
        >>> since = datetime.datetime.now() - datetime.timedelta(days=days)
        >>> since = since.strftime('%Y-%m-%d')
        >>> until = datetime.datetime.now().strftime('%Y-%m-%d')
        >>> status = 'resolved'
        >>> payload = {'since':since,'until':until,'status':status}
        >>> con = Connect('PagerDuty')
        >>> status, response = con.get(path, payload)                
        >>> print status
        200
        """        
        try:
            if self.service == 'PagerDuty':
                headers = {
                    'Authorization': 'Token token={0}'.format(self.key),
                    'Content-type': 'application/json',
                }
                req = requests.get(
                                'https://{0}.pagerduty.com{1}'.format(self.subdomain, path),
                                headers=headers,
                                params=payload,
                )
                results = json.loads(req.text)
            elif self.service == 'Conductor':
                headers = {
                    'Content-type': 'application/vnd.elemental+xml;version=3.0.3',
                    'Accept': 'application/xml',
                }
                req = requests.get(
                    'http://{0}{1}'.format(address, path),
                    headers=headers,
                )
                results = json.loads(json.dumps(xmltodict.parse(req.text)))
            elif self.service == 'Delta':
                headers = {
                    'Content-type': 'application/vnd.elemental+xml;version=1.6.1.34713',
                    'Accept': 'application/xml',
                }
                req = requests.get(
                    'http://{0}:8080{1}'.format(address, path),
                    headers=headers,
                )
                results = json.loads(json.dumps(xmltodict.parse(req.text)))
            elif self.service == 'Live':
                headers = {
                    'Content-type': 'application/vnd.elemental+xml;version=2.8.1',
                    'Accept': 'application/xml',
                }
                req = requests.get(
                    'http://{0}{1}'.format(address, path),
                    headers=headers,
                )
                results = json.loads(json.dumps(xmltodict.parse(req.text)))    
            elif self.service == 'Envivio':
                headers = {
                    'Content-type': 'application/xml',
                    'Accept': 'application/xml',
                }
                req = requests.get(
                    'http://{0}:8080{1}'.format(address, path),
                    headers=headers,
                )
                results = json.loads(json.dumps(xmltodict.parse(req.text)))                  
            else:
                return None
            return [req.status_code, results]
        except requests.exceptions.ConnectionError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'ConnectionError:', e))
            return [404, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'ConnectionError:', e)]
        except AttributeError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e))
            return [500, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e)]
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return [500, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)]
        
    def post(self, payload):
        """
        .. py:method:: Connect.post(path, payload)
        
        Post a json string update to an API query
        
        :param payload: JSON formatted API parameters
        :type payload: str
        :return: Status code of request and the JSON formatted response from API
        :rtype: dict{'status_code','JSON string'}
        :exception ConnectionError: In case of network problem (e.g. DNS failure, refused connection, etc)
        :exception HTTPError: In the event of the rare invalid HTTP response
        :exception TooManyRedirects: If a request times out, a Timeout exception is raised. If a request exceeds the configured number of maximum redirections
        :exception Exception: General exception with logged results

        :Example:

        >>> import requests
        >>> import json
        >>> import datetime
        >>> from Connect import Connect
        >>> days = 1
        >>> path = '/api/v1/incidents'
        >>> payload = json.dumps({"service_key": 'br549', "incident_key": 'nonexist', "event_type": 'resolve', "description": 'doctest', "details": 'none',})
        >>> con = Connect('PagerDuty')
        >>> status = con.post(payload)
        >>> print status[0]
        400
        """
        try:
            if self.service == 'PagerDuty':
                headers = {
                    'Authorization': 'Token token={0}'.format(self.key),
                    'Content-type': 'application/json',
                }
                req = requests.post(
                                'https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                                headers=headers,
                                data=payload,
                )
                results = req.text
            elif self.service == 'Conductor':
                return None
            else:
                return None    
            return [req.status_code, results]
        except requests.exceptions.ConnectionError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'ConnectionError:', e))
            return [404, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'ConnectionError:', e)]
        except AttributeError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e))
            return [500, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e)]
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return [500, '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)]
        
if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results                