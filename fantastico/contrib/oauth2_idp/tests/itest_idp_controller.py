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
.. py:module:: fantastico.contrib.oauth2_idp.test.itest_idp_controller
'''
from fantastico.server.tests.itest_dev_server import DevServerIntegration
import http

class IdpControllerIntegrationTests(DevServerIntegration):
    '''This class provides the tests suite for idp controller.'''

    def test_authenticate_ok(self):
        '''This test case ensures authenticate works as expected and redirect to specified redirect_uri.'''

        username = "admin@fantastico.com"
        password = "1234567890"

        redirect_uri = "/oauth/authorize"
        endpoint = "/oauth/idp/login?error_format=form&redirect_uri=%s" % redirect_uri
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        results = {}

        def authenticate_user(server):
            http_conn = http.client.HTTPConnection(host=server.hostname, port=server.port)

            http_conn.request("POST", endpoint,
                              body="username=%s&password=%s" % (username, password),
                              headers=headers)

            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_authentication(server):
            response = results.get("response")

            self.assertIsNotNone(response)

            self.assertEqual(302, response.status)

            location = response.headers.get("Location")
            self.assertIsNotNone(location)
            self.assertTrue(location.startswith("%s?login_token=" % redirect_uri))

            location = location[len("%s?login_token=" % redirect_uri):]
            first_qparam = location.find("&")

            if first_qparam == -1:
                first_qparam = len(location)

            login_token = location[:first_qparam]
            self.assertIsNotNone(login_token)
            self.assertGreater(len(login_token), 300)

        self._run_test_against_dev_server(authenticate_user, assert_authentication)

    def test_idp_loginscreen_ok(self):
        '''This test case ensures the login screen can be correctly displayed.'''

        endpoint = "/oauth/idp/ui/login?redirect_uri=/example/cb"

        results = {}

        def access_loginscreen(server):
            '''This method tries to do a successful get on login screen.'''

            http_conn = http.client.HTTPConnection(server.hostname, server.port)

            http_conn.request("GET", endpoint)

            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_displayed_ok(server):
            '''This method asserts the output to ensure login screen was loaded successfully.'''

            response = results.get("response")

            self.assertIsNotNone(response)
            self.assertEqual(200, response.status)

            body = response.read()

            self.assertIsNotNone(body)
            self.assertGreater(len(body), 0)

        self._run_test_against_dev_server(access_loginscreen, assert_displayed_ok)
