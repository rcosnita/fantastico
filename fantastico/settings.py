'''
Copyright 2013 Cosnita Radu Viorel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. codeauthor:: Radu Viorel Cosnita <radu.cosnita@gmail.com>

.. py:module:: fantastico.settings
'''

import os
from fantastico.utils import instantiator
from fantastico.exceptions import FantasticoSettingNotFoundError

class BasicSettings(object):
    '''This is the core class that describes all available settings of fantastico framework. For convenience all options
    have default values that ensure minimum functionality of the framework. Below you can find an example of three possible 
    configuration: Dev / Stage / Production.
    
    .. image:: /images/core/settings.png
    
    As you can see, if you want to overwrite basic configuration you simply have to extend the class and set new values
    for the attributes you want to overwrite.
    '''
        
    @property
    def installed_middleware(self):
        '''Property that holds all installed middlewares.'''
        
        return ["fantastico.middleware.request_middleware.RequestMiddleware",
                "fantastico.middleware.routing_engine.RoutingEngineMiddleware"]
    
    @property
    def supported_languages(self):
        '''Property that holds all supported languages by this fantastico instance.''' 
        
        return ["en_us"]
        
class SettingsFacade(object):
    '''For using a specific fantastico configuration you need to do two simple steps:

    * Set **FANTASTICO_ACTIVE_CONFIG** to the fully python qualified class name you want to use. E.g: :py:class:`fantastico.settings.BasicSettings`
    * In your code, you can use the following snippet to access a specific setting:
      
      .. code-block:: python
      
         from fantastico.settings import SettingsFacade
         
         print(SettingsFacade().get("installed_middleware"))
                 
    If no active configuration is set in the :py:class:`fantastico.settings.BasicSettings` will be used.'''
    
    __ENV_ACTIVE_CONFIG = "FANTASTICO_ACTIVE_CONFIG"
    
    def __init__(self, environ=None):
        self._environ = environ
        
        if self._environ is None:
            self._environ = os.environ
            
        self._cached_config = None
        
    def get(self, name):
        '''Method used to retrieve a setting value.
        
        :param name: Setting name.
        :param type: string
        :returns: The setting value.
        :rtype: object'''
                
        try:
            self._cached_config = self._cached_config or self.get_config()
            
            return getattr(self._cached_config, name)
        except AttributeError as ex:
            raise FantasticoSettingNotFoundError("Attribute %s could not be obtained: %s" % (name, str(ex)))
        except Exception as ex:
            raise FantasticoSettingNotFoundError("Exception thrown for attribute %s : %s" % (name, str(ex)))
    
    def get_config(self):
        '''Method used to return the active configuration which is used by this facade.
        
        :rtype: :py:class:`fantastico.settings.BasicSettings`
        :returns: Active configuration currently used.'''
        
        active_config = self._environ.get(self.__ENV_ACTIVE_CONFIG) or "fantastico.settings.BasicSettings"
        
        return instantiator.instantiate_class(active_config)