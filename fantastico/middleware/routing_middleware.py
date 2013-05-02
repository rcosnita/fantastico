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
.. py:module:: fantastico.middleware.routing_middleware
'''
from fantastico.exceptions import FantasticoNoRequestError, FantasticoError
from fantastico.routing_engine.router import Router

class RoutingMiddleware(object):
    '''Class used to integrate routing engine fantastico component into request / response lifecycle. This middleware is 
    responsible for:
    
    #. instantiating the router component and make it available to other components / middlewares through WSGI environment.
    #. register all configured fantastico loaders (:py:func:`fantastico.routing_engine.router.Router.get_loaders`).
    #. register all available routes (:py:func:`fantastico.routing_engine.router.Router.register_routes`).
    #. handle route requests (:py:func:`fantastico.routing_engine.router.Router.handle_route`).
    
    It is important to understand that routing middleware assume a **WebOb request** available into WSGI environ. Otherwise, 
    :py:class:`fantastico.exceptions.FantasticoNoRequestError` will be thrown. You can read more about request middleware 
    at :doc:`/features/request_response`.'''
    
    def __init__(self, app, router_cls = Router):
        self._app = app
        self._router = router_cls()
        
        self._router.get_loaders()
        self._router.register_routes()
        
    def __call__(self, environ, start_response):
        '''Method invoked when a new request must be solved by the routing engine.'''
        
        request = environ.get("fantastico.request")
        
        if not request:
            raise FantasticoNoRequestError()
        
        try:
            self._router.handle_route(request.path, environ)
        except Exception as ex:
            raise FantasticoError(ex)
        
        return self._app(environ, start_response)