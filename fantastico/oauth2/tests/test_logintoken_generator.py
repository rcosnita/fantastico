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
.. py:module:: fantastico.oauth2.tests.test_logintoken_generator
'''
from fantastico.oauth2.exceptions import OAuth2InvalidTokenDescriptorError, OAuth2InvalidTokenTypeError, OAuth2TokenExpiredError
from fantastico.oauth2.logintoken_generator import LoginTokenGenerator
from fantastico.oauth2.token import Token
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import time

class LoginTokenGeneratorTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for login token generator.'''

    _generator = None
    _db_conn = None

    def init(self):
        '''This method is invoked automatically in order to set common test cases dependencies.'''

        self._db_conn = Mock()

        self._generator = LoginTokenGenerator(self._db_conn)

    def test_generate_ok(self):
        '''This test case ensures a login token can be correctly generated from a descriptor.'''

        creation_time = 1388002667

        token_desc = {"client_id": "test-client", "user_id": 1, "expires_in": 3600}

        time_provider = Mock()
        time_provider.time = Mock(return_value=creation_time)

        token = self._generator.generate(token_desc, time_provider)

        self.assertIsNotNone(token)
        self.assertEqual(token_desc["client_id"], token.client_id)
        self.assertEqual("login", token.type)
        self.assertEqual(token_desc["user_id"], token.user_id)
        self.assertEqual(creation_time, token.creation_time)
        self.assertEqual(creation_time + token_desc["expires_in"], token.expiration_time)

    def test_generate_missing_clientid(self):
        '''This test case ensures a login token can not be generated without client id.'''

        self._test_generate_missing_attribute_error(None, "client_id")

    def test_generate_missing_userid(self):
        '''This test case ensures a login token can not be generated without user_id.'''

        token_desc = {"client_id": "test-idp"}

        self._test_generate_missing_attribute_error(token_desc, "user_id")

    def test_generate_missing_expiresin(self):
        '''This test case ensures a login token can not be generated without expires_in.'''

        token_desc = {"client_id": "test-idp", "user_id": 1}

        self._test_generate_missing_attribute_error(token_desc, "expires_in")

    def _test_generate_missing_attribute_error(self, token_desc, attr_name):
        '''This method provides a template for testing generate missing attribute from token descriptor.'''

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            self._generator.generate(token_desc)

        self.assertEqual(attr_name, ctx.exception.attr_name)

    def test_validate_token_ok(self):
        '''This test case ensures a valid token does not throw an exception.'''

        creation_time = time.time()
        expiration_time = int(creation_time + 300)

        token = Token({"client_id": "test-idp",
                       "type": LoginTokenGenerator.TOKEN_TYPE,
                       "user_id": 1,
                       "creation_time": int(creation_time),
                       "expiration_time": expiration_time})

        self.assertTrue(self._generator.validate(token))

    def test_validate_token_invalidtype(self):
        '''This test case ensures a token with a different type than login can not be validated by login token generator.'''

        creation_time = time.time()
        expiration_time = int(creation_time + 300)

        token = Token({"client_id": "test-idp",
                       "type": "Unknown",
                       "user_id": 1,
                       "creation_time": int(creation_time),
                       "expiration_time": expiration_time})

        with self.assertRaises(OAuth2InvalidTokenTypeError) as ctx:
            self._generator.validate(token)

        self.assertEqual(token.type, ctx.exception.token_type)

    def test_validate_token_expired(self):
        '''This test case ensures a token which is expired fails validation of login token generator.'''

        creation_time = int(time.time() - 7200)
        expiration_time = int(creation_time - 300)

        token = Token({"client_id": "test-idp",
                       "type": LoginTokenGenerator.TOKEN_TYPE,
                       "user_id": 1,
                       "creation_time": int(creation_time),
                       "expiration_time": expiration_time})

        self.assertRaises(OAuth2TokenExpiredError, lambda: self._generator.validate(token))
