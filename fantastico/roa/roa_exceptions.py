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
.. py:module:: fantastico.roa.exceptions
'''
from fantastico.exceptions import FantasticoError

class FantasticoRoaError(FantasticoError):
    '''This class provides the core error used within Fantastico ROA layer. Usually, more concrete exceptions are raised by
    ROA layers.'''

    def __init__(self, msg, http_code=400):
        super(FantasticoRoaError, self).__init__(msg, http_code=http_code)

class FantasticoRoaDuplicateError(FantasticoRoaError):
    '''This concrete exception is used to notify user that multiple resources with same name and version or url and version
    can not be registered multiple times.'''

class FantasticoRoaMethodNotSupportedError(FantasticoRoaError):
    '''This concrete exception is used to notify user that the current http method requested is not supported on the given
    resource.'''

    def __init__(self, msg):
        super(FantasticoRoaMethodNotSupportedError, self).__init__(msg, http_code=405)
