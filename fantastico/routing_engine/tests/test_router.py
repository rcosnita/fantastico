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

.. py:module:: fantastico.routing_engine.tests.test_router
'''
from fantastico.exceptions import FantasticoClassNotFoundError, FantasticoDuplicateRouteError, FantasticoNoRoutesError, \
    FantasticoRouteNotFoundError, FantasticoHttpVerbNotSupported
from fantastico.routing_engine.router import Router
from fantastico.routing_engine.routing_loaders import RouteLoader
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from threading import Thread

class RouterTests(FantasticoUnitTestsCase):
    '''Test suite that ensures routing core works correctly:

    * load routes from all available loaders
    * enrich the wsgi environ with the correct controller that can resolve the current request.'''

    def init(self):
        self._settings_facade = Mock()
        self._settings_facade_cls = Mock(return_value=self._settings_facade)
        self._router = Router(self._settings_facade_cls)

    def test_register_loader_not_found(self):
        '''Test case that ensures a fantastico class not found exception is thrown when a loader is not found.'''

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoaderNotFound"])

        self.assertRaises(FantasticoClassNotFoundError, self._router.get_loaders)

    def test_register_single_loader(self):
        '''Test case that ensures all configured loaders are registered by routing core.'''

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader"])

        loaders = self._router.get_loaders()

        self.assertIsNotNone(loaders)
        self.assertEqual(1, len(loaders))
        self.assertIsInstance(loaders[0], TestLoader)

    def test_register_multiple_loaders(self):
        '''Test case that ensures all configured loaders are registered by routing core in the given order.'''

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader",
                                                       "fantastico.routing_engine.tests.test_router.TestLoader2",
                                                       "fantastico.routing_engine.tests.test_router.TestLoader3"])

        loaders = self._router.get_loaders()

        self.assertIsNotNone(loaders)
        self.assertEqual(3, len(loaders))
        self.assertIsInstance(loaders[0], TestLoader)
        self.assertIsInstance(loaders[1], TestLoader2)
        self.assertIsInstance(loaders[2], TestLoader3)

    def test_register_routes_noconflict(self):
        '''Test case that ensures all configured loaders routes are registered correctly if no conflicts are found (no duplicate
        routes from multiple sources).'''

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader",
                                                       "fantastico.routing_engine.tests.test_router.TestLoader2"])

        routes = self._router.register_routes()

        self.assertIsNotNone(routes)
        self.assertEqual("fantastico.routing_engine.tests.test_router.Controller.do_stuff",
                         routes.get("/index.html")["http_verbs"]["GET"])
        self.assertEqual("fantastico.routing_engine.tests.test_router.Controller.do_stuff2",
                         routes.get("/index2.html")["http_verbs"]["GET"])

    def test_register_routes_conflict(self):
        '''Test case that ensures an exception is thrown whenever duplicate routes are detected.'''

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader",
                                                       "fantastico.routing_engine.tests.test_router.TestLoader2",
                                                       "fantastico.routing_engine.tests.test_router.TestLoader3"])

        self.assertRaises(FantasticoDuplicateRouteError, self._router.register_routes)

    def test_get_loaders_multithreads(self):
        '''Test case that ensures loaders are loaded by one single thread even if multiple threads request
        loaders list.'''

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader",
                                                       "fantastico.routing_engine.tests.test_router.TestLoader2",
                                                       "fantastico.routing_engine.tests.test_router.TestLoader3"])

        threads = []

        def get_loaders_async(router):
            router.get_loaders()

        for i in range(0, 10):
            thread = Thread(target=get_loaders_async, name="GetLoadersThread-%s" % i, kwargs={"router": self._router})
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(100)

        loaders = self._router.get_loaders()

        self.assertIsNotNone(loaders)
        self.assertEqual(3, len(loaders))
        self.assertIsInstance(loaders[0], TestLoader)
        self.assertIsInstance(loaders[1], TestLoader2)
        self.assertIsInstance(loaders[2], TestLoader3)

    def test_get_routes_multithreads(self):
        '''Test case that ensures routes register only once even if multiple threads call get routes.'''

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader",
                                                       "fantastico.routing_engine.tests.test_router.TestLoader2"])

        threads = []

        def get_routes_async(router):
            router.register_routes()

        for i in range(0, 10):
            thread = Thread(target=get_routes_async, name="GetRoutesThread-%s" % i, kwargs={"router": self._router})
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(100)

        routes = self._router.register_routes()

        self.assertIsNotNone(routes)
        self.assertEqual("fantastico.routing_engine.tests.test_router.Controller.do_stuff",
                         routes.get("/index.html")["http_verbs"]["GET"])
        self.assertEqual("fantastico.routing_engine.tests.test_router.Controller.do_stuff2",
                         routes.get("/index2.html")["http_verbs"]["GET"])

    def test_no_loaders_error(self):
        '''Test case that ensures router will not work correctly without loaders configured in current configuration.'''

        self._settings_facade.get = Mock(return_value=None)

        self.assertRaises(FantasticoNoRoutesError, self._router.get_loaders)

    def test_no_routes_error(self):
        '''Test case that ensures no register routes causes registration process to raise an exception.'''

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoaderEmpty"])

        self.assertRaises(FantasticoNoRoutesError, self._router.register_routes)

    def test_handle_route_ok(self):
        '''Test case that ensures handle route correctly instantiate the route handler and add it to WSGI environ dictionary.'''

        environ = {"REQUEST_METHOD": "GET"}

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader"])

        self._router.register_routes()

        self._router.handle_route("/index.html", environ)

        handler = environ.get("route_/index.html_handler")

        self.assertIsNotNone(handler)
        self.assertIsInstance(handler.get("controller"), Controller)
        self.assertEqual("do_stuff", handler.get("method"))

    def test_handle_route_regex_ok(self):
        '''Test case that ensures handle route correctly identifies a reg ex mapped url and execute it accordingly.'''

        environ = {"REQUEST_METHOD": "GET"}

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader"])

        self._router.register_routes()

        self._router.handle_route("/test-component/static-test/path/to/nowhere", environ)

        handler = environ.get("route_/test-component/static-test/path/to/nowhere_handler")

        self.assertIsNotNone(handler)
        self.assertIsInstance(handler.get("controller"), Controller)
        self.assertEqual("do_regex_action", handler.get("method"))

        url_params = handler.get("url_params")
        self.assertIsNotNone(url_params)
        self.assertEqual("test-component", url_params.get("component_name"))
        self.assertEqual("path/to/nowhere", url_params.get("path"))

    def test_handle_route_controller_missing(self):
        '''Test case that ensures handle route correctly raise an exception if it can't locate the requested controller.'''

        environ = {"REQUEST_METHOD": "GET"}

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader3"])

        self._router.register_routes()

        self.assertRaises(FantasticoClassNotFoundError, self._router.handle_route, *["/index.html", environ])

    def test_handle_route_empty_controller(self):
        '''Test case that ensures handle route will raise a fantastico exception in case an None or empty string is
        retrieved as route handler.'''

        environ = {"REQUEST_METHOD": "get"}

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader3"])

        self._router.register_routes()

        self.assertRaises(FantasticoNoRoutesError, self._router.handle_route, *["/index2.html", environ])

    def test_handle_route_notfound(self):
        '''This test case make sure an exception is thrown when a given url is not registered.'''

        environ = {}

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader3"])

        self._router.register_routes()

        self.assertRaises(FantasticoRouteNotFoundError, self._router.handle_route, *["/not_found_route.html", environ])

    def test_invalid_http_verb(self):
        '''This test case makes sure a route can not be invoked with an http verb that is not supported.'''

        environ = {"REQUEST_METHOD": "post"}

        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoader"])

        self._router.register_routes()

        with self.assertRaises(FantasticoHttpVerbNotSupported) as cm:
            self._router.handle_route("/index.html", environ)

        self.assertEqual("POST", cm.exception.http_verb)

