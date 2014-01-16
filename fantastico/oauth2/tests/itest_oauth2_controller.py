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
.. py:module:: fantastico.oauth2.tests.itest_oauth2_controller
'''
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from fantastico.settings import SettingsFacade
import http
import re
import urllib

class OAuth2ControllerIntegrationTests(DevServerIntegration):
    '''This class provides the integration tests suite for ensuring oauth2 controller works as expected.'''

    DEFAULT_CLIENT_ID = None
    DEFAULT_USER_ID = 1
    DEFAULT_SCOPES = "user.profile.read user.profile.update user.profile.delete"
    TOKEN_VALIDITY = None

    _settings_facade = None

    def init(self):
        '''This method is invoked in order to set all common dependencies for test cases.'''

        self._settings_facade = SettingsFacade()

        self.DEFAULT_CLIENT_ID = self._settings_facade.get("oauth2_idp")["client_id"]
        self.TOKEN_VALIDITY = self._settings_facade.get("access_token_validity")

    def test_implicit_grant(self):
        '''This test case ensures implicit grant type success scenario works as expected.'''

        state = "abcd xyz&abc"
        redirect_uri = "/oauth/idp/ui/cb"
        login_token = self._get_oauth2_logintoken(self.DEFAULT_CLIENT_ID, self.DEFAULT_USER_ID)
        endpoint = "/oauth/authorize?response_type=token&client_id=%s&login_token=%s&state=%s&scope=%s&redirect_uri=%s" % \
                    (self.DEFAULT_CLIENT_ID, login_token,
                     urllib.parse.quote(state),
                     urllib.parse.quote(self.DEFAULT_SCOPES),
                     urllib.parse.quote(redirect_uri))
        results = {}

        def trigger_implicit_flow(server):
            http_conn = http.client.HTTPConnection(host=server.hostname, port=server.port)
            http_conn.request("GET", endpoint)

            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_success(server):
            '''This method ensures the flow completed successfully by checking the location and hash part of the location.'''

            response = results["response"]

            self.assertIsNotNone(response)
            self.assertEqual(302, response.status)

            location = response.headers["Location"]

            self.assertIsNotNone(location)
            self.assertTrue(location.startswith("%s#access_token=" % redirect_uri))
            self.assertTrue(location.find("&expires_in=%s" % self.TOKEN_VALIDITY) > -1)
            self.assertTrue(location.find("&state=%s" % urllib.parse.quote(state)) > -1)
            self.assertTrue(location.find("&scope=%s" % urllib.parse.quote(self.DEFAULT_SCOPES)) > -1)

            location = location.replace("%s#access_token=" % redirect_uri, "")
            access_token = location[:location.find("&")]

            self.assertGreater(len(access_token), 400)

        self._run_test_against_dev_server(trigger_implicit_flow, assert_success)

    def test_authorize_implicit_missing_param_form(self):
        '''This test case ensures error, error_uri and error_description query parameters are appended to redirect_uri passed
        for implicit grant type.'''

        self._test_error_handling_implicit_graceful("form", "?")

    def test_authorize_implicit_missing_param_hash(self):
        '''This test case ensures error, error_uri and error_description query parameters are appended to redirect_uri passed
        for implicit grant type (into hash section).'''

        self._test_error_handling_implicit_graceful("hash", "#")

    def _test_error_handling_implicit_graceful(self, format, delimiter):
        '''This method provides a template for ensuring error handling method types which describe error through redirect
        and query or hash strings work as expected.'''

        endpoint = "/oauth/authorize?error_format=%s&redirect_uri=/example/cb" % format

        results = {}

        def invoke_implicit(server):
            '''This method tries to retrieve login screen.'''

            http_conn = http.client.HTTPConnection(server.hostname, server.port)

            http_conn.request("GET", endpoint)
            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_error_graceful(server):
            '''This method asserts that error was gracefully handled by OAuth2 exceptions middleware.'''

            response = results.get("response")

            self.assertIsNotNone(response)
            self.assertEqual(302, response.status)

            location = response.headers.get("Location")
            self.assertIsNotNone(location)

            self.assertTrue(location.startswith("/example/cb%s" % delimiter))
            self.assertTrue(location.find("error=invalid_request") > -1, "%s does not contain error query param." % location)

            result = re.findall(r"error_description=(.*)&", location)
            self.assertEqual(1, len(result), "%s does not contain error_description query param." % location)

            result = re.findall(r"error_uri=(.*)", location)
            self.assertEqual(1, len(result), "%s does not contain error_uri query param." % location)


        self._run_test_against_dev_server(invoke_implicit, assert_error_graceful)
