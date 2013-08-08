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
.. py:module:: fantastico.samples.mvc.mvc_hello
'''
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import ControllerProvider, Controller
from webob.response import Response
import json

@ControllerProvider()
class MvcHelloController(BaseController):
    '''This class provides some simple examples of how to write controllers based on Fantastico mvc.'''

    @Controller(url="/mvc/hello-world", method="GET",
                models={"FriendlyMessage": "fantastico.samples.mvc.models.friendly_message.MvcFriendlyMessage"})
    def say_hello(self, request):
        '''This method simple say hello world and wrap it into compatible response.'''

        message_model = request.models.FriendlyMessage

        msg = message_model.new_model(message="Hello world. It works like a charm.")

        msg_pk = message_model.create(msg)[0]

        msg_persisted = message_model.find_by_pk({message_model.model_cls.id: msg_pk})

        tpl = self.load_template(tpl_name="/say_hello.html", model_data={"hello_msg": msg_persisted.message})

        response = Response(tpl, content_type="text/html")

        message_model.delete(msg)

        return response

    @Controller(url="/mvc/reuse-component")
    def reuse_comonent(self, request):
        '''This method is used to showcase component reusage.'''

        print(request.content_type)

        return Response(self.load_template("/reuse_component.html", model_data={"url_ex": "/simple/url"}))

    @Controller(url="/simple/url")
    def handle_simple_url(self, request):
        '''This method returns a simple json object for testing purposes.'''

        print(request.content_type)

        content = {"message": "Hello world", "inner_message": {"message": "inner_message"}}

        return Response(body=json.dumps(content), content_type="application/json")
