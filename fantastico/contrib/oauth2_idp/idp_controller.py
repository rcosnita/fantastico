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
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
from fantastico.oauth2.tokens_service import TokensService
from fantastico.utils.dictionary_object import DictionaryObject
from webob.response import Response
import urllib

@ControllerProvider()
class IdpController(BaseController):
    '''This class provides the controller for all routes / APIs provided by oauth2 default Fantastico Identity Provider.'''

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

        return_url = request.params.get("return_url")

        if not return_url or len(return_url.strip()) == 0:
            raise OAuth2MissingQueryParamError("return_url")

        content = self.load_template(self._login_tpl,
                                     {"return_url": urllib.parse.quote(return_url)})

        return Response(content)

    @Controller(url="^/oauth/idp/login$", method="POST",
                models={"User": "fantastico.contrib.oauth2_idp.models.users.User"})
    def authenticate(self, request, tokens_service_cls=TokensService, user_repo_cls=UserRepository):
        '''This method receives a request to authenticate a user. It validates the username and password against a list of
        registered users.'''

        username = request.params.get("username")
        password = request.params.get("password")
        return_url = request.params.get("return_url")

        db_conn = request.models.User.session

        user_repo = user_repo_cls(db_conn)
        user = self._validate_user(username, password, user_repo)

        tokens_service = tokens_service_cls(db_conn)
        token = self._generate_token(user.user_id, tokens_service)

        encrypted_str = tokens_service.encrypt(token, token.client_id)
        return_url += "?login_token=%s" % encrypted_str

        return request.redirect(return_url)

    def _validate_user(self, username, password, user_repo):
        '''This method validates the given username and password against the record found in database. If no user is found or
        password does not match an exception is raised.'''

        user = user_repo.load_by_username(username)

        password_hash = self._passwords_hasher.hash_password(password, DictionaryObject({"salt": user.user_id}))

        if password_hash != user.password:
            raise Exception("Invalid user.")

        return user

    def _generate_token(self, user_id, tokens_service):
        '''This method generates a login token using the given user_id and tokens_service.'''

        token_desc = {"client_id": self._idp_client_id,
                      "user_id": user_id,
                      "expires_in": self._idp_expires_in}

        return tokens_service.generate(token_desc, TokenGeneratorFactory.LOGIN_TOKEN)
