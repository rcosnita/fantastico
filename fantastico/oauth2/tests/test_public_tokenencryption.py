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
from fantastico.exceptions import FantasticoDbNotFoundError, FantasticoDbError
from fantastico.oauth2.exceptions import OAuth2InvalidTokenDescriptorError, OAuth2Error, OAuth2TokenEncryptionError, \
    OAuth2InvalidClientError
from fantastico.oauth2.models.clients import Client
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

    def test_encrypt_token_missingtoken(self):
        '''This test case ensures encrypt fails if no token is specified.'''

        self._test_encrypt_missing_arg("token", None, None, None)

    def test_encrypt_token_missingiv(self):
        '''This test case ensures encrypt fails if no token_iv is specified.'''

        self._test_encrypt_missing_arg("token_iv", Mock(), None, None)

    def test_encrypt_token_missingkey(self):
        '''This test case ensures encrypt fails if no token_key is specified.'''

        self._test_encrypt_missing_arg("token_key", Mock(), Mock(), None)

    def _test_encrypt_missing_arg(self, attr_name, token, token_iv, token_key):
        '''This method provides a template for testing encrypt_token with various arguments. It automatically assert
        for invalid token descriptor exception being raised.'''

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            self._public_encryptor.encrypt_token(token, token_iv, token_key)

        self.assertEqual(attr_name, ctx.exception.attr_name)

    def test_encrypt_token_symmetric_oauth2ex(self):
        '''This test case ensures all oauth2 concrete exceptions raised during symmetric encryption are bubbled up.'''

        token = Token({})

        ex = OAuth2Error(error_code= -1, msg="Simple msg.", http_code=403)

        self._symmetric_encryptor.encrypt_token = Mock(side_effect=ex)

        with self.assertRaises(OAuth2Error) as ctx:
            self._public_encryptor.encrypt_token(token, self._token_iv, self._token_key)

        self.assertEqual(ex, ctx.exception)

    def test_encrypt_token_symmetric_ex(self):
        '''This test case ensures all unexpected exception raised by symmetric encryptor are not bubbled up.'''

        token = Token({})

        ex = Exception("Unexpected error.")

        self._symmetric_encryptor.encrypt_token = Mock(side_effect=ex)

        with self.assertRaises(OAuth2TokenEncryptionError):
            self._public_encryptor.encrypt_token(token, self._token_iv, self._token_key)

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

    def test_decrypt_token_missingdesc(self):
        '''This test case ensures a given token can not be decrypted by public token provider if it's null or empty.'''

        for encrypted_str in [None, "", "     "]:
            with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
                self._public_encryptor.decrypt_token(encrypted_str, self._token_iv, self._token_key)

            self.assertEqual("encrypted_str", ctx.exception.attr_name)

    def test_decrypt_token_noaesargs(self):
        '''This test case ensures a given token can be decrypted even though aes iv and key arguments are None. They are lazy
        obtained from client descriptor persisted into database.'''

        from fantastico.oauth2.models.return_urls import ClientReturnUrl

        token_iv = "token iv".encode()
        token_key = "token key".encode()

        client = Client(client_id="abcd", token_iv=base64.b64encode(token_iv),
                        token_key=base64.b64encode(token_key))

        public_desc = {"client_id": "abcd",
                       "type": "access",
                       "encrypted": "abc"}

        encrypted_desc = {"client_id": "abcd",
                          "type": "access",
                          "attr1": "test attr"}

        encrypted_token = Token(encrypted_desc)

        encrypted_str = base64.b64encode(json.dumps(public_desc).encode()).decode()

        model_facade = Mock()
        model_facade_cls = Mock(return_value=model_facade)

        model_facade.find_by_pk = Mock(return_value=client)

        self._symmetric_encryptor.decrypt_token = Mock(return_value=encrypted_token)

        token = self._public_encryptor.decrypt_token(encrypted_str, model_facade=model_facade_cls)

        self.assertEqual(encrypted_token, token)

        model_facade_cls.assert_called_once_with(Client)
        model_facade.find_by_pk.assert_called_once_with({Client.client_id: public_desc["client_id"]})

        self._symmetric_encryptor.decrypt_token.assert_called_once_with(public_desc["encrypted"], token_iv, token_key)

    def test_decrypt_token_invalidclient(self):
        '''This test case ensures a concrete exception is raised if the client id from public token is not found.'''

        from fantastico.oauth2.models.return_urls import ClientReturnUrl

        token_iv = "token iv".encode()
        token_key = "token key".encode()

        client = Client(client_id="abcd", token_iv=base64.b64encode(token_iv),
                        token_key=base64.b64encode(token_key))

        public_desc = {"client_id": "abcd",
                       "type": "access",
                       "encrypted": "abc"}

        encrypted_str = base64.b64encode(json.dumps(public_desc).encode()).decode()

        model_facade = Mock()
        model_facade_cls = Mock(return_value=model_facade)

        ex = FantasticoDbNotFoundError("Unexpected client %s" % client.client_id)

        model_facade.find_by_pk = Mock(side_effect=ex)

        with self.assertRaises(OAuth2InvalidClientError):
            self._public_encryptor.decrypt_token(encrypted_str, model_facade=model_facade_cls)

        model_facade_cls.assert_called_once_with(Client)
        model_facade.find_by_pk.assert_called_once_with({Client.client_id: public_desc["client_id"]})

    def test_decrypt_token_dberror(self):
        '''This test case ensures an oauth2 exception is raised if client descriptor search fails.'''

        from fantastico.oauth2.models.return_urls import ClientReturnUrl

        token_iv = "token iv".encode()
        token_key = "token key".encode()

        client = Client(client_id="abcd", token_iv=base64.b64encode(token_iv),
                        token_key=base64.b64encode(token_key))

        public_desc = {"client_id": "abcd",
                       "type": "access",
                       "encrypted": "abc"}

        encrypted_str = base64.b64encode(json.dumps(public_desc).encode()).decode()

        model_facade = Mock()
        model_facade_cls = Mock(return_value=model_facade)

        ex = FantasticoDbError("Unexpected client %s" % client.client_id)

        model_facade.find_by_pk = Mock(side_effect=ex)

        with self.assertRaises(OAuth2InvalidClientError):
            self._public_encryptor.decrypt_token(encrypted_str, model_facade=model_facade_cls)

        model_facade_cls.assert_called_once_with(Client)
        model_facade.find_by_pk.assert_called_once_with({Client.client_id: public_desc["client_id"]})

    def test_decrypt_symmetric_oauth2ex(self):
        '''This test case ensures all oauth2 exception caused by symmetric provider are bubbled up.'''

        public_token_desc = {"client_id": "abc",
                             "type": "access",
                             "encrypted": "long encrypted token"}

        encrypted_str = base64.b64encode(json.dumps(public_token_desc).encode()).decode()

        ex = OAuth2Error(error_code= -1, msg="Unexpected error")
        self._symmetric_encryptor.decrypt_token = Mock(side_effect=ex)

        with self.assertRaises(OAuth2Error) as ctx:
            self._public_encryptor.decrypt_token(encrypted_str, self._token_iv, self._token_key)

        self.assertEqual(ex, ctx.exception)

        self._symmetric_encryptor.decrypt_token.assert_called_once_with(public_token_desc["encrypted"], self._token_iv,
                                                                        self._token_key)

    def test_decrypt_symmetric_ex(self):
        '''This test case ensures all unexpected exceptions (non oauth2) raised by symmetric encryptor are correctly converted
        to concrete oauth2 exceptions.'''

        public_token_desc = {"client_id": "abc",
                             "type": "access",
                             "encrypted": "long encrypted token"}

        encrypted_str = base64.b64encode(json.dumps(public_token_desc).encode()).decode()

        ex = Exception("Unexpected exception.")
        self._symmetric_encryptor.decrypt_token = Mock(side_effect=ex)

        with self.assertRaises(OAuth2TokenEncryptionError):
            self._public_encryptor.decrypt_token(encrypted_str, self._token_iv, self._token_key)

        self._symmetric_encryptor.decrypt_token.assert_called_once_with(public_token_desc["encrypted"], self._token_iv,
                                                                        self._token_key)
