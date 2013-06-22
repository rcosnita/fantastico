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
.. py:module:: fantastico.routing_engine.custom_responses
'''
from fantastico.exceptions import FantasticoError
from webob.response import Response

class RedirectResponse(Response):
    '''This class encapsulates the logic for programatically redirecting client from a fantastico controller.
    
    .. code-block:: python
    
        @Controller(url="/redirect/example")
        def redirect_to_google(self, request):
            return request.redirect("http://www.google.ro/")
    
    There are some special cases when you would like to pass some query parameters to redirect destination. This is also easily
    achievable in Fantastico:
    
    .. code-block:: python
    
        @Controller(url="/redirect/example")
        def redirect_to_google(self, request):
            return request.redirect("http://www.google.ro/search", 
                                    query_params=[("q", "hello world")])
    
    The above example will redirect client browser to 
    `http://www.google.ro/search?q=hello world <http://www.google.ro/search?q=hello world>`_'''
    
    def __init__(self, destination, query_params=None):
        if destination is None or len(destination.strip()) == 0:
            raise FantasticoError("You can not build a redirect response without a valid destination.")
        
        self._destination = destination
        self._query_params = query_params or []
        
        self._build_destination()
        
        super(RedirectResponse, self).__init__(status=301, 
                                               headerlist=[("Location", self._destination),
                                                           ("Content-Type", "text/html")], 
                                               content_type = "text/html")
    
    def _build_destination(self):
        '''This method is used to append the given query params to the base destination.'''
        
        params = ["%s=%s" % (param[0], param[1]) for param in self._query_params]
        
        if not params:
            return
        
        self._destination = "%s?%s" % (self._destination, "&".join(params))