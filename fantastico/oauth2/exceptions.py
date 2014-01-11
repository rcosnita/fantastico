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

class OAuth2InvalidTokenDescriptorError(OAuth2Error):
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

class OAuth2InvalidTokenTypeError(OAuth2Error):
    '''This class provides a concrete exception used to notify that a token has been sent to a token generator which does not
    support it or the token type is unknown.'''

    ERROR_CODE = 12020

    @property
    def token_type(self):
        '''This property returns the invalid token type.'''

        return self._token_type

    def __init__(self, token_type, msg):
        self._token_type = token_type

        super(OAuth2InvalidTokenTypeError, self).__init__(self.ERROR_CODE, msg)

class OAuth2TokenExpiredError(OAuth2Error):
    '''This class provides a concrete exception used to notify that a token is expired.'''

    ERROR_CODE = 12030

    def __init__(self, msg=None):
        super(OAuth2TokenExpiredError, self).__init__(self.ERROR_CODE, msg)

class OAuth2TokenEncryptionError(OAuth2Error):
    '''This class provides a concrete exception used to notify an error during encrypt / decrypt token operations.'''

    ERROR_CODE = 12040

    def __init__(self, msg):
        super(OAuth2TokenEncryptionError, self).__init__(self.ERROR_CODE, msg)

class OAuth2InvalidClientError(OAuth2Error):
    '''This class provides a concrete exception used to notify an invalid client (not found or revoked).'''

    ERROR_CODE = 12050

    def __init__(self, msg):
        super(OAuth2InvalidClientError, self).__init__(self.ERROR_CODE, msg)

class OAuth2InvalidScopesError(OAuth2Error):
    '''This class provides a concrete exception used to notify that a client is not allowed to use a request set of scopes.'''

    ERROR_CODE = 12060

    def __init__(self, msg):
        super(OAuth2InvalidScopesError, self).__init__(self.ERROR_CODE, msg)

class OAuth2MissingQueryParamError(OAuth2Error):
    '''This class provides a concrete exception used to notify a missing query parameter from an OAuth2 endpoint.'''

    ERROR_CODE = 12070

    @property
    def param_name(self):
        '''This property return the name of the query parameter which is missing.'''

        return self._param_name

    def __init__(self, param_name):
        self._param_name = param_name

        msg = "Query parameter %s is missing." % param_name

        super(OAuth2MissingQueryParamError, self).__init__(self.ERROR_CODE, msg)

class OAuth2UnsupportedGrantError(OAuth2Error):
    '''This class provides a concrete exception for notifying unsupport oauth2 grant type.'''

    ERROR_CODE = 12080

    @property
    def handler_type(self):
        '''This property holds the unsupported grant type name.'''

        return self._handler_type

    def __init__(self, handler_type):
        self._handler_type = handler_type

        msg = "Handler type %s is not supported" % handler_type

        super(OAuth2UnsupportedGrantError, self).__init__(self.ERROR_CODE, msg)

class OAuth2UnauthorizedError(OAuth2Error):
    '''This class provides a concrete exception for notifying unauthorized access to oauth2 protected resources.'''

    ERROR_CODE = 12100

    def __init__(self, msg):
        super(OAuth2UnauthorizedError, self).__init__(self.ERROR_CODE, msg, http_code=401)

class OAuth2AuthenticationError(OAuth2Error):
    '''This class provides a concrete exception used to notify a failed authentication attempt from an OAuth2 IDP.'''

    ERROR_CODE = 12200

    def __init__(self, msg, http_code=403):
        super(OAuth2AuthenticationError, self).__init__(self.ERROR_CODE, msg, http_code)
