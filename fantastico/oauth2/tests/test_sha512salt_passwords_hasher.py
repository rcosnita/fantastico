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
.. py:module:: fantastico.oauth2.tests.test_sha512salt_passwords_hasher
'''
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.oauth2.sha512salt_passwords_hasher import Sha512SaltPasswordsHasher
from fantastico.utils.dictionary_object import DictionaryObject
from fantastico.oauth2.exceptions import OAuth2TokenEncryptionError

class Sha512SaltPasswordsHasherTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for sha512 with salt hashing provider.'''

    _hasher = None

    def init(self):
        '''This method is invoked automatically in order to setup common dependencies for all test cases.'''

        self._hasher = Sha512SaltPasswordsHasher()

    def test_hash_ok(self):
        '''This test case ensures a base64 encoded hash is return correctly by password hasher.'''

        plain_passwd = "abc123test"
        hash_ctx = DictionaryObject({"salt": 123})
        expected_result = "MzYxZTA5NTk2ZmVjNzZlMzc0MGZiY2I1YTc3NGM2YjM4OTBkMDFlNDEwYzQ5ZDdkNzAwM2IyNWJkZTUxOWE4MTAyMDM5Mzg1YTI4NDA0MmUxODNlN2JhMmNlZmM3NzU0NDQ2MTk5ZjhkYjQzZWEwMDE3MzhmODJmNDBmZWExM2M="

        result = self._hasher.hash_password(plain_passwd, hash_ctx)

        self.assertEqual(expected_result, result)

    def test_hash_none(self):
        '''This test case ensures that a hash is generated for empty or null passwords.'''

        hash_ctx = DictionaryObject({"salt": 123})
        expected_result = "M2M5OTA5YWZlYzI1MzU0ZDU1MWRhZTIxNTkwYmIyNmUzOGQ1M2YyMTczYjhkM2RjM2VlZTRjMDQ3ZTdhYjFjMWViOGI4NTEwM2UzYmU3YmE2MTNiMzFiYjVjOWMzNjIxNGRjOWYxNGE0MmZkN2EyZmRiODQ4NTZiY2E1YzQ0YzI="

        for plain_passwd in [None, "", "     "]:
            result = self._hasher.hash_password(plain_passwd, hash_ctx)

            self.assertEqual(expected_result, result)

    def test_hash_nocontext(self):
        '''This test case ensures an exception is raised if no hash context is given or if the context does not contain salt
        entry.'''

        for hash_ctx in [None, {}, {"unknown_attr": "sample value"}]:
            passwd = self._hasher.hash_password("123", DictionaryObject(hash_ctx))
            self.assertEqual(passwd, self._hasher.hash_password("123", DictionaryObject({"salt": 9999})))
