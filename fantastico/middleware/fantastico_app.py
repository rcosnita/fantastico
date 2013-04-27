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
.. py:module:: fantastico.middleware.fantastico_app
'''

from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator

class FantasticoApp(object):
    '''This class represents the wsgi application entry point. It is designed to wrap together all configured middlewares
    and to return an http response.'''

    class OldCallableApp(object):
        '''Class used to save __call__ method from a wsgi middleware. It is used before chaining it at startup.'''
        
        def __init__(self, callable_obj):
            self._callable_obj = callable_obj
            
        def __call__(self, environ, start_response):
            '''Take the same number of arguments as any other middleware __call__ method.'''
             
            return self._callable_obj(environ, start_response)
    
    def __init__(self, settings_facade=SettingsFacade):
        self._settings_facade = settings_facade()
        
        self._wrap_middlewares()
        
    def _wrap_middlewares(self):
        '''Method used to register all configured middlewares in the correct order.'''
        
        installed_middlewares = self._settings_facade.get("installed_middleware")
        
        curr_app_cls, curr_app_inst = FantasticoApp, FantasticoApp.OldCallableApp(self.__call__)
        
        for middleware_cls in reversed(installed_middlewares):            
            middleware = instantiator.instantiate_class(middleware_cls, [curr_app_inst])
                                    
            curr_app_cls.__call__ = lambda inst, environ, start_response: middleware(environ, start_response)
                                    
            curr_app_cls, curr_app_inst = middleware.__class__, FantasticoApp.OldCallableApp(middleware.__call__)
        
    def __call__(self, environ, start_response):
        '''This method is used to execute the application and all configured middlewares in the correct order.'''
        
        return None