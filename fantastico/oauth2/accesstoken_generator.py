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
.. py:module:: fantastico.oauth2.accesstoken_generator
'''
from fantastico.oauth2.token import Token
from fantastico.oauth2.token_generator import TokenGenerator
import time
from fantastico.oauth2.exceptions import OAuth2InvalidTokenTypeError, OAuth2TokenExpiredError

class AccessTokenGenerator(TokenGenerator):
    '''This class provides the methods for working with access tokens: (generate and validate).'''

    TOKEN_TYPE = "access"

    def generate(self, token_desc, time_provider=time):
        '''This method generates a new access token starting from the givent token descriptor. In order to succeed the token
        descriptor must contain the following keys:

            * client_id - Client unique identifier.
            * user_id - User unique identifier.
            * scopes - The scopes requested for this client (a space delimited list of strings).
            * expires_in - The time to live period (in seconds) for the newly generated access token.
        '''

        token_desc = token_desc or {}

        client_id = self._validate_missing_attr("client_id", token_desc)
        user_id = self._validate_missing_attr("user_id", token_desc)
        scopes = self._validate_missing_attr("scopes", token_desc).split(" ")
        expires_in = self._validate_missing_attr("expires_in", token_desc)

        client = self._validate_client(client_id)
        self._validate_client_scopes(client.scopes, scopes)

        creation_time = time_provider.time()

        expiration_time = int(creation_time) + expires_in

        token = Token({"client_id": client_id,
                       "type": "access",
                       "user_id": user_id,
                       "scopes": scopes,
                       "creation_time": int(creation_time),
                       "expiration_time": expiration_time})

        return token

    def validate(self, token):
        '''This method validates a given access token. It checks for:

            * valid client id
            * valid token type
            * token not expired
        '''

        if self.TOKEN_TYPE != token.type:
            raise OAuth2InvalidTokenTypeError(token.type, "Token type %s not supported." % token.type)

        if token.expiration_time < time.time():
            raise OAuth2TokenExpiredError("Access token is expired.")

        self._validate_client(token.client_id)

        return True