class TestLoader(RouteLoader):
    '''Simple route loader used for unit testing.'''

    def load_routes(self):
        return {"/index.html": {"http_verbs": {
                                               "GET": "fantastico.routing_engine.tests.test_router.Controller.do_stuff"
                                               }
                                },
                "^/(?P<component_name>.*)/static-test/(?P<path>.*)":
                    {"http_verbs": {"GET": "fantastico.routing_engine.tests.test_router.Controller.do_regex_action"
                                    }
                     }
                }

class TestLoader2(RouteLoader):
    '''Simple route loader used for unit testing.'''

    def load_routes(self):
        return {"/index2.html": {"http_verbs": {"GET": "fantastico.routing_engine.tests.test_router.Controller.do_stuff2"
                                                }
                                 }
                }

class TestLoader3(RouteLoader):
    '''Simple route loader used for unit testing.'''

    def load_routes(self):
        return {"/index.html": {"http_verbs": {
                                               "GET": "fantastico.routing_engine.tests.test_router.not_found.Controller.do_stuff2"
                                              }
                                },
                "/index2.html": {"http_verbs": {
                                                "GET": ""
                                               }
                                 }
                }

class TestLoaderEmpty(RouteLoader):
    '''Simple route loader meant to return no routes - unit testing purposes.'''

    def load_routes(self):
        return {}

class Controller(object):
    '''Just a simple controller used for unit testing purposes.'''

    def __init__(self, settings_facade):
        self._settings_facade = settings_facade()

    def do_stuff(self, request):
        '''Simple method for handling a route.'''
