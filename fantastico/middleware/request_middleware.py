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

.. py:module:: fantastico.middleware.request_response
'''
from fantastico import mvc
from fantastico.locale.language import Language
from fantastico.middleware.request_context import RequestContext
from fantastico.routing_engine.custom_responses import RedirectResponse
from fantastico.settings import SettingsFacade
from webob.request import Request
import uuid

class RequestMiddleware(object):
    '''This class provides the middleware responsible for converting wsgi environ dictionary into a request. The result is saved
    into current WSGI environ under key **fantastico.request**. In addition each new request receives an identifier. If subsequent
    requests are triggered from that request then they will also receive the same request id.'''

    def __init__(self, app):
        self._app = app

    def _build_context(self, request):
        '''Method used to build the context object starting for a request.'''

        client_langs = request.accept_language

        settings_facade = SettingsFacade(request.environ)
        supported_langs = settings_facade.get("supported_languages")

        if hasattr(client_langs, "_parsed"):
            client_langs = client_langs._parsed
        else:
            client_langs = []

        context = RequestContext(settings_facade, self._get_supported_lang(supported_langs, client_langs))

        request.context = context

    def _get_supported_lang(self, supported_languages, client_languages):
        '''Method used to detect supported language by intersected the supported languages configured with the languages
        requested by user.'''

        for lang in client_languages:
            lang_code = lang[0].lower().replace("-", "_")

            for lang_supported in supported_languages:
                if lang_code == lang_supported:
                    return Language(lang_code)

                if(lang_supported.startswith(lang_code)):
                    return Language(lang_supported)

        return Language(supported_languages[0])

    def _redirect(self, destination, query_params=None):
        '''This method is used to build a redirect response base on the given arguments.'''

        return RedirectResponse(destination=destination, query_params=query_params)

    def __call__(self, environ, start_response, uuid_generator=uuid.uuid4):
        request = Request(environ)
        self._build_context(request)

        request.request_id = environ.get("fantastico.current_request_id")

        if not request.request_id:
            request.request_id = uuid_generator()

        request.redirect = self._redirect

        environ["fantastico.current_request_id"] = request.request_id
        environ["fantastico.request"] = request

        try:
            return self._app(environ, start_response)
        finally:
            if mvc.CONN_MANAGER:
                mvc.CONN_MANAGER.close_connection(request.request_id)
