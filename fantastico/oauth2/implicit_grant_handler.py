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
.. py:module:: fantastico.oauth2.implicit_grant_handler
'''
from fantastico.oauth2.grant_handler import GrantHandler
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
from fantastico.routing_engine.custom_responses import RedirectResponse

class ImplicitGrantHandler(GrantHandler):
    '''This class provides the implementation for implicit grant type described in
    `RFC6749 <http://tools.ietf.org/html/rfc6749>`_. Implementation of this grant type is fully compliant with OAuth2 spec.'''

    def __init__(self, tokens_service, settings_facade):
        super(ImplicitGrantHandler, self).__init__(tokens_service, settings_facade)

        self._expires_in = self._settings_facade.get("access_token_validity")

    def handle_grant(self, request):
        '''This method provides the algorithm for implementing implicit grant type handler. Internally it will use TokensService
        in order to generate a new access token.'''

        client_id = self._validate_missing_param(request, "client_id")
        redirect_uri = self._validate_missing_param(request, "redirect_uri")
        state = self._validate_missing_param(request, "state")

        error_redirect = self._get_error_redirect(request, redirect_uri, state)
        if error_redirect:
            return error_redirect

        scopes = self._validate_missing_param(request, "scope")

        encrypted_login = self._validate_missing_param(request, "login_token")

        login_token = self._tokens_service.decrypt(encrypted_login)

        self._tokens_service.validate(login_token)

        access_token = self._tokens_service.generate({"client_id": client_id,
                                                      "user_id": login_token.user_id,
                                                      "scopes": scopes,
                                                      "expires_in": self._expires_in}, TokenGeneratorFactory.ACCESS_TOKEN)

        encrypted_access = self._tokens_service.encrypt(access_token, client_id)

        prefix_sign = "#"
        if redirect_uri.find("#") > -1:
            prefix_sign = "&"

        return_url = "%s%saccess_token=%s&state=%s&token_type=%s&expires_in=%s" % \
                        (redirect_uri, prefix_sign, encrypted_access, state, access_token.type, self._expires_in)

        return RedirectResponse(return_url)

    def _get_error_redirect(self, request, redirect_uri, state):
        '''This method builds an error redirect response if the request has query parameters indicating error case.'''

        error = request.params.get("error")

        if not error:
            return

        error_description = request.params.get("error_description", "")
        error_uri = request.params.get("error_uri")

        redirect_uri = "%s#error=%s&error_description=%s&error_uri=%s&state=%s" % \
                                (redirect_uri, error, error_description, error_uri, state)

        return RedirectResponse(redirect_uri)
