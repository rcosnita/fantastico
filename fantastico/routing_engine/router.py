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
from fantastico.exceptions import FantasticoDuplicateRouteError, FantasticoNoRoutesError, FantasticoRouteNotFoundError, \
    FantasticoHttpVerbNotSupported
from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator
import re
import threading

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

        if self._loader_lock is None and len(self._loaders) == 0:
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

        route_configs = self._find_url_regex(url)
        route_config = None

        http_verb = environ.get("REQUEST_METHOD").upper()

        for route_config in route_configs:
            if http_verb not in route_config["http_verbs"]:
                route_config = None
                continue

            break

        if not route_config:
            raise FantasticoHttpVerbNotSupported(http_verb)

        http_verb_config = route_config["http_verbs"][http_verb]

        last_dot = http_verb_config.rfind(".")

        if last_dot == -1:
            raise FantasticoNoRoutesError("Route %s has an invalid controller mapped." % url)

        controller_cls = http_verb_config[:last_dot]
        controller_meth = http_verb_config[last_dot + 1:]

        environ["route_%s_handler" % url] = {"controller": instantiator.instantiate_class(controller_cls,
                                                                                          [self._settings_facade]),
                                             "method": controller_meth,
                                             "url_params": route_config.get("url_params")}

    def _find_url_regex(self, url):
        '''This method is used to obtain route configuration starting from a given url.

        :param url: the relative url we want to serve. E.g: /component1/test/url
        :type url: string
        :returns: A list of dictionaries containing the method and http_verbs supported.
        :raises FantasticoNoRoutesError: This exception is raised if the url does not match any registered patterns.
        '''

        route_configs = []
        route_config = None

        for route_pat in self._routes.keys():
            match = re.search(route_pat, url)

            if not match:
                continue

            route_config = self._routes[route_pat]

            route_config["url_params"] = match.groupdict()

            route_configs.append(route_config)

        if not route_config:
            raise FantasticoRouteNotFoundError("Route %s is not registered or no config registered." % url)

        return route_configs
