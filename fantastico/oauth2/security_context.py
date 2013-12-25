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

        pass

    @property
    def login_token(self):
        '''This property returns the current login token passed to the current http request. Login token is already decoded
        as documented in :doc:`/features/oauth2/tokens_format` (encrypted section).'''

    def __init__(self):
        pass
