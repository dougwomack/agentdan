#!/usr/bin/env python
import config
from pprint import pformat

class User:
    """
    .. py:class:: User
    
    A class library to create an instance of User supporting PagerDuty responses
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
	"""  
    def __init__(self, userid, name, email, time_zone, color, role, avatar_url, user_url, invitation_sent):
        """/
        .. py:method:: User.__init__(userid, name, email, time_zone, color, role, avatar_url, user_url, invitation_sent)
    
        Instantiate an instance of User
        
        :param userid: The PagerDuty generated id for this user
        :type userid: str
        :param name: The PagerDuty username
        :type name: str
        :param email: The user's email address
        :type email: str
        :param time_zone: The user's local timezone
        :type time_zone: str
        :param color: The user's color designation in PagerDuty
        :type color: str
        :param role: The user's assigned role
        :type role: str
        :param avatar_url: The path to the user's avatar
        :type avatar_url: str
        :param user_url: The path to the user's account
        :type user_url: str
        :param invitation_sent: Whether a user's invite has been sent after user creation
        :type invitation_sent: bool
        :return: Instance of User
        :rtype: obj
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> eval(repr(u))
        User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        """
        try:
            self.userid = userid
            self.name = name
            self.email = email
            self.time_zone = time_zone
            self.color = color
            self.role = role
            self.avatar_url = avatar_url
            self.user_url = user_url
            self.invitation_sent = invitation_sent
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            
    def __getitem__(self, key):
        """
        .. py:method:: User.__getitem__(key)
    
        Returns the value of an instance attribute
    
        :param key: The attribute name to retrieve
        :type key: str
        :return: The attribute's value
        :rtype: str
        :exception AttributeError: If the attribute name provided does not exists
        :exception Exception: General exception with logged results
        
        :Example:
        
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> print u['color']
        blue
        """
        try:
            return getattr(self, key) 
        except AttributeError as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'AttributeError:', e))
            return 'AttributeError: {0}'.format(e)
        except Exception as e:
            config.log.error('{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e))
            return '{0}:{1}:{2} {3}'.format(self.__class__, sys.exc_info()[-1].tb_lineno, 'Exception:', e)
        
    def __setitem__(self, key, value):
        """
        .. py:method:: User.__setitem__(key, value)
    
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
        
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> u.__setitem__('name', 'Joe Smart')
        'Joe Smart'
        >>> print repr(u)
        User('BR549', 'Joe Smart', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
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
        .. py:method:: User.__str__()

        Return a readable string representation of an instance

        :return: String representation of User instance
        :rtype: str
        
        :Example:
        
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> print u
        User: { 'avatar_url': 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG',
          'color': 'blue',
          'email': 'jsmo@heehaw.com',
          'invitation_sent': 'true',
          'name': 'Joe Smo',
          'role': 'user',
          'time_zone': 'Eastern Time (US & Canada)',
          'user_url': '/users/BR549',
          'userid': 'BR549'}
        """
        return 'User: {0}'.format(pformat(vars(self), indent=2, width=80, depth=1))

    def __repr__(self):
        """
        .. py:method:: User.__repr__()

        Return a string representation readable by the interpreter  

        :return: Interpreter usable string representation 
        :rtype: str
        
        :Example:
        
        >>> u = User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        >>> print repr(u)
        User('BR549', 'Joe Smo', 'jsmo@heehaw.com', 'Eastern Time (US & Canada)', 'blue', 'user', 'https://secure.gravatar.com/avatar/2e32280905f296791ed387cd0f61ec6b.png?d=mm&r=PG', '/users/BR549', 'true')
        """
        return 'User(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\')'.format(self.userid, 
                                                                                                              self.name, 
                                                                                                              self.email, 
                                                                                                              self.time_zone, 
                                                                                                              self.color, 
                                                                                                              self.role, 
                                                                                                              self.avatar_url, 
                                                                                                              self.user_url, 
                                                                                                              self.invitation_sent)
    
if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    print results
