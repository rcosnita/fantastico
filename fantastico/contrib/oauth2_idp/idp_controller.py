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
.. py:module:: fantastico.contrib.oauth2_idp.idp_controller
'''

from fantastico.contrib.oauth2_idp.models.user_repository import UserRepository
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import Controller, ControllerProvider
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.mvc.models.model_filter_compound import ModelFilterAnd
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError, OAuth2AuthenticationError, OAuth2Error
from fantastico.oauth2.models.return_urls import ClientReturnUrl
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
from fantastico.oauth2.tokens_service import TokensService
from fantastico.utils.dictionary_object import DictionaryObject
from webob.response import Response
import urllib

@ControllerProvider()
class IdpController(BaseController):
    '''This class provides the controller for all routes / APIs provided by oauth2 default Fantastico Identity Provider.'''

    REDIRECT_PARAM = "redirect_uri"

    def __init__(self, settings_facade, passwords_hasher_cls=PasswordsHasherFactory):
        super(IdpController, self).__init__(settings_facade)

        self._idp_config = self._settings_facade.get("oauth2_idp")
        self._idp_client_id = self._idp_config["client_id"]
        self._idp_expires_in = self._idp_config["expires_in"]
        self._login_tpl = self._idp_config["template"]
        self._passwords_hasher = passwords_hasher_cls().get_hasher(PasswordsHasherFactory.SHA512_SALT)

    @Controller(url="^/oauth/idp/ui/login$")
    def show_login(self, request):
        '''This method returns the login page for Fantastico.'''

        return_url = request.params.get(self.REDIRECT_PARAM)

        if not return_url or len(return_url.strip()) == 0:
            raise OAuth2MissingQueryParamError(self.REDIRECT_PARAM)

        content = self.load_template(self._login_tpl,
                                     {self.REDIRECT_PARAM: urllib.parse.quote(return_url)},
                                     enable_global_folder=True)

        return Response(content)

    @Controller(url="^/oauth/idp/ui/cb$") # pylint: disable=W0613
    def show_oauth_idpcallback(self, request):
        '''This method loads the idp callback page which contains the client side code for extracting the current generated
        token.'''

        content = self.load_template("authorize_cb.html")

        return Response(content)

    @Controller(url="^/oauth/idp/login$", method="POST",
                models={"ClientReturnUrl": "fantastico.oauth2.models.return_urls.ClientReturnUrl"})
    def authenticate(self, request, tokens_service_cls=TokensService, user_repo_cls=UserRepository):
        '''This method receives a request to authenticate a user. It validates the username and password against a list of
        registered users.'''

        username = self._validate_missing_param(request, "username")
        password = self._validate_missing_param(request, "password")
        return_url = self._validate_missing_param(request, self.REDIRECT_PARAM)

        clienturls_facade = request.models.ClientReturnUrl
        self._validate_return_url(clienturls_facade, return_url)

        db_conn = clienturls_facade.session

        try:
            user_repo = user_repo_cls(db_conn)
            user = self._validate_user(username, password, user_repo)

            tokens_service = tokens_service_cls(db_conn)
            token = self._generate_token(user.user_id, tokens_service)

            encrypted_str = tokens_service.encrypt(token, token.client_id)

            if return_url.find("?") == -1:
                return_url += "?login_token=%s" % encrypted_str
            else:
                return_url += "&login_token=%s" % encrypted_str

            return request.redirect(return_url)
        except OAuth2Error:
            raise
        except Exception as ex:
            raise OAuth2AuthenticationError("Unexpected error occured: %s" % str(ex))

    def _validate_return_url(self, clienturls_facade, return_url):
        '''This test case checks the existence of return url in the list of supported return urls for idp.'''

        qmark_pos = return_url.find("?")

        if qmark_pos > -1:
            return_url = return_url[:qmark_pos]

        client_urls = clienturls_facade.get_records_paged(
                                    start_record=0, end_record=1,
                                    filter_expr=ModelFilterAnd(
                                                    ModelFilter(ClientReturnUrl.client_id, self._idp_client_id, ModelFilter.EQ),
                                                    ModelFilter(ClientReturnUrl.return_url, return_url, ModelFilter.EQ)))

        if len(client_urls) != 1:
            raise OAuth2MissingQueryParamError(self.REDIRECT_PARAM)

    def _validate_user(self, username, password, user_repo):
        '''This method validates the given username and password against the record found in database. If no user is found or
        password does not match an exception is raised.'''

        user = user_repo.load_by_username(username)
        if not user:
            raise OAuth2AuthenticationError("Username or password do not match.")

        password_hash = self._passwords_hasher.hash_password(password, DictionaryObject({"salt": user.user_id}))

        if password_hash != user.password:
            # when the account is created for the first time there is no user_id available so a default salt is used.
            password_hash_default = self._passwords_hasher.hash_password(password)

            if password_hash_default != user.password:
                raise OAuth2AuthenticationError("Username or password do not match.")

        return user

    def _generate_token(self, user_id, tokens_service):
        '''This method generates a login token using the given user_id and tokens_service.'''

        token_desc = {"client_id": self._idp_client_id,
                      "user_id": user_id,
                      "expires_in": self._idp_expires_in}

        return tokens_service.generate(token_desc, TokenGeneratorFactory.LOGIN_TOKEN)

    def _validate_missing_param(self, request, param_name):
        '''This method ensures a param is found into the given request. If it is not found a concrete exception is raised.'''

        param = request.params.get(param_name)

        if not param:
            raise OAuth2MissingQueryParamError(param_name)

        return param
