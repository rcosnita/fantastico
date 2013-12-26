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
.. py:module:: fantastico.oauth2.exceptions
'''
from fantastico.exceptions import FantasticoError

class OAuth2Error(FantasticoError):
    '''This class provides the base class for OAuth2 exceptions. In order to be compliant with
    `OAuth2 spec <http://tools.ietf.org/html/rfc6749>`_ each oauth error is described by a status code, an error code and a
    friendly description.'''

    ERROR_CODE = 12000 # generic oauth2 error code

    @property
    def error_code(self):
        '''This property returns the exception error code.'''

        return self._error_code

    def __init__(self, error_code=ERROR_CODE, msg=None, http_code=400):
        super(OAuth2Error, self).__init__(msg, http_code)

        self._error_code = error_code

class OAuth2InvalidTokenDescriptorError(FantasticoError):
    '''This class provides a concrete exception used to notify a missing attribute from a token descriptor.'''

    ERROR_CODE = 12010

    @property
    def attr_name(self):
        '''This property returns the missing attribute name.'''

        return self._attr_name

    def __init__(self, attr_name):
        self._attr_name = attr_name

        msg = "Token descriptor misses attribute %s." % attr_name

        super(OAuth2InvalidTokenDescriptorError, self).__init__(self.ERROR_CODE, msg)
