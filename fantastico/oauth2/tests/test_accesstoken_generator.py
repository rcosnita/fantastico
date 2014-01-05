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
.. py:module:: fantastico.oauth2.tests.test_accesstoken_generator
'''
from fantastico.exceptions import FantasticoDbNotFoundError
from fantastico.oauth2.accesstoken_generator import AccessTokenGenerator
from fantastico.oauth2.exceptions import OAuth2InvalidTokenDescriptorError, OAuth2InvalidClientError, OAuth2InvalidScopesError, \
    OAuth2InvalidTokenTypeError, OAuth2TokenExpiredError
from fantastico.oauth2.models.clients import Client
from fantastico.oauth2.models.scopes import Scope
from fantastico.oauth2.token import Token
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import time
import uuid

class AccessTokenGeneratorTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for access tokens generator.'''

    _db_conn = None
    _model_facade = None
    _generator = None

    def init(self):
        '''This method is invoked in order to set up common dependencies for every test case.'''

        self._db_conn = Mock()
        self._model_facade = Mock()
        model_facade_cls = Mock(return_value=self._model_facade)

        self._generator = AccessTokenGenerator(self._db_conn, model_facade_cls=model_facade_cls)

    def test_generate_ok(self):
        '''This test case ensures an access token can be correctly generated.'''

        creation_time = time.time()

        time_provider = Mock()
        time_provider.time = Mock(return_value=creation_time)

        token_desc = {"client_id": "my-sample-app",
                      "user_id": 123,
                      "scopes": "scope1 scope2 scope3 scope4",
                      "expires_in": 3600}

        expected_client = Client()
        expected_client.scopes = [Scope(name=scope) for scope in token_desc["scopes"].split(" ")]

        self._mock_client_search(expected_client)

        token = self._generator.generate(token_desc, time_provider)

        self.assertIsNotNone(token)
        self.assertEqual(token_desc["client_id"], token.client_id)
        self.assertEqual(token_desc["user_id"], token.user_id)
        self.assertEqual(token_desc["scopes"].split(" "), token.scopes)
        self.assertEqual(int(creation_time), token.creation_time)
        self.assertEqual(int(creation_time) + token_desc["expires_in"], token.expiration_time)

    def test_generate_noclientid(self):
        '''This test case ensures an exception is raised if no client id is specified.'''

        self._test_generate_template_error("client_id", None)

    def test_generate_nouserid(self):
        '''This test case ensures an exception is raised if no user id is specified.'''

        token_desc = {"client_id": "sample-client"}

        self._test_generate_template_error("user_id", token_desc)

    def test_generate_noscopes(self):
        '''This test case ensures an exception is raised if no scopes are specified.'''

        token_desc = {"client_id": "sample-client",
                      "user_id": 123}

        for scopes in [None, ""]:
            token_desc["scopes"] = scopes

            self._test_generate_template_error("scopes", token_desc)

    def test_generate_noexpiresin(self):
        '''This test case ensures an exception is raised if no expires_in is specified.'''

        token_desc = {"client_id": "sample-client",
                      "user_id": 123,
                      "scopes": "scope1 scope2"}

        self._test_generate_template_error("expires_in", token_desc)

    def _test_generate_template_error(self, attr_name, token_desc):
        '''This method provides a sample method for testing various generate exception cases caused by missing keys from token
        descriptor.'''

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            self._generator.generate(token_desc)

        self.assertEqual(attr_name, ctx.exception.attr_name)

    def test_generate_client_revoked(self):
        '''This test case ensures a token can not be generated for a client which is revoked.'''

        client_id = str(uuid.uuid4())

        token_desc = {"client_id": client_id,
                      "user_id": 1,
                      "scopes": "scope1 scope2",
                      "expires_in": 3600}

        expected_client = Client(client_id, name="simple app", revoked=True)

        self._mock_client_search(expected_client)

        with self.assertRaises(OAuth2InvalidClientError):
            self._generator.generate(token_desc)

        self._model_facade.find_by_pk.assert_called_once_with({Client.client_id: client_id})

    def test_generate_client_notfound(self):
        '''This test case ensures an exception is raised if the client specified in descriptor is not found.'''

        client_id = str(uuid.uuid4())

        token_desc = {"client_id": client_id,
                      "user_id": 1,
                      "scopes": "scope1 scope2",
                      "expires_in": 3600}

        self._mock_client_search(None)

        with self.assertRaises(OAuth2InvalidClientError):
            self._generator.generate(token_desc)

        self._model_facade.find_by_pk.assert_called_once_with({Client.client_id: client_id})

    def test_generate_client_invalidscopes(self):
        '''This test case ensures an exception is raised if the client is not allowed to used requested scopes.'''

        client_id = str(uuid.uuid4())

        token_desc = {"client_id": client_id,
                      "user_id": 1,
                      "scopes": "scope1 scope2",
                      "expires_in": 3600}

        expected_client = Client(client_id, name="simple app", revoked=False)
        expected_client.scopes = []

        self._mock_client_search(expected_client)

        with self.assertRaises(OAuth2InvalidScopesError):
            self._generator.generate(token_desc)

        self._model_facade.find_by_pk.assert_called_once_with({Client.client_id: client_id})

    def _mock_client_search(self, expected_client):
        '''This method provides the mock for client search by client_id. It returns a mock model facade which returns
        expected_client when invoked.'''

        if expected_client:
            self._model_facade.find_by_pk = Mock(return_value=expected_client)
        else:
            self._model_facade.find_by_pk = Mock(side_effect=FantasticoDbNotFoundError("Client not found."))

    def test_validate_ok(self):
        '''This test case ensures a valid token passes validation.'''

        creation_time = int(time.time())
        expiration_time = creation_time + 3600

        token = Token({"client_id": "sample-app",
                       "type": "access",
                       "user_id": 1,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        expected_client = Client(client_id=token.client_id, revoked=False)
        self._mock_client_search(expected_client)

        self.assertTrue(self._generator.validate(token))

    def test_validate_invalidtype(self):
        '''This test case ensures an exception is raised when the token type is not compatible with generator.'''

        creation_time = int(time.time())
        expiration_time = creation_time + 3600

        token = Token({"client_id": "sample-app",
                       "type": "unknown",
                       "user_id": 1,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        with self.assertRaises(OAuth2InvalidTokenTypeError) as ctx:
            self._generator.validate(token)

        self.assertEqual(token.type, ctx.exception.token_type)

    def test_validate_tokenexpired(self):
        '''This test case ensures an exception is raised if the token is expired.'''

        creation_time = int(time.time() - 7200)
        expiration_time = int(time.time() - 3600)

        token = Token({"client_id": "sample-app",
                       "type": "access",
                       "user_id": 1,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        with self.assertRaises(OAuth2TokenExpiredError):
            self._generator.validate(token)

    def test_validate_token_clientrevoked(self):
        '''This test case ensures an expection is raised if the token client is not valid.'''

        creation_time = int(time.time())
        expiration_time = creation_time + 3600

        token = Token({"client_id": "sample-app",
                       "type": "access",
                       "user_id": 1,
                       "creation_time": creation_time,
                       "expiration_time": expiration_time})

        expected_client = Client(client_id=token.client_id, revoked=True)
        self._mock_client_search(expected_client)

        with self.assertRaises(OAuth2InvalidClientError):
            self._generator.validate(token)
