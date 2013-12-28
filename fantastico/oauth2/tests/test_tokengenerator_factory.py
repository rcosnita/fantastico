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
.. py:module:: fantastico.oauth2.tests.test_tokengenerator_factory
'''
from fantastico.oauth2.exceptions import OAuth2InvalidTokenTypeError
from fantastico.oauth2.logintoken_generator import LoginTokenGenerator
from fantastico.oauth2.tokengenerator_factory import TokenGeneratorFactory
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from fantastico.oauth2.accesstoken_generator import AccessTokenGenerator

class TokenGeneratoryFactoryTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for token generator factory.'''

    _factory = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies for test cases.'''

        self._factory = TokenGeneratorFactory()

    def test_logintokengenerator_get(self):
        '''This test case ensures the tokens generator factory can correctly instantiate a login token generator.'''

        login_generator = self._factory.get_generator(TokenGeneratorFactory.LOGIN_TOKEN, Mock())
        access_generator = self._factory.get_generator(TokenGeneratorFactory.ACCESS_TOKEN, Mock())

        self.assertIsNotNone(login_generator)
        self.assertIsNotNone(access_generator)
        self.assertIsInstance(login_generator, LoginTokenGenerator)
        self.assertIsInstance(access_generator, AccessTokenGenerator)

    def test_unknonwgenerator_get_exception(self):
        '''This test case ensures a concrete exception is raised if the requested token generator is not supported.'''

        with self.assertRaises(OAuth2InvalidTokenTypeError) as ctx:
            self._factory.get_generator("Unknown", Mock())

        self.assertEqual("Unknown", ctx.exception.token_type)
