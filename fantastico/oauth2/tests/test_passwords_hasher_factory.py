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
.. py:module:: fantastico.oauth2.tests.test_passwords_hasher_factory
'''
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.oauth2.sha512salt_passwords_hasher import Sha512SaltPasswordsHasher
from fantastico.oauth2.exceptions import OAuth2TokenEncryptionError

class PasswordsHasherFactoryTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite which ensures passwords hasher factory correct behavior.'''

    _factory = None

    def init(self):
        '''This method is invoked automatically in order to setup common dependencies for all test cases.'''

        self._factory = PasswordsHasherFactory()

    def test_sha512salt_get(self):
        '''This test case ensures sha512 with salt passwords hasher can be instantiated using the factory.'''

        sha512_hasher = PasswordsHasherFactory().get_hasher(PasswordsHasherFactory.SHA512_SALT)

        self.assertIsInstance(sha512_hasher, Sha512SaltPasswordsHasher)

    def test_unsupportedalg_get(self):
        '''This test case ensures a concrete exception is raised if the requested algorithm is not supported.'''

        with self.assertRaises(OAuth2TokenEncryptionError):
            self._factory.get_hasher("unknown algorithm")
