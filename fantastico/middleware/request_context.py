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

.. py:module:: fantastico.middleware.request_context
'''

class RequestContext(object):
    '''This class holds various attributes useful giving a context to an http request. Among other things we need
    to be able to access current language, current session and possible current user profile.'''

    def __init__(self, settings, language):
        '''
        :param language: The language associated with the current request.
        :type language: fantastico.locale.language.Language
        :param settings: The current settings facade that can be used to obtain items from framework configuration.
        :type settings: fantastico.settings.SettingsFacade
        '''

        self._settings = settings
        self._language = language
        self._wsgi_app = None

    @property
    def settings(self):
        '''Property that holds the current settings facade used for accessing fantastico configuration.'''

        return self._settings

    @property
    def language(self):
        '''Property that holds the current language that must be used during this request.'''

        return self._language

    @property
    def wsgi_app(self):
        '''Property that holds the WSGI application instance under which the request is handled.'''

        return self._wsgi_app

    @wsgi_app.setter
    def wsgi_app(self, value):
        '''Setter property used to set wsgi application under which the current request is handled.'''

        self._wsgi_app = value
