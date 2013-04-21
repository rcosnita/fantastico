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

.. py:module:: fantastico.exceptions

This package contains all core fantastico exceptions that are raised by different methods. 
'''

class FantasticoError(Exception):
    '''.. image:: /images/core/exceptions.png
    
    **FantasticoError** is the base of all exceptions raised within fantastico framework. It describe common attributes that
    each concrete fantastico exception must provide. By default all fantastico exceptions inherit FantasticoError exception. 
    We do this because each raised unhandled FantasticoError is map to a specific exception response. This strategy guarantees
    that at no moment errors will cause fantastico framework wsgi container to crash.
    '''
    
class FantasticoClassNotFoundError(FantasticoError):
    '''This exception is raised whenever code tries to dynamically import and instantiate a class which can not be resolved.'''
    
class FantasticoSettingNotFoundError(FantasticoError):
    '''This exception is raised whenever code tries to obtain a setting that is not available in the current fantastico
    configuration.'''