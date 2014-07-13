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
.. py:module:: fantastico.oauth2.tests.test_implicit_granthandler
'''
import urllib

from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError
from fantastico.oauth2.implicit_grant_handler import ImplicitGrantHandler
from fantastico.oauth2.token import Token
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
from fantastico.routing_engine.custom_responses import RedirectResponse
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from webob.request import Request
from webob.response import Response


class ImplicitGrantHandlerTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for implicit grant handler.'''

    _EXPIRES_IN = 3600

    _settings_facade = None
    _tokens_service = None
    _handler = None
    _oauth2_idp = None
    _client_repo = None

    def init(self):
        '''This method is invoked automatically in order to setup common dependencies for all test cases.'''

        self._oauth2_idp = {"client_id": "11111111-1111-1111-1111-111111111111",
                            "template": "/components/frontend/views/custom_login.html",
                            "expires_in": 1209600,
                            "idp_index": "/oauth/idp/ui/login"}

        self._client_repo = Mock()
        client_repo_cls = Mock(return_value=self._client_repo)

        self._tokens_service = Mock()
        self._tokens_service.db_conn = Mock()
        self._tokens_service.validate = Mock(return_value=None)

        self._settings_facade = Mock()

        self._settings_facade.get = self._mock_get_setting

        self._handler = ImplicitGrantHandler(self._tokens_service, self._settings_facade, client_repo_cls=client_repo_cls)

        client_repo_cls.assert_called_once_with(self._tokens_service.db_conn)

    def _mock_get_setting(self, setting_name):
        '''This method mocks settings_facade get for expected settings used in implicit grant handler.'''

        if setting_name == "access_token_validity":
            return self._EXPIRES_IN

        if setting_name == "oauth2_idp":
            return self._oauth2_idp

        raise ValueError("Setting %s must not be accessed." % setting_name)

    def test_handle_ok(self):
        '''This test case ensures implicit grant works as expected when all prerequisites are fulfilled.'''

        client_id = "sample app"
        redirect_uri = "/example/cb"
        scope = "scope1 scope2"
        state = "xyz"

        encrypted_login = "abcd"

        self._test_handle_template(client_id, redirect_uri, scope, state, encrypted_login)

    def test_handle_noredirect_ok(self):
        '''This test case ensures implicit grant without redirect works as expected when all prerequisites 
        are fulfilled.'''

        client_id = "sample app"
        redirect_uri = "/example/cb"
        scope = "scope1 scope2"
        state = "xyz"

        encrypted_login = "abcd"
        
        redirect = 0

        self._test_handle_template(client_id, redirect_uri, scope, state, encrypted_login, 
                                   redirect_qparam=redirect)
    
    def test_handle_ok_redirectwithhash(self):
        '''This test case ensures implicit grant works as expected even when redirect uri has a fragment in it.'''

        client_id = "sample app"
        redirect_uri = "/example/cb#a=b"
        scope = "scope1 scope2"
        state = "xyz"

        encrypted_login = "abcd"

        encrypted_access = "abcd"
        expected_redirect = "%s&access_token=%s&state=%s&token_type=access&expires_in=%s&scope=%s" % \
                                    (redirect_uri, encrypted_access,
                                     urllib.parse.quote(state), self._EXPIRES_IN,
                                     urllib.parse.quote(scope))

        self._test_handle_template(client_id, redirect_uri, scope, state, encrypted_login,
                                   expected_redirect=expected_redirect,
                                   encrypted_access=encrypted_access)

    def test_handle_missing_client(self):
        '''This test case ensures a missing query parameter exception is raised when client_id is missing.'''

        with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
            self._test_handle_missingparam(client_id=None)

        self.assertEqual("client_id", ctx.exception.param_name)

    def test_handle_missing_redirecturi(self):
        '''This test case ensures a missing query parameter exception is raised when redirect_uri is missing.'''

        with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
            self._test_handle_missingparam(client_id="sample", redirect_uri=None)

            self.assertEqual("redirect_uri", ctx.exception.param_name)

    def test_handle_missing_state(self):
        '''This test case ensures a missing query parameter exception is raised when state is missing.'''

        with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
            self._test_handle_missingparam(client_id="sample", redirect_uri="/example/cb", state=None)

        self.assertEqual("state", ctx.exception.param_name)

    def test_handle_missing_scope(self):
        '''This test case ensures a missing query parameter exception is raised when scope is missing.'''

        with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
            self._test_handle_missingparam(client_id="sample", redirect_uri="/example/cb", state="xyz", scope=None)

        self.assertEqual("scope", ctx.exception.param_name)

    def test_handle_missing_login(self):
        '''This test case ensures a redirect response to idp is received if login_token query parameter is missing.'''

        request_url = "/oauth/authorize?response_type=token&state=xyz&error_format=hash&client_id=11111111-1111-1111-1111-111111111111&scope=scope1&redirect_uri=%2Fexample%2Fcb"
        expected_url = "%s?redirect_uri=%s" % (self._oauth2_idp["idp_index"], urllib.parse.quote(request_url))

        request = Request.blank(request_url)
        request.redirect = lambda url: RedirectResponse(url)

        response = self._handler.handle_grant(request)

        self.assertIsInstance(response, RedirectResponse)
        self.assertEqual(expected_url, response.headers["Location"])

    def test_handle_grant_invalidredirect(self):
        '''This test case ensures an exception is raised if the given redirect uri is not supported by the current client.'''

        client_id = "abcd"
        redirect_uri = "/abcduri"

        request = Mock()
        request.params = {"client_id": client_id,
                          "redirect_uri": redirect_uri,
                          "state": "xyz",
                          "scope": "a b c"}

        self._client_repo.load_client_by_returnurl = Mock(return_value=None)

        response = self._handler.handle_grant(request)

        self.assertIsNotNone(response)
        self.assertEqual(401, response.status_code)
        self.assertTrue(response.body.decode().find(redirect_uri) > -1)

        self._client_repo.load_client_by_returnurl.assert_called_once_with(redirect_uri)

    def test_error_redirect(self):
        '''This test case ensures a redirect response is sent if the implicit handler request contains error query parameter.
        This case occurs only when authentication fails.'''

        request = Mock()
        request.params = {"client_id": "sample-app",
                          "redirect_uri": "/sample/cb",
                          "state": "xyz",
                          "error": "access_denied",
                          "error_description": "Simple error.",
                          "error_uri": "/sample/uri/122.html"}

        response = self._handler.handle_grant(request)

        self.assertIsInstance(response, RedirectResponse)

        expected_redirect = "%s#error=%s&error_description=%s&error_uri=%s&state=%s" % \
                                (request.params["redirect_uri"],
                                 request.params["error"],
                                 urllib.parse.quote(request.params["error_description"]),
                                 urllib.parse.quote(request.params["error_uri"]), request.params["state"])

        self.assertEqual(expected_redirect, response.headers["Location"])

    def _test_handle_missingparam(self, client_id=None, redirect_uri=None, scope=None, state=None, encrypted_login=None):
        '''This method provides a template for testing handle_grant method from implicit provider when mandatory query
        parameters are missing.'''

        return self._test_handle_template(client_id, redirect_uri, scope, state, encrypted_login)

    def _test_handle_template(self, client_id, redirect_uri, scope, state, encrypted_login, expected_redirect=None,
                              encrypted_access=None, redirect_qparam=None):
        '''This method provides a template for testing handle_grant method from implicit grant provider.'''

        if not encrypted_access:
            encrypted_access = "encrypted access token"

        if not expected_redirect:
            scope = scope or ""
            state = state or ""
            expected_redirect = "%s#access_token=%s&state=%s&token_type=access&expires_in=%s&scope=%s" % \
                                    (redirect_uri, encrypted_access,
                                     urllib.parse.quote(state), self._EXPIRES_IN,
                                     urllib.parse.quote(scope))

        login_token = Token({"user_id": 1})

        access_token = Token({"type": "access"})

        request = Mock()
        request.params = {"client_id": client_id,
                          "redirect_uri": redirect_uri,
                          "scope": scope,
                          "state": state,
                          "login_token": encrypted_login,
                          "redirect": redirect_qparam}

        self._tokens_service.decrypt = Mock(return_value=login_token)
        self._tokens_service.generate = Mock(return_value=access_token)
        self._tokens_service.encrypt = Mock(return_value=encrypted_access)

        response = self._handler.handle_grant(request)

        if not redirect_qparam:
            self.assertIsInstance(response, RedirectResponse)
        else:
            self.assertIsInstance(response, Response)
            
        self.assertEqual(expected_redirect, response.headers.get("Location"))

        self._tokens_service.decrypt.assert_called_once_with(encrypted_login)
        self._tokens_service.validate.assert_called_once_with(login_token)
        self._tokens_service.generate.assert_called_once_with({"client_id": client_id,
                                                               "user_id": login_token.user_id,
                                                               "scopes": scope,
                                                               "expires_in": self._EXPIRES_IN},
                                                              TokenGeneratorFactory.ACCESS_TOKEN)
        self._tokens_service.encrypt.assert_called_once_with(access_token, client_id)
