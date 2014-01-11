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
.. py:module:: fantastico.oauth2_idp.models.tests.test_user_validator
'''
from fantastico.contrib.oauth2_idp.models.validators.user_validator import UserValidator
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils.dictionary_object import DictionaryObject

class UserValidatorTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for UserValidator.'''

    _validator = None

    def init(self):
        self._validator = UserValidator()

    def test_format_resource_ok(self):
        '''This test case ensures format_resource works correctly for an expected resource.'''

        desc = {"username": "abcd", "password": "1234567"}
        resource = DictionaryObject(desc, immutable=False)

        self._validator.format_resource(resource, None)

        self.assertEqual(desc["username"], resource.username)
        self.assertTrue("password" not in desc)

    def test_format_resource_none_ok(self):
        '''This test case ensures validation works correctly for even when resource does not contain keys.'''

        desc = {}
        resource = DictionaryObject(desc, immutable=False)

        self._validator.format_resource(resource, None)

        self.assertEqual(desc, {})
