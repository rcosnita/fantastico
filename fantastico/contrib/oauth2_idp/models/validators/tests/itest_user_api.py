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
from fantastico.contrib.oauth2_idp.models.persons import Person
from fantastico.contrib.oauth2_idp.models.users import User
from fantastico.mvc.model_facade import ModelFacade
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
        self._invalidate_oauth2_token(self._access_token)
        self._access_token = None

    def _create_user(self, hostname, port):
        '''This method simply creates a new user using the api and returns the new user username.'''

        username = "admintest@fantastico.com"

        endpoint = "/api/latest/oauth-idp-profile"

        user = {"username": username, "password": "123456"}

        http_conn = http.client.HTTPConnection(hostname, port)

        http_conn.request("POST", endpoint, json.dumps(user))

        response = http_conn.getresponse()

        self.assertIsNotNone(response)
        self.assertEqual(201, response.status)

        location = response.headers.get("Location")
        self.assertIsNotNone(location)

        http_conn.close()

        return location.split("/")[-1]

    def _delete_user(self, user_id, token, hostname, port):
        '''This method removes the requested user_id.'''

        db_conn = None
        conn_manager = None
        request_id = None

        person_facade = None
        person = None

        try:
            conn_manager, request_id, db_conn = self._get_db_conn()

            person_facade = ModelFacade(Person, db_conn)
            user = ModelFacade(User, db_conn).find_by_pk({User.user_id: user_id})
            person = person_facade.find_by_pk({Person.person_id: user.person_id})

            endpoint = "/api/latest/oauth-idp-profile/%s?token=%s" % (user_id, token)

            http_conn = http.client.HTTPConnection(hostname, port)

            http_conn.request("DELETE", endpoint)

            response = http_conn.getresponse()

            http_conn.close()

            self.assertIsNotNone(response)
            self.assertEqual(204, response.status)
        finally:
            if person:
                person_facade.delete(person)

            if db_conn:
                conn_manager.close_connection(request_id)

    def test_retrieve_user_ok(self):
        '''This test case ensures default user used in tests can be retrieved correctly.'''

        results = {"user_id": None, "token": None}

        def get_new_user(server):
            '''This method triggers an http get on default user.'''

            results["user_id"] = user_id = int(self._create_user(server.hostname, server.port))
            results["token"] = access_token = self._get_oauth2_token(self.DEFAULT_CLIENT_ID, user_id, self.SCOPES)

            http_conn = http.client.HTTPConnection(host=server.hostname, port=server.port)

            http_conn.request("GET", "/api/latest/oauth-idp-profile/%s" % user_id,
                              headers={"Authorization": "Bearer %s" % access_token})

            results["response"] = http_conn.getresponse()

            http_conn.close()

            self._delete_user(user_id, access_token, server.hostname, server.port)

        def assert_user(server):
            '''This method assert the user response against expected results.'''

            response = results.get("response")

            self.assertIsNotNone(response)
            self.assertEqual(200, response.status)

            body = response.read()
            self.assertIsNotNone(body)

            body = json.loads(body.decode())

            self.assertNotIn("password", body)
            self.assertEqual("admintest@fantastico.com", body["username"])
            self.assertEqual(results.get("user_id"), body["user_id"])
            self.assertGreater(body["person_id"], 1)

        self._run_test_against_dev_server(get_new_user, assert_user)

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
