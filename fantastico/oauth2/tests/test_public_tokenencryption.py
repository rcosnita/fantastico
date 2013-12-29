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
.. py:module:: fantastico.oauth2.tests.test_public_tokenencryption
'''
from fantastico.oauth2.token import Token
from fantastico.oauth2.token_encryption import PublicTokenEncryption
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import base64
import json

class PublicTokenEncryptionTests(FantasticoUnitTestsCase):
    '''This class provides tests suite for public token encryption algorithm.'''

    _symmetric_encryptor = None
    _public_encryptor = None

    _token_iv = None
    _token_key = None

    def init(self):
        '''This method is invoked automatically in order to setup common dependencies for all test cases.'''

        self._symmetric_encryptor = Mock()
        self._public_encryptor = PublicTokenEncryption(self._symmetric_encryptor)
        self._token_iv = Mock()
        self._token_key = Mock()

    def test_encrypt_token_ok(self):
        '''This test case ensures a given token object can be correctly encrypted by public token encryption.'''

        token = Token({"client_id": 123,
              "type": "access",
              "attr1": "cool-attr"})

        self._symmetric_encryptor.encrypt_token = Mock(return_value="test")

        encrypted_str = self._public_encryptor.encrypt_token(token, self._token_iv, self._token_key)

        self.assertIsNotNone(encrypted_str)

        encrypted_str = base64.b64decode(encrypted_str.encode())

        public_token = json.loads(encrypted_str.decode())

        self.assertIsNotNone(public_token)
        self.assertEqual(token.client_id, public_token.get("client_id"))
        self.assertEqual(token.type, public_token.get("type"))
        self.assertEqual("test", public_token.get("encrypted"))

        self._symmetric_encryptor.encrypt_token.assert_called_once_with(token, self._token_iv, self._token_key)

    def test_decrypt_token_ok(self):
        '''This test case ensures a given token can be decrypted correctly by public token provider.'''

        encrypted_token_desc = {"client_id": "abc",
                                "type": "access",
                                "attr1": "attr test"}
        token_desc = {"client_id": "abc",
                      "type": "access",
                      "encrypted": "abc"}

        encrypted_str = base64.b64encode(json.dumps(token_desc).encode())
        encrypted_token = Token(encrypted_token_desc)

        self._symmetric_encryptor.decrypt_token = Mock(return_value=encrypted_token)

        token = self._public_encryptor.decrypt_token(encrypted_str.decode(), self._token_iv, self._token_key)

        self.assertIsNotNone(token)
        self.assertEqual(encrypted_token, token)

        self._symmetric_encryptor.decrypt_token.assert_called_once_with("abc", self._token_iv, self._token_key)
