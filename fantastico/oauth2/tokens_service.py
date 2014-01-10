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
.. py:module:: fantastico.oauth2.tokens_service
'''
from fantastico.oauth2.exceptions import OAuth2InvalidTokenTypeError, OAuth2Error, OAuth2InvalidClientError
from fantastico.oauth2.models.client_repository import ClientRepository
from fantastico.oauth2.token_encryption import PublicTokenEncryption, AesTokenEncryption
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
import base64

class TokensService(object):
    '''This class provides an abstraction for working with all supported token types. Internally it uses
    :py:class:`fantastico.oauth2.tokengenerator_factory.TokenGeneratorFactory` for obtaining a correct token generator. Then,
    it delegates all calls to that token generator.'''

    def __init__(self, db_conn, factory_cls=TokenGeneratorFactory, client_repo_cls=ClientRepository,
                 encryptor_cls=PublicTokenEncryption):
        self._db_conn = db_conn
        self._tokens_factory = factory_cls()
        self._client_repo = client_repo_cls(self._db_conn)
        self._encryptor = encryptor_cls(AesTokenEncryption())

    @property
    def db_conn(self):
        '''This property returns the database connection used by this token service.'''

        return self._db_conn

    def generate(self, token_desc, token_type):
        '''This method generates a concrete token from the given token descriptor. It uses token_type in order to choose the right
        token generator.

        .. code-block:: python

            # extract db_conn from one of your controller injected facade models.

            # generate a new access token
            tokens_service = TokensService(db_conn)

            token_desc = {"client_id": "sample-client",
                          "user_id": 123,
                          "scopes": "scope1 scope2 scope3",
                          "expires_in": 3600}
            access_token = tokens_service.generate(token_desc, TokenGeneratorFactory.ACCESS_TOKEN)'''

        try:
            generator = self._tokens_factory.get_generator(token_type, self._db_conn)

            token = generator.generate(token_desc)

            return token
        except OAuth2Error:
            raise
        except Exception as ex:
            raise OAuth2InvalidTokenTypeError(token_type, "An exception occured while generating token %s: %s" % \
                                              (token_type, str(ex)))

    def validate(self, token):
        '''This method validates a given token object. Internally, a generator is selected to validate the given token based on
        the given token type.

        .. code-block:: python

            # extract db_conn from one of your controller injected facade models.
            # extract token from request or instantiate a new token.

            tokens_service = TokensService(db_conn)
            tokens_service.validate(token)
        '''

        try:
            generator = self._tokens_factory.get_generator(token.type, self._db_conn)

            return generator.validate(token)
        except OAuth2Error:
            raise
        except Exception as ex:
            raise OAuth2InvalidTokenTypeError(token.type, "Unable to validate token: %s" % str(ex))

    def invalidate(self, token):
        '''This method invalidates a given token object. For instance, authorization codes can be invalidated. In order to
        invalidate a token you can use the code snippet below:

        .. code-block:: python

            # extract db_conn from one of your controller injected facade models.
            # extract token from request or instantiate a new token.

            tokens_service = TokensService(db_conn)
            tokens_service.invalidate(token)
        '''

        try:
            generator = self._tokens_factory.get_generator(token.type, self._db_conn)

            generator.invalidate(token)
        except OAuth2Error:
            raise
        except Exception as ex:
            raise OAuth2InvalidTokenTypeError(token.type, "Unable to invalidate token: %s" % str(ex))

    def encrypt(self, token, client_id):
        '''This method encrypts a given token and returns the encrypted string representation. Client id is required in order
        to obtain the encryption keys.'''

        try:
            client = self._client_repo.load(client_id)
        except Exception as ex:
            raise OAuth2InvalidClientError("Client %s can not be loaded: %s" % (client_id, str(ex)))

        token_iv = base64.b64decode(client.token_iv.encode())
        token_key = base64.b64decode(client.token_key.encode())

        return self._encryptor.encrypt_token(token, token_iv, token_key)

    def decrypt(self, encrypted_str):
        '''This method decrypts a given string and returns a concrete token object.'''

        return self._encryptor.decrypt_token(encrypted_str, client_repo=self._client_repo)
