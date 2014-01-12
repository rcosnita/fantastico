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

from fantastico.contrib.oauth2_idp.models.users import User
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.mvc.models.model_filter_compound import ModelFilterAnd
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError, OAuth2AuthenticationError, OAuth2Error
from fantastico.oauth2.models.return_urls import ClientReturnUrl
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.oauth2.token import Token
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
from fantastico.routing_engine.custom_responses import RedirectResponse
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils.dictionary_object import DictionaryObject
from mock import Mock
import time
import urllib

class IdpControllerTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for oauth2 fantastico identity provider controller.'''

    _IDP_CLIENTID = "11111111-1111-1111-1111-111111111111"
    _TPL_LOGIN = "/mock/location/views/login.html"
    _EXPIRES_IN = 3600

    _idp_controller = None
    _hasher = None

    _tokens_service = None
    _tokens_service_cls = None

    def init(self):
        '''This method is invoked automatically in order to setup dependencies common to all test cases.'''

        from fantastico.contrib.oauth2_idp.idp_controller import IdpController

        oauth2_idp = {"client_id": self._IDP_CLIENTID,
                      "template": self._TPL_LOGIN,
                      "expires_in": self._EXPIRES_IN}

        self._hasher = Mock()
        self._hasher.get_hasher = Mock(return_value=self._hasher)
        hasher_cls = Mock(return_value=self._hasher)

        settings_facade = Mock()
        settings_facade.get = Mock(return_value=oauth2_idp)

        self._idp_controller = IdpController(settings_facade, passwords_hasher_cls=hasher_cls)

        settings_facade.get.assert_called_once_with("oauth2_idp")
        hasher_cls.assert_called_once_with()
        self._hasher.get_hasher.assert_called_once_with(PasswordsHasherFactory.SHA512_SALT)

        self._tokens_service = Mock()
        self._tokens_service_cls = Mock(return_value=self._tokens_service)

    def test_show_login_ok(self):
        '''This test case ensures login screen is displayed correctly when all required parameters are passed.'''

        redirect_param_name = self._idp_controller.REDIRECT_PARAM

        request = Mock()
        request.params = {redirect_param_name: "/simple/test"}

        self._idp_controller.load_template = Mock(return_value="cool result")

        response = self._idp_controller.show_login(request)

        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)

        self.assertIsNotNone(response.body)
        body = response.body.decode()

        self.assertEqual("cool result", body)

        self._idp_controller.load_template.assert_called_once_with(
                                        self._TPL_LOGIN,
                                        {redirect_param_name: urllib.parse.quote(request.params[redirect_param_name])},
                                        enable_global_folder=True)

    def test_show_login_missingreturn(self):
        '''This test case ensures login screen is not displayed if return_url query parameter is not provided.'''

        request = Mock()
        request.params = {}

        for return_url in [None, "", "    "]:
            request.params[self._idp_controller.REDIRECT_PARAM] = return_url

            with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
                self._idp_controller.show_login(request)

            self.assertEqual(self._idp_controller.REDIRECT_PARAM, ctx.exception.param_name)

    def test_authenticate_ok(self):
        '''This test case ensures a correct login token is generated during authentication phase. It also checks for correct
        redirect response.'''

        return_url = "http://expected-url.com/cb"
        expected_url = "http://expected-url.com/cb?login_token=123"

        self._test_authenticate_ok(return_url, expected_url)

    def test_authenticate_returnwithparams_ok(self):
        '''This test case ensures a correct login token is generated during authentication phase. It also checks that return_url
        receives login_token as an additional query parameter. Moreover, this test case ensures that original return_url query
        parameters are kept.'''

        return_url = "http://expected-url.com/cb?state=xyz"
        expected_url = "http://expected-url.com/cb?state=xyz&login_token=123"

        self._test_authenticate_ok(return_url, expected_url)

    def _test_authenticate_ok(self, return_url, expected_url):
        '''This method provides a template test case for ensuring authenticate succeeds for various return_url values.'''

        user = User(username="john.doe@gmail.com",
                    password="12345",
                    person_id=1)
        user.user_id = 123

        creation_time, expiration_time = self._mock_creationexpiration_time()

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        response = self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls,
                                                     user_repo_cls=user_repo_cls)

        self.assertIsNotNone(response)
        self.assertEqual(302, response.status_code)

        location = response.headers.get("Location")

        self.assertEqual(expected_url, location)

        user_repo.load_by_username.assert_called_once_with(user.username)
        self._hasher.hash_password.assert_called_once_with(user.password, DictionaryObject({"salt": user.user_id}))

        tokens_service_cls.assert_called_once_with(clienturl_facade.session)
        tokens_service.generate.assert_called_once_with({"client_id": self._IDP_CLIENTID,
                                                         "user_id": user.user_id,
                                                         "expires_in": self._EXPIRES_IN}, TokenGeneratorFactory.LOGIN_TOKEN)
        tokens_service.encrypt.assert_called_once_with(token, token.client_id)


    def test_authenticate_missing_username(self):
        '''This test case ensures an exception is raised when the username is not posted.'''

        user = User()

        self._test_authenticate_missing_param(user, None, "username")

    def test_authenticate_missing_password(self):
        '''This test case ensures an exception is raised when the password is not posted.'''

        user = User(username="john.doe")

        self._test_authenticate_missing_param(user, None, "password")

    def test_authenticate_missing_redirecturi(self):
        '''This test case ensures an exception is raised when the return url query parameter is missing.'''

        user = User(username="john.doe", password="12345")

        self._test_authenticate_missing_param(user, None, self._idp_controller.REDIRECT_PARAM)

    def test_authenticate_invalid_redirecturi(self):
        '''This test case ensures an exception is raised when the return url query parameter is not accepted by idp.'''

        creation_time, expiration_time = self._mock_creationexpiration_time()

        user = User(username="john.doe@gmail.com", password="12345")
        user.session = Mock()

        return_url = "/test/url?state=xyz"

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        clienturl_facade.get_records_paged = Mock(return_value=[])

        with self.assertRaises(OAuth2MissingQueryParamError):
            self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls, user_repo_cls=user_repo_cls)

        return_url = return_url[:return_url.find("?")]
        clienturl_facade.get_records_paged.assert_called_once_with(
                                    start_record=0, end_record=1,
                                    filter_expr=ModelFilterAnd(
                                                    ModelFilter(ClientReturnUrl.client_id, self._IDP_CLIENTID, ModelFilter.EQ),
                                                    ModelFilter(ClientReturnUrl.return_url, return_url, ModelFilter.EQ)))

    def _test_authenticate_missing_param(self, user, return_url, param_name):
        '''This method provides a template test case for checking missing required query parameters tests.'''

        creation_time, expiration_time = self._mock_creationexpiration_time()

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
            self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls, user_repo_cls=user_repo_cls)

        self.assertEqual(param_name, ctx.exception.param_name)

    def test_authenticate_usernotfound(self):
        '''This test case ensures a concrete exception is raised when user is not found.'''

        creation_time, expiration_time = self._mock_creationexpiration_time()

        user = User(username="john.doe@gmail.com", password="123456")
        user.session = Mock()

        return_url = "/test/url"

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        user_repo.load_by_username = Mock(return_value=None)

        with self.assertRaises(OAuth2AuthenticationError):
            self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls, user_repo_cls=user_repo_cls)

        user_repo.load_by_username.assert_called_once_with(user.username)

    def test_authenticate_different_passwords(self):
        '''This test case ensures an exception is raised when passwords do not match.'''

        creation_time, expiration_time = self._mock_creationexpiration_time()

        user = User(username="john.doe@gmail.com", password="123456")
        user.session = Mock()

        return_url = "/test/url"

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        with self.assertRaises(OAuth2AuthenticationError):
            self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls, user_repo_cls=user_repo_cls)

    def test_authenticate_user_repoex(self):
        '''This test case ensures unexpected exceptions raised by user repo are casted to concrete oauth2 exceptions.'''

        with self.assertRaises(OAuth2AuthenticationError):
            self._test_authenticate_userrepo_ex(Exception("Unexpected error."))

    def test_authenticate_user_repooauth2ex(self):
        '''This test case ensures oauth2 exceptions raised by user repo are bubbled up.'''

        ex = OAuth2Error(error_code= -1)

        with self.assertRaises(OAuth2Error) as ctx:
            self._test_authenticate_userrepo_ex(ex)

        self.assertEqual(ex, ctx.exception)

    def _test_authenticate_userrepo_ex(self, ex):
        '''This method provides a template test case which allows user_repo dependencies to throw various exceptions.'''

        creation_time, expiration_time = self._mock_creationexpiration_time()

        user = User(username="john.doe@gmail.com", password="12345")
        user.session = Mock()

        return_url = "/test/url"

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        user_repo.load_by_username = Mock(side_effect=ex)

        self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls, user_repo_cls=user_repo_cls)

    def test_authenticate_passwordhasher_ex(self):
        '''This test case ensures unexpected exceptions raised by password hasher are casted to concrete oauth2 exceptions.'''

        with self.assertRaises(OAuth2AuthenticationError):
            self._test_authenticate_passwordhasher_ex(Exception("Unexpected exception."))

    def test_authenticate_passwordhasher_oauth2ex(self):
        '''This test case ensures oauth2 exceptions raised by password hasher are bubbled up.'''

        ex = OAuth2Error(error_code= -1)

        with self.assertRaises(OAuth2Error) as ctx:
            self._test_authenticate_passwordhasher_ex(ex)

        self.assertEqual(ex, ctx.exception)

    def _test_authenticate_passwordhasher_ex(self, ex):
        '''This method provides a template test case which allows password hasher to raise various exceptions.'''

        creation_time, expiration_time = self._mock_creationexpiration_time()

        user = User(username="john.doe@gmail.com", password="12345")
        user.session = Mock()

        return_url = "/test/url"

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        self._hasher.hash_password = Mock(side_effect=ex)

        self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls, user_repo_cls=user_repo_cls)

    def test_authenticate_generatetoken_ex(self):
        '''This test case ensures unexpected exceptions raised during token generation are casted to concrete oauth2 exceptions.'''

        with self.assertRaises(OAuth2Error):
            self._test_authenticate_generatetoken_ex(Exception("Unexpected exception."))

    def test_authenticate_generatetoken_oauth2ex(self):
        '''This test case ensures oauth2 exceptions raised during token generation are bubbled up.'''

        ex = OAuth2Error(error_code= -1)

        with self.assertRaises(OAuth2Error) as ctx:
            self._test_authenticate_generatetoken_ex(ex)

        self.assertEqual(ex, ctx.exception)

    def _test_authenticate_generatetoken_ex(self, ex):
        '''This method provides a template test case which allows tokens service generate method to raise various exceptions.'''

        creation_time, expiration_time = self._mock_creationexpiration_time()

        user = User(username="john.doe@gmail.com", password="12345")
        user.session = Mock()

        return_url = "/test/url"

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        tokens_service.generate = Mock(side_effect=ex)

        self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls, user_repo_cls=user_repo_cls)

    def test_authenticate_encrypt_ex(self):
        '''This test case ensures unexpected exceptions raised during token encryption are casted to oauth2 exceptions.'''

        with self.assertRaises(OAuth2AuthenticationError):
            self._test_authenticate_encrypt_ex(Exception("Unexpected exception."))

    def test_authenticate_encrypt_oauth2ex(self):
        '''This test case ensures oauth2 exceptions raised during token encryption are bubbled up.'''

        ex = OAuth2Error(error_code= -1)

        with self.assertRaises(OAuth2Error) as ctx:
            self._test_authenticate_encrypt_ex(ex)

        self.assertEqual(ex, ctx.exception)

    def _test_authenticate_encrypt_ex(self, ex):
        '''This method provides a template test case which allows token encrypt method to raise various exceptions.'''

        creation_time, expiration_time = self._mock_creationexpiration_time()

        user = User(username="john.doe@gmail.com", password="12345")
        user.session = Mock()

        return_url = "/test/url"

        token = Token({"client_id": self._IDP_CLIENTID,
                       "type": "login",
                       "user_id": user.user_id,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        request, user_repo_cls, user_repo, tokens_service_cls, \
            tokens_service, clienturl_facade = self._mock_authenticate_dependencies(token, user, return_url)

        tokens_service.encrypt = Mock(side_effect=ex)

        self._idp_controller.authenticate(request, tokens_service_cls=tokens_service_cls, user_repo_cls=user_repo_cls)

    def test_authenticate_unsupportedreturn_url(self):
        '''This test case ensures return url value is defined in the list of supported return urls accepted by Fantastico
        OAuth2 IDP.'''

    def _mock_authenticate_dependencies(self, token, user, return_url):
        '''This method mocks authenticate dependencies and returns them as a tuple object.'''

        if return_url:
            return_url_base = return_url

            if return_url_base.find("?") > -1:
                return_url_base = return_url_base[:return_url_base.find("?")]

        clienturl_facade = Mock()

        if return_url:
            clienturl_facade.get_records_paged = Mock(return_value=[return_url_base])
        clienturl_facade.session = Mock()

        request = Mock()
        request.params = {"username": user.username,
                          "password": user.password,
                          self._idp_controller.REDIRECT_PARAM: return_url}
        request.models = Mock()
        request.models.ClientReturnUrl = clienturl_facade
        request.redirect = lambda destination: RedirectResponse(destination)

        user_repo = Mock()
        user_repo.load_by_username = Mock(return_value=user)
        user_repo_cls = Mock(return_value=user_repo)

        self._hasher.hash_password = Mock(return_value="12345")

        tokens_service = Mock()
        tokens_service_cls = Mock(return_value=tokens_service)

        tokens_service.generate = Mock(return_value=token)
        tokens_service.encrypt = Mock(return_value="123")

        return (request, user_repo_cls, user_repo, tokens_service_cls, tokens_service, clienturl_facade)

    def _mock_creationexpiration_time(self):
        '''This method calculates creation and expiration time values.'''

        creation_time = int(time.time())
        expiration_time = creation_time + self._EXPIRES_IN

        return creation_time, expiration_time
