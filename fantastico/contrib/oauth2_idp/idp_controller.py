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

from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import Controller, ControllerProvider
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.utils.dictionary_object import DictionaryObject
from webob.response import Response
import urllib
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory

@ControllerProvider()
class IdpController(BaseController):
    '''This class provides the controller for all routes / APIs provided by oauth2 default Fantastico Identity Provider.'''

    def __init__(self, settings_facade, passwords_hasher_cls=PasswordsHasherFactory,
                 generators_factory_cls=TokenGeneratorFactory):
        super(IdpController, self).__init__(settings_facade)

        self._idp_config = self._settings_facade.get("oauth2_idp")
        self._idp_client_id = self._idp_config["client_id"]
        self._login_tpl = self._idp_config["template"]
        self._passwords_hasher = passwords_hasher_cls().get_hasher(PasswordsHasherFactory.SHA512_SALT)
        # self._login_generator = generators_factory_cls().get_generator(TokenGeneratorFactory.LOGIN_TOKEN, self.)

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
    def authenticate(self, request, tokens_factory_cls=TokenGeneratorFactory):
        '''This method receives a request to authenticate a user. It validates the username and password against a list of
        registered users.'''

        username = request.params.get("username")
        password = request.params.get("password")
        return_url = request.params.get("return_url")

        user = self._validate_user(username, password, request.models.User)

        return_url = "%s#login_token=%s" % (return_url, "abcd")

        return request.redirect(return_url)

    def _validate_user(self, username, password, user_facade):
        '''This method validates the given username and password against the record found in database. If no user is found or
        password does not match an exception is raised.'''

        records = user_facade.get_records_paged(
                                            start_record=0, end_record=1,
                                            filter_expr=ModelFilter(user_facade.username, username, ModelFilter.EQ))

        user = records[0]

        hashed_password = self._passwords_hasher.hash_password(password, DictionaryObject({"salt": user.user_id}))

        return user
