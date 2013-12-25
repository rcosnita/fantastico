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
.. py:module:: fantastico.oauth2.token_generator
'''
from abc import abstractmethod, ABCMeta # pylint: disable=W0611

class TokenGenerator(object, metaclass=ABCMeta):
    '''This class provides an abstract contract which must be provided by each concrete token generator. A token generator
    must provide the following functionality:

        * generate a new token
        * validate a given token
        * invalidate a given token'''

    @abstractmethod
    def generate(self, token_desc):
        '''This method must be overriden so that it builds a correct token from the given descriptor. Descriptor is a free
        form object.

        :param token_desc: A dictionary containing all keys required for generating a new token.
        :type token_desc: dict
        :return: A new token object.
        :rtype: :py:class:`fantastico.oauth2.token.Token`
        '''

    @abstractmethod
    def validate(self, token):
        '''This method must be overriden so that it validates the given token. Usually, if the token is not valid a concrete
        exception must be raised.

        :param token: The token object we want to validate.
        :type token: :py:class:`fantastico.oauth2.token.Token`
        '''

    def invalidate(self, token):
        '''This method must be overriden if the given token supports invalidation (e.g: authorization code). In many cases
        this is not necessary so this is a nop.'''

        pass
