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
.. py:module:: fantastico.contrib.oauth2_idp.tests.test_idp_controller
'''

from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.oauth2.token import Token
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
from fantastico.routing_engine.custom_responses import RedirectResponse
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils.dictionary_object import DictionaryObject
from mock import Mock
from sqlalchemy.schema import Column
from sqlalchemy.types import String
import urllib

class IdpControllerTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for oauth2 fantastico identity provider controller.'''

    _IDP_CLIENTID = "11111111-1111-1111-1111-111111111111"
    _TPL_LOGIN = "/mock/location/views/login.html"

    _idp_controller = None
    _hasher = None

    def init(self):
        '''This method is invoked automatically in order to setup dependencies common to all test cases.'''

        from fantastico.contrib.oauth2_idp.idp_controller import IdpController

        oauth2_idp = {"client_id": self._IDP_CLIENTID,
                      "template": self._TPL_LOGIN}

        self._hasher = Mock()
        self._hasher.get_hasher = Mock(return_value=self._hasher)
        hasher_cls = Mock(return_value=self._hasher)

        settings_facade = Mock()
        settings_facade.get = Mock(return_value=oauth2_idp)

        self._generators_factory = Mock()
        self._generators_factory.get_generator = Mock()

        self._idp_controller = IdpController(settings_facade, passwords_hasher_cls=hasher_cls)

        settings_facade.get.assert_called_once_with("oauth2_idp")
        hasher_cls.assert_called_once_with()
        self._hasher.get_hasher.assert_called_once_with(PasswordsHasherFactory.SHA512_SALT)

    def test_show_login_ok(self):
        '''This test case ensures login screen is displayed correctly when all required parameters are passed.'''

        request = Mock()
        request.params = {"return_url": "/simple/test"}

        self._idp_controller.load_template = Mock(return_value="cool result")

        response = self._idp_controller.show_login(request)

        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)

        self.assertIsNotNone(response.body)
        body = response.body.decode()

        self.assertEqual("cool result", body)

        self._idp_controller.load_template.assert_called_once_with(
                                        self._TPL_LOGIN,
                                        {"return_url": urllib.parse.quote(request.params["return_url"])})

    def test_show_login_missingreturn(self):
        '''This test case ensures login screen is not displayed if return_url query parameter is not provided.'''

        request = Mock()
        request.params = {}

        for return_url in [None, "", "    "]:
            request.params["return_url"] = return_url

            with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
                self._idp_controller.show_login(request)

            self.assertEqual("return_url", ctx.exception.param_name)

    def test_authenticate_ok(self):
        '''This test case ensures a correct login token is generated during authentication phase. It also checks for correct
        redirect response.'''

        user_id = 123
        username = "john.doe@email.com"
        password = "12345"
        return_url = "/test/url?abc=1"

        hashed_password = "hashed_password"
        self._hasher.hash_password = Mock(return_value=hashed_password)

        user = DictionaryObject({"user_id": user_id,
                                 "username": username,
                                 "password": hashed_password,
                                 "person_id": 5})

        user_facade = Mock()
        user_facade.session = Mock()
        user_facade.username = Column("username", String(100))

        request = Mock()
        request.params = {"username": username,
                          "password": password,
                          "return_url": return_url}
        request.models = Mock()
        request.models.User = user_facade

        request.redirect = lambda destination: RedirectResponse(destination)

        user_facade.get_records_paged = Mock(return_value=[user])

        login_generator = Mock()
        login_generator.generate = Mock(return_value=Token({}))

        tokens_factory = Mock()
        tokens_factory.get_generator = Mock(return_value=login_generator)
        tokens_factory_cls = Mock(return_value=tokens_factory)

        response = self._idp_controller.authenticate(request, tokens_factory_cls)

        self.assertIsNotNone(response)
        self.assertEqual(301, response.status_code)
        self.assertEqual("%s#login_token=abcd" % (return_url),
                         response.headers.get("Location"))

        user_facade.get_records_paged.assert_called_with(
                                            start_record=0, end_record=1,
                                            filter_expr=ModelFilter(user_facade.username, user.username, ModelFilter.EQ))
        self._hasher.hash_password.assert_called_once_with(password, DictionaryObject({"salt": user_id}))
        tokens_factory.get_generator.assert_called_once_with(TokenGeneratorFactory.LOGIN_TOKEN, user_facade.session)
