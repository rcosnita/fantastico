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
.. py:module:: fantastico.oauth2.grant_handler
'''

from abc import abstractmethod, ABCMeta # pylint: disable=W0611
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError

class GrantHandler(object, metaclass=ABCMeta):
    '''This class provides the abstract contract of a handler. Each concrete handler must implement this contract in order to
    correctly extend Fantastico OAuth2 supported handlers.'''

    def __init__(self, tokens_service, settings_facade):
        self._tokens_service = tokens_service
        self._settings_facade = settings_facade

    @abstractmethod
    def handle_grant(self, request):
        '''This method must be overriden in order to correctly implement grant logic. It receives the current http request
        and return a http response.'''

    def _validate_missing_param(self, request, param_name):
        '''This method tries to obtain the param_name from the current request. If parameter is not found an
        oauth2 exception is raised.'''

        value = request.params.get(param_name)
        if not value:
            raise OAuth2MissingQueryParamError(param_name)

        return value
