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
.. py:module:: fantastico.oauth2.security_context
'''

class SecurityContext(object):
    '''This class provides the OAuth2 security context. Security context is available for each request and can be accessed
    using the following code snippet:

    .. code-block:: python

       @Controller(url="/test/controller")
       def handle_request(self, request):
           security_ctx = request.context.security

           # do something with security context
    '''

    @property
    def access_token(self):
        '''This property returns the current access token passed to the current http request. Access token is already decoded
        as documented in :doc:`/features/oauth2/tokens_format` (encrypted section).'''

        return self._access_token

    @property
    def required_scopes(self):
        '''This property returns the current required scopes for http request. Required scopes are only available at runtime.'''

        return self._required_scopes

    def __init__(self, access_token, required_scopes=None):
        self._access_token = access_token
        self._required_scopes = required_scopes

        self._access_token_scopes = {}
        if self._access_token:
            self._access_token_scopes = {scope: True for scope in self._access_token.scopes}

    def validate_context(self, attr_scope="scopes"):
        '''This method tries to validate the current security context using the current access token and required scopes.
        Internally, the method simply ensures required scopes are present in access token granted scopes. Moreover, it receives
        an optional parameter which allows requester to decide what section of required scopes it wants to validates. Valid
        values are: scopes, create_scopes, read_scopes, update_scopes or delete_scopes.'''

        if not self._required_scopes:
            return True

        if attr_scope != "scopes":
            attr_scope = "%s_scopes" % attr_scope

        required_scopes = getattr(self._required_scopes, attr_scope)

        for scope in required_scopes:
            if not self._access_token_scopes.get(scope):
                return False

        return True
