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
.. py:module:: fantastico.oauth2.oauth2_controller
'''
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import ControllerProvider, Controller
from fantastico.oauth2.grant_handler_factory import GrantHandlerFactory
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError, OAuth2UnsupportedGrantError

@ControllerProvider()
class OAuth2Controller(BaseController):
    '''This class provides the routes specified in OAUTH 2 specification (`RFC6479 <http://tools.ietf.org/html/rfc6749>`_). A
    technical overview of OAuth2 implementation in Fantastico is presented below:

    .. image:: /images/oauth2/oauth2_overview.png
    '''

    def __init__(self, settings_facade, handler_factory_cls=GrantHandlerFactory):
        super(OAuth2Controller, self).__init__(settings_facade)

        self._handler_factory = handler_factory_cls()

    @Controller(url="^/oauth/authorize$",
                models={"Client": "fantastico.oauth2.models.clients.Client"})
    def handle_authorize(self, request):
        '''This method provides the /authorize endpoint compliant with `RFC6479 <http://tools.ietf.org/html/rfc6749>`_ standard.
        Authorize endpoint provides an API for obtaining an access token or an authorization code depending on the grant type.'''

        db_conn = request.models.Client.session
        grant_type = self._validate_param(request, "response_type")

        grant_handler = self._handler_factory.get_handler(grant_type, db_conn)

        return grant_handler.handle_grant(request)

    def handle_token(self, request):
        '''This method provides the /token endpoint compliant with `RFC6479 <http://tools.ietf.org/html/rfc6749>`_.
        Token endpoint provides an API for obtaining access tokens.'''

        grant_type = request.params.get("grant_type", "refresh_token")

        raise OAuth2UnsupportedGrantError(grant_type)

    def _validate_param(self, request, param_name):
        '''This method tries to obtain param_name from the given request. If the parameter is not found an oauth2 exception is
        raised.'''

        value = request.params.get(param_name)
        if not value:
            raise OAuth2MissingQueryParamError(param_name)

        return value
