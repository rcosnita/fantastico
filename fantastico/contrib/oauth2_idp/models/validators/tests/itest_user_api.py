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
.. py:module:: fantastico.oauth2_idp.models.tests.itest_user_api
'''
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from fantastico.settings import SettingsFacade
import http
import json

class UserResourceIntegrationTests(DevServerIntegration):
    '''This class provides the integration tests which ensures that CRUD operations work as expected on user resource. We do this
    because we also want to validate oauth2 roa validation.'''

    DEFAULT_CLIENT_ID = None
    DEFAULT_USER_ID = 1
    SCOPES = "user.profile.read user.profile.update user.profile.delete"

    _access_token = None
    _settings_facade = None

    def init(self):
        '''This method is invoked before executing each test case. It generates an access_token which is authorized to access user
        api.'''

        self._settings_facade = SettingsFacade()
        self.DEFAULT_CLIENT_ID = self._settings_facade.get("oauth2_idp")["client_id"]
        self._access_token = self._get_oauth2_token(self.DEFAULT_CLIENT_ID, self.DEFAULT_USER_ID, self.SCOPES)

    def cleanup(self):
        self._access_token = None

    def test_retrieve_user_ok(self):
        '''This test case ensures default user used in tests can be retrieved correctly.'''

        results = {}

        def get_default_user(server):
            '''This method triggers an http get on default user.'''

            http_conn = http.client.HTTPConnection(host=server.hostname, port=server.port)

            http_conn.request("GET", "/api/latest/oauth-idp-profile/%s" % self.DEFAULT_USER_ID,
                              headers={"Authorization": "Bearer %s" % self._access_token})

            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_user(server):
            '''This method assert the user response against expected results.'''

            response = results.get("response")

            self.assertIsNotNone(response)
            self.assertEqual(200, response.status)

            body = response.read()
            self.assertIsNotNone(body)

            body = json.loads(body.decode())

            self.assertNotIn("password", body)
            self.assertEqual("admin@fantastico.com", body["username"])
            self.assertEqual(1, body["user_id"])
            self.assertEqual(1, body["person_id"])

        self._run_test_against_dev_server(get_default_user, assert_user)

    def test_retrieve_users_ok(self):
        '''This test case ensures users can be retrieved .'''

        results = {}

        def get_default_user(server):
            '''This method triggers an http get on default users collection endpoint.'''

            http_conn = http.client.HTTPConnection(host=server.hostname, port=server.port)

            http_conn.request("GET", "/api/latest/oauth-idp-profile?token=%s" % self._access_token)

            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_user(server):
            '''This method assert the user response against expected results.'''

            response = results.get("response")

            self.assertIsNotNone(response)
            self.assertEqual(200, response.status)

            body = response.read()
            self.assertIsNotNone(body)

            body = json.loads(body.decode())

            items = body.get("items")
            self.assertNotIn("password", items[0])
            self.assertEqual("admin@fantastico.com", items[0]["username"])
            self.assertEqual(1, items[0]["user_id"])
            self.assertEqual(1, items[0]["person_id"])

        self._run_test_against_dev_server(get_default_user, assert_user)

    def test_get_users_unauthorized(self):
        '''This method ensures users collection can not be accessed without an access token sent.'''

        results = {}

        def get_users(server):
            '''This method triggers an http get on default user.'''

            http_conn = http.client.HTTPConnection(host=server.hostname, port=server.port)

            http_conn.request("GET", "/api/latest/oauth-idp-profile")

            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_unauthorized(server):
            '''This method assert the user response against expected results.'''

            response = results.get("response")

            self.assertIsNotNone(response)
            self.assertEqual(401, response.status)

        self._run_test_against_dev_server(get_users, assert_unauthorized)
