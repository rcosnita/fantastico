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
from fantastico.oauth2.accesstoken_generator import AccessTokenGenerator
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import time
from fantastico.oauth2.exceptions import OAuth2InvalidTokenDescriptorError

class AccessTokenGeneratorTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for access tokens generator.'''

    _generator = AccessTokenGenerator()

    def init(self):
        '''This method is invoked in order to set up common dependencies for every test case.'''

        self._generator = AccessTokenGenerator()

    def test_generate_ok(self):
        '''This test case ensures an access token can be correctly generated.'''

        creation_time = time.time()

        time_provider = Mock()
        time_provider.time = Mock(return_value=creation_time)

        token_desc = {"client_id": "my-sample-app",
                      "user_id": 123,
                      "scopes": "scope1 scope2 scope3 scope4",
                      "expires_in": 3600}

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
