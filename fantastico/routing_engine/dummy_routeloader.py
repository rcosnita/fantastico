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

.. py:module:: fantastico.routing_engine.dummy_routeloader
'''
from fantastico.routing_engine.routing_loaders import RouteLoader
from webob.response import Response

class DummyRouteLoader(RouteLoader):
    '''This class represents an example of how to write a route loader. **DummyRouteLoader** is available in all configurations
    and it provides a single route to the routing engine: */dummy/route/loader/test*. Integration tests rely on this loader
    to be configured in each available profile.'''
    
    DUMMY_ROUTE = "/dummy/route/loader/test"
    
    def load_routes(self):
        return {DummyRouteLoader.DUMMY_ROUTE: "fantastico.routing_engine.dummy_routeloader.DummyRouteLoader.display_test"}
    
    def display_test(self, request):
        '''This method handles **/dummy/route/loader/test route**. It is expected to receive a response with status code 400.
        We do this for being able to test rendering and also avoid false positive security scans messages.'''
        
        return Response(content_type=request.content_type, text="Hello world.", status_code=400)