#!/usr/bin/env python
import config
from pprint import pformat

class Incident:
    """
    .. py:class:: Incident

    A class library to provide PagerDuty Inicident datatype

    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """  
    def __init__(self, incident_number, status, urgency, created_on, html_url, incident_key, service, escalation_policy, last_status_change_by, last_status_change_on, trigger_summary_data, trigger_details_html_url, pending_actions = [], assigned_to = []):
        """
        .. py:method:: Incident.__init__(incident_number, status, urgency, created_on, html_url, incident_key, service, escalation_policy, last_status_change_by, last_status_change_on, trigger_summary_data, trigger_details_html_url, pending_actions = [], assigned_to = [])

        Instantiate an instance of Incident

        :param incident_number: The number of the incident. This is unique across your account
        :type incident_number: int
        :param status: The current status of the incident. Valid statuses are: (triggered, acknowledged, resolved)
        :type status: str
        :param urgency:  current urgency of the incident. Valid urgencies are: (high, low)
        :type urgency: str
        :param created_on: The date/time the incident was triggered
        :type created_on: date/time
        :param html_url: The PagerDuty website URL where the incident can be viewed and further actions taken. This is not the resource URL
        :type html_url: str
        :param incident_key: The incident's de-duplication key. See the PagerDuty Integration API docs for further details
        :type incident_key: str
        :param service: The PagerDuty service that the incident belongs to. The service will contain fields of its own
        :type service: obj
        :param escalation_policy: The escalation policy that the incident belongs to. The policy will contain fields of its own
        :type escalation_policy: obj
        :param last_status_change_by: The user who is responsible for the incident's last status change
        :type last_status_change_by: obj
        :param last_status_change_on: The date/time the incident's status last changed
        :type last_status_change_on: date/time
        :param trigger_summary_data: Some condensed information regarding the initial event that triggered this incident
        :type trigger_summary_data: obj
        :param trigger_details_html_url: The PagerDuty website URL where the full details regarding the initial event that triggered this incident can be found. (This is not the resource URL.)
        :type trigger_details_html_url: str
        :param assigned_to: The list of assignments of the incident
        :type assigned_to: arr
        :param pending_actions: The list of pending_actions on the incident
        :type pending_actions: arr
        :return: Instance of User
        :rtype: obj
        
        .. Todo:: Incorporate service, escalation_policy, last_status_changed_by, triggered_summary_data object data and assigned_to, pending_actions array data
        
        :Example:
        
        >>> inc = Incident(64, 'resolved', 'low', '2016-02-28T10:02:41Z', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP', 'Port-Channel22 (DMC-leaf1) Down', 'service', 'esclation_policy', '', '2016-02-28T10:04:37Z', 'trigger_summary_data', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP/log_entries/Q201PYPWVMT7BA', pending_actions = [], assigned_to = [])
        >>> eval(repr(inc))
        Incident('64', 'resolved', 'low', '2016-02-28T10:02:41Z', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP', 'Port-Channel22 (DMC-leaf1) Down', 'service', 'esclation_policy', '', '2016-02-28T10:04:37Z', 'trigger_summary_data', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP/log_entries/Q201PYPWVMT7BA', '[]', '[]')
        """
        try:
            self.incident_number = incident_number
            self.status = status
            self.urgency = urgency
            self.created_on = created_on
            self.html_url = html_url
            self.incident_key = incident_key
            self.service = service
            self.escalation_policy = escalation_policy
            self.last_status_change_by = last_status_change_by
            self.last_status_change_on = last_status_change_on
            self.trigger_summary_data = trigger_summary_data
            self.trigger_details_html_url = trigger_details_html_url
            self.pending_actions = pending_actions
            self.assigned_to = assigned_to
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            
    def __getitem__(self, key):
        """
        .. py:method:: Incident.__getitem__(key)
    
        Returns the value of an instance attribute
    
        :param key: The attribute name to retrieve
        :type key: str
        :return: The attribute's value
        :rtype: str
        :exception AttributeError: If the attribute name provided does not exists
        
        :Example:
        
        >>> inc = Incident(64, 'resolved', 'low', '2016-02-28T10:02:41Z', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP', 'Port-Channel22 (DMC-leaf1) Down', 'service', 'esclation_policy', '', '2016-02-28T10:04:37Z', 'trigger_summary_data', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP/log_entries/Q201PYPWVMT7BA', pending_actions = [], assigned_to = [])
        >>> print inc['status']
        resolved
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
        .. py:method:: Incident.__setitem__(key, value)
    
        Sets the value of an instance attribute
    
        :param key: The attribute name to set
        :type key: str
        :param value: The value to assign to the attribute
        :type value: str
        :return: The attribute's new value
        :rtype: str
        :exception AttributeError: If the attribute name provided does not exists
        
        :Example:
        
        >>> inc = Incident(64, 'resolved', 'low', '2016-02-28T10:02:41Z', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP', 'Port-Channel22 (DMC-leaf1) Down', 'service', 'esclation_policy', '', '2016-02-28T10:04:37Z', 'trigger_summary_data', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP/log_entries/Q201PYPWVMT7BA', pending_actions = [], assigned_to = [])
        >>> inc.__setitem__('status', 'triggered')
        'triggered'
        >>> print inc['status']
        triggered
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
        .. py:method:: Incident.__str__()

        Return a readable string representation of an instance

        :return: String representation of Incident instance
        :rtype: str
        
        :Example:
        
        >>> inc = Incident(64, 'resolved', 'low', '2016-02-28T10:02:41Z', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP', 'Port-Channel22 (DMC-leaf1) Down', 'service', 'esclation_policy', '', '2016-02-28T10:04:37Z', 'trigger_summary_data', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP/log_entries/Q201PYPWVMT7BA', pending_actions = [], assigned_to = [])
        >>> print inc
        Incident: { 'assigned_to': [],
          'created_on': '2016-02-28T10:02:41Z',
          'escalation_policy': 'esclation_policy',
          'html_url': 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP',
          'incident_key': 'Port-Channel22 (DMC-leaf1) Down',
          'incident_number': 64,
          'last_status_change_by': '',
          'last_status_change_on': '2016-02-28T10:04:37Z',
          'pending_actions': [],
          'service': 'service',
          'status': 'resolved',
          'trigger_details_html_url': 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP/log_entries/Q201PYPWVMT7BA',
          'trigger_summary_data': 'trigger_summary_data',
          'urgency': 'low'}
          """
        return 'Incident: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: Incident.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str

        :Example:
        
        >>> inc = Incident(64, 'resolved', 'low', '2016-02-28T10:02:41Z', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP', 'Port-Channel22 (DMC-leaf1) Down', 'service', 'esclation_policy', '', '2016-02-28T10:04:37Z', 'trigger_summary_data', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP/log_entries/Q201PYPWVMT7BA', pending_actions = [], assigned_to = [])
        >>> print repr(inc)
        Incident('64', 'resolved', 'low', '2016-02-28T10:02:41Z', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP', 'Port-Channel22 (DMC-leaf1) Down', 'service', 'esclation_policy', '', '2016-02-28T10:04:37Z', 'trigger_summary_data', 'https://encompass-digital-media.pagerduty.com/incidents/PK35GXP/log_entries/Q201PYPWVMT7BA', '[]', '[]')
        """
        return 'Incident(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\', \'{10}\', \'{11}\', \'{12}\', \'{13}\')'.format(self.incident_number, self.status, 
                                                                                                                                                                   self.urgency, self.created_on, self.html_url, 
                                                                                                                                                                   self.incident_key, self.service, 
                                                                                                                                                                   self.escalation_policy, 
                                                                                                                                                                   self.last_status_change_by, self.last_status_change_on, 
                                                                                                                                                                   self.trigger_summary_data, self.trigger_details_html_url, 
                                                                                                                                                                   self.pending_actions, self.assigned_to)

if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results            