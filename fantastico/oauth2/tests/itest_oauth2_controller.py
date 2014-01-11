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
import urllib

class OAuth2ControllerIntegrationTests(DevServerIntegration):
    '''This class provides the integration tests suite for ensuring oauth2 controller works as expected.'''

    DEFAULT_CLIENT_ID = SettingsFacade().get("oauth2_idp")["client_id"]
    DEFAULT_USER_ID = 1
    DEFAULT_SCOPES = "user.profile.read user.profile.update user.profile.delete"
    TOKEN_VALIDITY = SettingsFacade().get("access_token_validity")

    def test_implicit_grant(self):
        '''This test case ensures implicit grant type success scenario works as expected.'''

        redirect_uri = "/oauth/idp/ui/cb"
        login_token = self._get_oauth2_logintoken(self.DEFAULT_CLIENT_ID, self.DEFAULT_USER_ID)
        endpoint = "/oauth/authorize?response_type=token&client_id=%s&login_token=%s&state=xyz&scope=%s&redirect_uri=%s" % \
                    (self.DEFAULT_CLIENT_ID, login_token, urllib.parse.quote(self.DEFAULT_SCOPES),
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
            self.assertTrue(location.find("&state=xyz") > -1)
            self.assertTrue(location.find("&scope=%s" % self.DEFAULT_SCOPES) > -1)

            location = location.replace("%s#access_token=" % redirect_uri, "")
            access_token = location[:location.find("&")]

            self.assertGreater(len(access_token), 400)

        self._run_test_against_dev_server(trigger_implicit_flow, assert_success)
