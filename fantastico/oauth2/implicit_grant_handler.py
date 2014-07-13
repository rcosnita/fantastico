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
from fantastico.exception_formatters import ExceptionFormattersFactory
from fantastico.oauth2.grant_handler import GrantHandler
from fantastico.oauth2.models.client_repository import ClientRepository
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
from fantastico.routing_engine.custom_responses import RedirectResponse
from webob.response import Response
import urllib

class ImplicitGrantHandler(GrantHandler):
    '''This class provides the implementation for implicit grant type described in
    `RFC6749 <http://tools.ietf.org/html/rfc6749>`_. Implementation of this grant type is fully compliant with 
    OAuth2 spec. In addition to RFC6749, the implicit grant implemented in fantastico supports an additional
    query parameter named **redirect** which is optional. If redirect query parameter is specified with value
    0 then a 200 OK response is returned to the client in comparison with redirect 1 value where 302 Found response
    is returned. We do this in order to support more advanced use cases where user can orchestrate the redirects
    rather than browser.'''

    def __init__(self, tokens_service, settings_facade, exception_formatters_cls=ExceptionFormattersFactory,
                 client_repo_cls=ClientRepository):
        super(ImplicitGrantHandler, self).__init__(tokens_service, settings_facade)

        self._expires_in = self._settings_facade.get("access_token_validity")
        self._idp_url = self._settings_facade.get("oauth2_idp")["idp_index"]
        self._exception_formatter = exception_formatters_cls().get_formatter(ExceptionFormattersFactory.HASH)
        self._client_repo = client_repo_cls(tokens_service.db_conn)

    def handle_grant(self, request):
        '''This method provides the algorithm for implementing implicit grant type handler. Internally it will use TokensService
        in order to generate a new access token. In addition, if redirect query parameter is set to false then a 200 OK response
        with Location header and no body is sent to the client.'''

        client_id = self._validate_missing_param(request, "client_id")
        redirect_uri = self._validate_missing_param(request, "redirect_uri")
        state = self._validate_missing_param(request, "state")

        error_redirect = self._get_error_redirect(request, redirect_uri, state)
        if error_redirect:
            return error_redirect

        scopes = self._validate_missing_param(request, "scope")

        invalid_redirect = self._validate_redirect_uri(redirect_uri)
        if invalid_redirect:
            return invalid_redirect

        encrypted_login = request.params.get("login_token")
        if not encrypted_login:
            return self._redirect_to_idp(request)

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

        return_url = "%s%saccess_token=%s&state=%s&token_type=%s&expires_in=%s&scope=%s" % \
                        (redirect_uri, prefix_sign, encrypted_access, urllib.parse.quote(state),
                         access_token.type, self._expires_in,
                         urllib.parse.quote(scopes))
        
        is_redirect = int(request.params.get("redirect") or 1)
        if is_redirect == 1:            
            return RedirectResponse(return_url)
        
        response = Response(body=b"")
        response.headers["Location"] = return_url
        
        return response

    def _get_error_redirect(self, request, redirect_uri, state):
        '''This method builds an error redirect response if the request has query parameters indicating error case.'''

        error = request.params.get("error")

        if not error:
            return

        error_description = request.params.get("error_description", "")
        error_uri = request.params.get("error_uri")

        redirect_uri = self._exception_formatter.format_ex({"error": error,
                                                            "error_description": error_description,
                                                            "error_uri": error_uri,
                                                            "state": state},
                                                           ctx={"redirect_uri": redirect_uri})

        return RedirectResponse(redirect_uri)

    def _redirect_to_idp(self, request):
        '''This method redirects the current request to identity provider (login not proven).'''

        request_url = request.url.replace(request.host_url, "")

        redirect_url = "%s?redirect_uri=%s" % (self._idp_url, urllib.parse.quote(request_url))

        return request.redirect(redirect_url)

    def _validate_redirect_uri(self, redirect_uri):
        '''This method ensures the given redirect uri is valid for specified client. If this is not the case a 401 response
        object is returned.'''

        client = self._client_repo.load_client_by_returnurl(redirect_uri)

        if client:
            return None

        msg = "%s redirect_uri is not supported by any registered client." % redirect_uri

        return Response(body=msg.encode(), status_code=401)
