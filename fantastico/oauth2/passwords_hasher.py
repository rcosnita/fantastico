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
.. py:module:: fantastico.oauth2.passwords_hasher
'''

from abc import ABCMeta # pylint: disable=W0611
from abc import abstractmethod

class PasswordsHasher(object, metaclass=ABCMeta):
    '''This class provides an abstract contract for password hasher. A password hasher is an algorithm that generates a strong
    hash starting from a plain text string.'''

    @abstractmethod
    def hash_password(self, plain_passwd, hash_ctx=None):
        '''This method must be overriden in order to provide concrete hashing algorithm.

        :param plain_passwd: The plain password for which we want to obtain a strong hash.
        :type plain_passwd: str
        :param hash_ctx: An optional hashing context which contains additional attributes required by hashing algorithm. E.g: sha512 with salt.
        :type hash_ctx: :py:class:`fantastico.utils.dictionary_object.DictionaryObject`
        :returns: The strong hash generated.
        :rtype: str
        '''
