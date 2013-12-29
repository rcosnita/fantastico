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
.. py:module:: fantastico.contrib.idp.idp_controller
'''

from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import Controller, ControllerProvider
from webob.response import Response
import urllib

@ControllerProvider()
class IdpController(BaseController):
    '''This class provides the controller for all routes / APIs provided by oauth2 default Fantastico Identity Provider.'''

    def __init__(self, settings_facade):
        super(IdpController, self).__init__(settings_facade)

        self._idp_config = self._settings_facade.get("oauth2_idp")
        self._idp_client_id = self._idp_config["client_id"]
        self._login_tpl = self._idp_config["template"]

    @Controller(url="^/oauth/idp/ui/login$")
    def show_login(self, request):
        '''This method returns the login page for Fantastico.'''

        return_url = request.params.get("return_url")

        content = self.load_template(self._login_tpl,
                                     {"return_url": urllib.parse.quote(return_url)})

        return Response(content)

    @Controller(url="^/oauth/idp/login$", method="POST")
    def authenticate(self, request):
        '''This method receives a request to authenticate a user. It validates the username and password against a list of
        registered users.'''

        return Response("Authenticating user.")
