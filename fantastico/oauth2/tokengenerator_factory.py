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
.. py:module:: fantastico.oauth2.tokengenerator_factory
'''
from fantastico.oauth2.accesstoken_generator import AccessTokenGenerator
from fantastico.oauth2.exceptions import OAuth2InvalidTokenTypeError
from fantastico.oauth2.logintoken_generator import LoginTokenGenerator

class TokenGeneratorFactory(object):
    '''This class provides the entry point for working with generators. It provides a factory for easily instantiating a generator
    which can work with a request token type.

    .. code-block:: python

        login_generator = TokenGeneratorFactory().get_generator(TokenGeneratorFactory.LOGIN_TOKEN)'''

    ACCESS_TOKEN = AccessTokenGenerator.TOKEN_TYPE
    LOGIN_TOKEN = LoginTokenGenerator.TOKEN_TYPE

    def __init__(self):
        self._supported_generators = {self.ACCESS_TOKEN: AccessTokenGenerator,
                                      self.LOGIN_TOKEN: LoginTokenGenerator}

    def get_generator(self, token_type, db_conn):
        '''This method returns an instance of a token generator which can handel requested token type.

        :param token_type: A unique token type.
        :type token_type: string
        :param db_conn: An existing database connection (sql alchemy object) used when working with client context.
        :return: An instance of a concrete token generator which is compatible with the request token type.
        :rtype: :py:class:`fantastico.oauth2.token_generator.TokenGenerator`
        '''

        generator_cls = self._supported_generators.get(token_type)

        if not generator_cls:
            raise OAuth2InvalidTokenTypeError(token_type, "%s token type is not supported." % token_type)

        return generator_cls(db_conn)
