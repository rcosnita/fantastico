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
.. py:module:: fantastico.oauth2.token_encryption
'''

from Crypto.Cipher import AES
from abc import abstractmethod, ABCMeta # pylint: disable=W0611
from fantastico.oauth2.exceptions import OAuth2InvalidTokenDescriptorError, OAuth2TokenEncryptionError
from fantastico.oauth2.token import Token
import json

class TokenEncryption(object, metaclass=ABCMeta):
    '''This class provides an abstract model for token encryption providers. A token encryption provider must be able
    to encrypt / decrypt a :py:class:`fantastico.oauth2.token.Token` objects.'''

    @abstractmethod
    def encrypt_token(self, token, token_iv, token_key):
        '''This method must be overriden by concrete providers in order to correctly transform a token object into an encrypted
        string.


        :param token: A token object we want to encrypt.
        :type token: :py:class:`fantastico.oauth2.token.Token`
        :param token_iv: Token initialization vector used in symmetric encryption. Most of the times this will have a fix 128 bits length.
        :type token_iv: byte[]
        :param token_key: Token key used in symmetric encryption. Based on the implementation the length might vary: 128 / 192 / 256 bits.
        :type token_key: byte[]
        :return: The encrypted representation of the token.
        :rtype: str'''

    @abstractmethod
    def decrypt_token(self, encrypted_str, token_iv, token_key):
        '''This method must be overriden by concrete providers in order to correctly transform an encrypted string into a token
        object.

        :param encrypted_str: Encrypted token representation.
        :type encrypted_str: str
        :param token_iv: Token initialization vector used in symmetric encryption. Most of the times this will have a fix 128 bits length.
        :type token_iv: byte[]
        :param token_key: Token key used in symmetric encryption. Based on the implementation the length might vary: 128 / 192 / 256 bits.
        :type token_key: byte[]
        :return: Decrypted token object.
        :rtype: :py:class:`fantastico.oauth2.token.Token`'''

class AesTokenEncryption(TokenEncryption):
    '''This class provides a generic AES token encryption provider. It allows developers to specify the number of bits used
    for AES (128 / 192 / 256 bits).'''

    def encrypt_token(self, token, token_iv, token_key):
        '''This method uses AES for encrypting the given token. Internally it transform the token into a JSON string and
        encrypt it using given token_iv and token_key.'''

        if not token:
            raise OAuth2InvalidTokenDescriptorError("token")

        if not token_iv:
            raise OAuth2InvalidTokenDescriptorError("token_iv")

        if not token_key:
            raise OAuth2InvalidTokenDescriptorError("token_key")

        try:
            text = json.dumps(token.dictionary)

            cipher = AES.new(token_key, AES.MODE_CFB, token_iv)

            return cipher.encrypt(text)
        except Exception as ex:
            raise OAuth2TokenEncryptionError(str(ex))

    def decrypt_token(self, encrypted_str, token_iv, token_key):
        '''This method uses AES for decrypting the given string. Internally, decrypted string is converted into a dictionary and
        then into a concrete token object.'''

        if not encrypted_str:
            raise OAuth2InvalidTokenDescriptorError("encrypted_str")

        if not token_iv:
            raise OAuth2InvalidTokenDescriptorError("token_iv")

        if not token_key:
            raise OAuth2InvalidTokenDescriptorError("token_key")

        try:
            cipher = AES.new(token_key, AES.MODE_CFB, token_iv)

            decrypted_text = cipher.decrypt(encrypted_str).decode()
            token_descriptor = json.loads(decrypted_text)

            return Token(token_descriptor)
        except Exception as ex:
            raise OAuth2TokenEncryptionError(str(ex))
