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
.. py:module:: fantastico.oauth2.logintoken_generator
'''
from fantastico.oauth2.exceptions import OAuth2InvalidTokenTypeError, OAuth2TokenExpiredError
from fantastico.oauth2.token import Token
from fantastico.oauth2.token_generator import TokenGenerator
import time

class LoginTokenGenerator(TokenGenerator):
    '''This class provides support for generating and working with login tokens. A login token is used for proving that a user
    is authenticated correctly. For more information, read :doc:`/features/oauth2/tokens_format`.'''

    TOKEN_TYPE = "login"

    def generate(self, token_desc, time_provider=time):
        '''This method generates a login token. In order to succeed token descriptor must contain the following keys:

            * client_id - a unique identifier for the idp which generated the token.
            * user_id - idp user unique identifier.
            * expires_in - an integer value in seconds determining the maximum validity of the token.

        If any of the above keys are missing an oauth 2 exception is raised.
        '''

        token_desc = token_desc or {}

        client_id = self._validate_missing_attr("client_id", token_desc)
        user_id = self._validate_missing_attr("user_id", token_desc)

        creation_time = int(time_provider.time())

        expires_in = self._validate_missing_attr("expires_in", token_desc)

        expiration_time = creation_time + expires_in

        token = {"client_id": client_id,
                 "type": self.TOKEN_TYPE,
                 "user_id": user_id,
                 "creation_time": creation_time,
                 "expiration_time": expiration_time}

        return Token(token)

    def validate(self, token):
        '''This method checks the given login token for:

            * correct type (login).
            * expiration time.
        '''

        if token.type != self.TOKEN_TYPE:
            raise OAuth2InvalidTokenTypeError(token.type, "Login token generator does not support %s tokens." % token.type)

        if token.expiration_time < time.time():
            raise OAuth2TokenExpiredError("Token is expired.")

        return True
