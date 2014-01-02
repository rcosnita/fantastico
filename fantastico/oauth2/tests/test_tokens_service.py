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
.. py:module:: fantastico.oauth2.tests.test_tokens_service.TokensService
'''
from fantastico.oauth2.exceptions import OAuth2Error, OAuth2InvalidTokenTypeError
from fantastico.oauth2.token import Token
from fantastico.oauth2.tokens_service import TokensService
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class TokensServiceTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for tokens service implementation.'''

    _tokens_service = None

    _tokens_generator = None
    _tokens_factory = None
    _db_conn = None

    def init(self):
        '''This method is invoked automatically in order to setup common dependencies for all test cases.'''

        self._db_conn = Mock()

        self._tokens_generator = Mock()
        self._tokens_factory = Mock()
        self._tokens_factory.get_generator = Mock(return_value=self._tokens_generator)

        factory_cls = Mock(return_value=self._tokens_factory)

        self._tokens_service = TokensService(self._db_conn, factory_cls)

        factory_cls.assert_called_once_with()

    def test_generate_ok(self):
        '''This test case ensures tokens service can generate a token starting from a given dictionary.'''

        token_type = "mock-type"
        token_desc = {"client_id": "abc",
                      "test_attr": 1}

        expected_token = Token(token_desc)

        self._tokens_generator.generate = Mock(return_value=expected_token)

        token = self._tokens_service.generate(token_desc, token_type)

        self.assertEqual(expected_token, token)

        self._tokens_factory.get_generator.assert_called_once_with(token_type, self._db_conn)
        self._tokens_generator.generate.assert_called_once_with(token_desc)

    def test_generate_factory_oauth2ex(self):
        '''This test case ensures all oauth2 exceptions raised from factory class are bubbled up.'''

        ex = OAuth2Error(error_code= -1)

        self._tokens_factory.get_generator = Mock(side_effect=ex)

        with self.assertRaises(OAuth2Error) as ctx:
            self._tokens_service.generate({}, "unknown")

        self.assertEqual(ex, ctx.exception)

    def test_generate_factory_ex(self):
        '''This test case ensures all unexpected exceptions are casted to oauth2 exceptions.'''

        ex = Exception("Unexpected exception.")

        self._tokens_factory.get_generator = Mock(side_effect=ex)

        with self.assertRaises(OAuth2InvalidTokenTypeError):
            self._tokens_service.generate({}, "unknown")

    def test_generate_generator_oauth2ex(self):
        '''This test case ensures generator oauth2 exceptions are bubbled up.'''

        token_type = "mock-type"
        token_desc = {"client_id": "abc",
                      "test_attr": 1}

        ex = OAuth2Error(error_code= -1)

        self._tokens_generator.generate = Mock(side_effect=ex)

        with self.assertRaises(OAuth2Error) as ctx:
            self._tokens_service.generate(token_desc, token_type)

        self.assertEqual(ex, ctx.exception)

    def test_generate_generator_ex(self):
        '''This test case ensures generator unexpected exceptions are casted to oauth2 exceptions.'''

        token_type = "mock-type"
        token_desc = {"client_id": "abc",
                      "test_attr": 1}

        ex = Exception("Unexpected exception.")

        self._tokens_generator.generate = Mock(side_effect=ex)

        with self.assertRaises(OAuth2InvalidTokenTypeError):
            self._tokens_service.generate(token_desc, token_type)

    def test_validate_ok(self):
        '''This test case ensures token validation works correctly for a given token.'''

        token_desc = {"client_id": "abc",
                      "type": "mock-type",
                      "attr": "test-attr"}
        token = Token(token_desc)

        self._tokens_generator.validate = Mock(return_value=True)

        self.assertTrue(self._tokens_service.validate(token))

        self._tokens_factory.get_generator.assert_called_once_with(token.type, self._db_conn)
        self._tokens_generator.validate.assert_called_once_with(token)

    def test_validate_factory_oauth2ex(self):
        '''This test case ensures factory oauth2 exceptions are bubbled up.'''

        token = Token({"type": "mock-type"})

        ex = OAuth2Error(error_code= -1)

        self._tokens_factory.get_generator = Mock(side_effect=ex)

        with self.assertRaises(OAuth2Error) as ctx:
            self._tokens_service.validate(token)

        self.assertEqual(ex, ctx.exception)

    def test_validate_factory_ex(self):
        '''This test case ensures factory unexpected errors are converted to oauth2 concrete exceptions.'''

        token = Token({"type": "mock-type"})

        ex = Exception("Unexpected exception.")

        self._tokens_factory.get_generator = Mock(side_effect=ex)

        with self.assertRaises(OAuth2InvalidTokenTypeError):
            self._tokens_service.validate(token)

    def test_validate_generator_oauth2ex(self):
        '''This test case ensures generator oauth2 exceptions are bubbled up.'''

        token = Token({"type": "mock-type"})

        ex = OAuth2Error(error_code= -1)

        self._tokens_generator.validate = Mock(side_effect=ex)

        with self.assertRaises(OAuth2Error) as ctx:
            self._tokens_service.validate(token)

        self.assertEqual(ex, ctx.exception)

    def test_validate_generator_ex(self):
        '''This test case ensures generator unexpected exceptions are converted to oauth2 concrete exceptions.'''

        token = Token({"type": "mock-type"})

        ex = Exception("Unexpected exception.")

        self._tokens_generator.validate = Mock(side_effect=ex)

        with self.assertRaises(OAuth2InvalidTokenTypeError):
            self._tokens_service.validate(token)

    def test_invalidate_ok(self):
        '''This test case ensures tokens can be invalidated successfully.'''

        token = Token({"type": "mock-type"})

        self._tokens_generator.invalidate = Mock()

        self.assertIsNone(self._tokens_service.invalidate(token))

        self._tokens_factory.get_generator.assert_called_once_with(token.type, self._db_conn)
        self._tokens_generator.invalidate.assert_called_once_with(token)

    def test_invalidate_factory_oauth2ex(self):
        '''This test case ensures factory oauth2 exceptions are bubbled up.'''

        token = Token({"type": "mock-type"})

        ex = OAuth2Error(error_code= -1)

        self._tokens_factory.get_generator = Mock(side_effect=ex)

        with self.assertRaises(OAuth2Error) as ctx:
            self._tokens_service.invalidate(token)

        self.assertEqual(ex, ctx.exception)

    def test_invalidate_factory_ex(self):
        '''This test case ensures factory unexpected exceptions are converted to oauth2 concrete exceptions.'''

        token = Token({"type": "mock-type"})

        ex = Exception("Unexpected exception.")

        self._tokens_factory.get_generator = Mock(side_effect=ex)

        with self.assertRaises(OAuth2InvalidTokenTypeError):
            self._tokens_service.invalidate(token)

    def test_invalidate_generator_oauth2ex(self):
        '''This test case ensures generator oauth2 exceptions are bubbled up.'''

        token = Token({"type": "mock-type"})

        ex = OAuth2Error(error_code= -1)

        self._tokens_generator.invalidate = Mock(side_effect=ex)

        with self.assertRaises(OAuth2Error) as ctx:
            self._tokens_service.invalidate(token)

        self.assertEqual(ex, ctx.exception)

    def test_invalidate_generator_ex(self):
        '''This test case ensures generator unexpected exceptions are converted to oauth2 concrete exceptions.'''

        token = Token({"type": "mock-type"})

        ex = Exception("Unexpected exception.")

        self._tokens_generator.invalidate = Mock(side_effect=ex)

        with self.assertRaises(OAuth2InvalidTokenTypeError):
            self._tokens_service.invalidate(token)
