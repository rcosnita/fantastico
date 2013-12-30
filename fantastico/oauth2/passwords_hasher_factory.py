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
.. py:module:: fantastico.oauth2.passwords_hasher_factory
'''
from fantastico.oauth2.sha512salt_passwords_hasher import Sha512SaltPasswordsHasher
from fantastico.oauth2.exceptions import OAuth2TokenEncryptionError

class PasswordsHasherFactory(object):
    '''This class provides a factory used to obtain concrete password hasher providers. At the moment, the following
    hashers are supported:

        * SHA512_SALT'''

    SHA512_SALT = "sha512-salt"

    def __init__(self):
        self._supported_hashers = {self.SHA512_SALT: Sha512SaltPasswordsHasher}

    def get_hasher(self, hash_alg):
        '''This method obtains a concrete passwords hasher provider based on the requested hash algorithm. See the constants
        defined in this factory in order to find out supported algorithms.

        :param hash_alg: A string uniquely identifying desired hash algorithm.
        :type hash_alg: str
        :returns: A concrete passwords hasher provider.
        :rtype: :py:class:`fantastico.oauth2.passwords_hasher.PasswordsHasher`
        :raises fantastico.oauth2.exceptions.OAuth2TokenEncryptionError: In case the requested algorithm is not supported.
        '''

        hasher = self._supported_hashers.get(hash_alg)

        if not hasher:
            raise OAuth2TokenEncryptionError("Hashing algorithm %s is not supported." % hash_alg)

        return hasher()
