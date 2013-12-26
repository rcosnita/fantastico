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
.. py:module:: fantastico.oauth2.tests.test_aes_tokenencryption
'''
from Crypto import Random
from Crypto.Cipher import AES
from fantastico.oauth2.exceptions import OAuth2InvalidTokenDescriptorError, OAuth2TokenEncryptionError
from fantastico.oauth2.token import Token
from fantastico.oauth2.token_encryption import AesTokenEncryption
from fantastico.tests.base_case import FantasticoUnitTestsCase

class AesTokenEncryptionTests(FantasticoUnitTestsCase):
    '''This class provides tests suite for AES token encryption provider from fantastico.'''

    _aes_iv = None

    def init(self):
        '''This method is invoked automatically in order to initialize common test cases dependencies.'''

        self._aes_iv = Random.new().read(AES.block_size)

    def test_aes_ok(self):
        '''This test case ensures token encryption correctly supports AES-128 algorithm.'''

        aes_provider = AesTokenEncryption()

        for key_length in [16, 24, 32]:
            token_key = Random.new().read(key_length)

            token = Token({"client_id": "test client",
                           "attr1": "test"})

            token_encrypted = aes_provider.encrypt_token(token, self._aes_iv, token_key)
            token_decrypted = aes_provider.decrypt_token(token_encrypted, self._aes_iv, token_key)

            self.assertIsNotNone(token_decrypted)
            self.assertEqual(token.client_id, token_decrypted.client_id)
            self.assertEqual(token.attr1, token_decrypted.attr1)

    def test_aes_encrypt_notoken(self):
        '''This test case ensures aes encrypt fails if no token is given.'''

        aes_provider = AesTokenEncryption()

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            aes_provider.encrypt_token(None, None, None)

        self.assertEqual("token", ctx.exception.attr_name)

    def test_aes_encrypt_notokeniv(self):
        '''This test case ensures aes encrypt fails if no token_iv is given.'''

        aes_provider = AesTokenEncryption()

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            aes_provider.encrypt_token(Token({}), None, None)

        self.assertEqual("token_iv", ctx.exception.attr_name)

    def test_aes_encrypt_notokenkey(self):
        '''This test case ensures aes encrypt fails if no token_key is given.'''

        aes_provider = AesTokenEncryption()

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            aes_provider.encrypt_token(Token({}), "simple key", None)

        self.assertEqual("token_key", ctx.exception.attr_name)

    def test_aes_encrypt_unexpected_error(self):
        '''This test case ensures all unexpected exceptions from encrypt are converted correctly into OAuth2 encryption errors.'''

        aes_provider = AesTokenEncryption()

        with self.assertRaises(OAuth2TokenEncryptionError):
            aes_provider.encrypt_token(Token({}), "Simple IV", "Simple Key")

    def test_aes_decrypt_notoken(self):
        '''This test case ensures aes decrypt fails if no token is given.'''

        aes_provider = AesTokenEncryption()

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            aes_provider.decrypt_token(None, None, None)

        self.assertEqual("encrypted_str", ctx.exception.attr_name)

    def test_aes_descrypt_notokeniv(self):
        '''This test case ensures aes decrypt fails if no token iv is given.'''

        aes_provider = AesTokenEncryption()

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            aes_provider.decrypt_token(Token({}), None, None)

        self.assertEqual("token_iv", ctx.exception.attr_name)

    def test_aes_decrypt_notokenkey(self):
        '''This test case ensures aes decrypt fails if no token_key is given.'''

        aes_provider = AesTokenEncryption()

        with self.assertRaises(OAuth2InvalidTokenDescriptorError) as ctx:
            aes_provider.decrypt_token(Token({}), "simple key", None)

        self.assertEqual("token_key", ctx.exception.attr_name)

    def test_aes_decrypt_unexpected_error(self):
        '''This test case ensures all unexpected exceptions from decrypt are converted correctly into OAuth2 encryption errors.'''

        aes_provider = AesTokenEncryption()

        with self.assertRaises(OAuth2TokenEncryptionError):
            aes_provider.decrypt_token(Token({}), "Simple IV", "Simple Key")
