#!/usr/bin/env python
import config
from pprint import pformat

class Alert:
    """
    .. py:class:: Alert
    
    A class library to provide access to PagerDuty generated alerts
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """
    def __init__(self, alertId, alertType, started_at, user, address = ''):
        """
        .. py:method:: Alert.__init__(alertId, alertType, started_at, user, address = '')

        Instantiate an instance of Alert

        :param alertId: The Alert generated id for this alert
        :type alertId: str
        :param alertType: The type of alert generated
        :type alertType: str
        :param started_at: The start date/time of the alert
        :type started_at: date/time
        :param user: The user account the alert was forwarded too
        :type user: obj
        :param address: The destination of the alert
        :type address: str
        :return: Instance of Alert
        :rtype: obj
        :exception Exception: General exception with logged results

        :Example:
        
        >>> from User import User
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> alert = Alert('PWL7QXS', 'Email', '2013-03-06T15:28:50-05:00', u, 'dwomack@encompass.tv')
        >>> print repr(alert)
        Alert('PWL7QXS', 'Email', '2013-03-06T15:28:50-05:00', 'User: { 'avatar_url': 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG',
          'color': 'blue',
          'email': 'jsmo@heehaw.com',
          'invitation_sent': 'true',
          'name': 'Joe Smo',
          'role': 'user',
          'time_zone': 'Eastern Time (US & Canada)',
          'user_url': '/users/BR549',
          'userid': 'BR549'}', 'dwomack@encompass.tv')
        """
        try:
            self.alertId = alertId
            self.alertType = alertType
            self.started_at = started_at
            self.address = address
            self.user = user
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            
    def __getitem__(self, key):
        """
        .. py:method:: Alert.__getitem__(key)
    
        Returns the value of an instance attribute
    
        :param key: The attribute name to retrieve
        :type key: str
        :return: The attribute's value
        :rtype: str
        :exception AttributeError: If the attribute name provided does not exists
        :exception Exception: General exception with logged results

        :Example:
        
        >>> from User import User
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> alert = Alert('PWL7QXS', 'Email', '2013-03-06T15:28:50-05:00', u, 'dwomack@encompass.tv')
        >>> print alert['address']
        dwomack@encompass.tv
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
        .. py:method:: Alert.__setitem__(key, value)
    
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
        
        >>> from User import User
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> alert = Alert('PWL7QXS', 'Email', '2013-03-06T15:28:50-05:00', u, 'dwomack@encompass.tv')
        >>> alert.__setitem__('address', 'jbob@encompass.tv')
        'jbob@encompass.tv'
        >>> print repr(alert)        
        Alert('PWL7QXS', 'Email', '2013-03-06T15:28:50-05:00', 'User: { 'avatar_url': 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG',
          'color': 'blue',
          'email': 'jsmo@heehaw.com',
          'invitation_sent': 'true',
          'name': 'Joe Smo',
          'role': 'user',
          'time_zone': 'Eastern Time (US & Canada)',
          'user_url': '/users/BR549',
          'userid': 'BR549'}', 'jbob@encompass.tv')
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
        .. py:method:: Alert.__str__()

        Return a readable string representation of an instance

        :return: String representation of Alert instance
        :rtype: str
        
        >>> from User import User
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> alert = Alert('PWL7QXS', 'Email', '2013-03-06T15:28:50-05:00', u, 'dwomack@encompass.tv')
        >>> print alert
        Alert: { 'address': 'dwomack@encompass.tv',
          'alertId': 'PWL7QXS',
          'alertType': 'Email',
          'started_at': '2013-03-06T15:28:50-05:00',
          'user': User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')}
        """
        return 'Alert: {0}'.format(pformat(vars(self), indent=2, width=80, depth=2))

    def __repr__(self):
        """
        .. py:method:: Alert.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> from User import User
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> alert = Alert('PWL7QXS', 'Email', '2013-03-06T15:28:50-05:00', u, 'dwomack@encompass.tv')
        >>> print repr(alert)
        Alert('PWL7QXS', 'Email', '2013-03-06T15:28:50-05:00', 'User: { 'avatar_url': 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG',
          'color': 'blue',
          'email': 'jsmo@heehaw.com',
          'invitation_sent': 'true',
          'name': 'Joe Smo',
          'role': 'user',
          'time_zone': 'Eastern Time (US & Canada)',
          'user_url': '/users/BR549',
          'userid': 'BR549'}', 'dwomack@encompass.tv')
        """
        return 'Alert(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')'.format(self.alertId, 
                                                                           self.alertType, 
                                                                           self.started_at, 
                                                                           self.user, 
                                                                           self.address)

if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results    