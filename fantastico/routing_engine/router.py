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

.. py:module:: fantastico.routing_engine.router
'''
from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator
import threading
from fantastico.exceptions import FantasticoDuplicateRouteError, FantasticoNoRoutesError, \
    FantasticoRouteNotFoundError

class Router(object):
    '''This class is used for registering all available routes by using all registered loaders.'''
    
    def __init__(self, settings_facade=SettingsFacade):
        self._settings_facade = settings_facade()
        self._loaders = []
        self._loader_lock = None
        self._routes_lock = None
        self._routes = {}
        
    def get_loaders(self):
        '''Method used to retrieve all available loaders. If loaders are not currently instantiated they are by these method.
        This method also supports multi threaded workers mode of wsgi with really small memory footprint. It uses an internal
        lock so that it makes sure available loaders are instantiated only once per wsgi worker.'''
                
        conf_loaders = self._settings_facade.get("routes_loaders") or []
                
        if len(conf_loaders) == 0:
            raise FantasticoNoRoutesError("No loaders configured.")
                        
        if self._loader_lock is not None and len(self._loaders) == 0:
            self._loader_lock = threading.Lock()
            self._loaders = []
        
        if self._loader_lock:
            self._loader_lock.acquire()
        
        if len(self._loaders) == 0:
            for loader_cls in conf_loaders:
                loader = instantiator.instantiate_class(loader_cls, [self._settings_facade])
                
                self._loaders.append(loader)
            
        if self._loader_lock is not None:
            self._loader_lock.release()
            self._loader_lock = None
            
        return self._loaders
    
    def register_routes(self):
        '''Method used to register all routes from all loaders. If the loaders are not yet initialized this method will first
        load all available loaders and then it will register all available routes. Also, this method initialize available routes
        only once when it is first invoked.'''
        
        if len(self._loaders) == 0:
            self.get_loaders()
        
        if len(self._routes) == 0 and self._routes_lock is None:
            self._routes_lock = threading.Lock()
            
        if self._routes_lock:
            self._routes_lock.acquire()
        
        if len(self._routes) == 0:
            for loader in self._loaders:
                loader_routes = loader.load_routes()
                
                for route in loader_routes.keys():
                    if route in self._routes:
                        raise FantasticoDuplicateRouteError("Route %s already registered." % route)
                
                    self._routes[route] = loader_routes[route]
                    
        if self._routes_lock:
            self._routes_lock.release()
            self._routes_lock = None
        
        if len(self._routes) == 0:
            raise FantasticoNoRoutesError("No routes found with %s registered loaders." % len(self._loaders))
        
        return self._routes
    
    def handle_route(self, url, environ):
        '''Method used to identify the given url method handler. It enrich the environ dictionary with a new entry that
        holds a controller instance and a function to be executed from that controller.'''
        
        if url not in self._routes:
            raise FantasticoRouteNotFoundError("Route %s is not registered." % url)
        
        route_config = self._routes[url]
        
        if route_config is None:
            raise FantasticoNoRoutesError("Route %s has an invalid controller mapped." % url)
        
        last_dot = route_config.rfind(".")

        if last_dot == -1:
            raise FantasticoNoRoutesError("Route %s has an invalid controller mapped." % url)
        
        controller_cls =  route_config[:last_dot]
        controller_meth = route_config[last_dot + 1:]
        
        environ["route_%s_handler" % url] = {"controller": instantiator.instantiate_class(controller_cls, 
                                                                                          [self._settings_facade]),
                                             "method": controller_meth}