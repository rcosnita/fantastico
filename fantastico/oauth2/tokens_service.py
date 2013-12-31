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
from fantastico.oauth2.exceptions import OAuth2InvalidTokenTypeError, OAuth2Error
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory

class TokensService(object):
    '''This class provides an abstraction for working with all supported token types. Internally it uses
    :py:class:`fantastico.oauth2.tokengenerator_factory.TokenGeneratorFactory` for obtaining a correct token generator. Then,
    it delegates all calls to that token generator.'''

    def __init__(self, db_conn, factory_cls=TokenGeneratorFactory):
        self._db_conn = db_conn
        self._tokens_factory = factory_cls()

    def generate(self, token_desc, token_type):
        '''This method generates a concrete token from the given token descriptor. It uses token_type in order to choose the right
        token generator.'''

        try:
            generator = self._tokens_factory.get_generator(token_type, self._db_conn)

            token = generator.generate(token_desc)

            return token
        except OAuth2Error:
            raise
        except Exception as ex:
            raise OAuth2InvalidTokenTypeError(token_type, "An exception occured while generating token %s: %s" % \
                                              (token_type, str(ex)))
