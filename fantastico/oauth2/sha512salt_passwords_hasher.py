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
.. py:module:: fantastico.oauth2.sha512salt_passwords_hasher
'''
from fantastico.oauth2.passwords_hasher import PasswordsHasher
import base64
import hashlib
from fantastico.utils.dictionary_object import DictionaryObject

class Sha512SaltPasswordsHasher(PasswordsHasher):
    '''This class provides the sha512salt implementation for password hashing. In addition, the result is encoded using base64.
    In order to use this hasher try the code snippet below:

    .. code-block:: python

        sha512_hasher = PasswordsHasherFactory().get_hasher(PasswordsHasherFactory.SHA512_SALT)
        hashed_passwd = sha512_hasher.hash_password("abcd", DictionaryObject({"salt": 123}))'''

    _DEFAULT_SALT = 9999

    def hash_password(self, plain_passwd, hash_ctx=None):
        '''This method provides the sha512 with salt algorithm for a given plain password. In addition, the hash is base64
        encoded.'''

        if not hash_ctx or not hash_ctx.dictionary.get("salt"):
            hash_ctx = DictionaryObject({"salt": self._DEFAULT_SALT})

        plain_passwd = (plain_passwd or "").strip()

        salt = hash_ctx.salt

        text = (plain_passwd + str(salt)).encode()

        hashed_text = hashlib.sha512(text).hexdigest()

        return base64.b64encode(hashed_text.encode()).decode()
