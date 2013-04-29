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
from fantastico.exceptions import FantasticoClassNotFoundError, \
    FantasticoDuplicateRouteError, FantasticoNoRoutesError
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
        self.assertEqual("fantastico.routing_engine.router.tests.test_router.Controller.do_stuff", routes.get("/index.html"))
        self.assertEqual("fantastico.routing_engine.router.tests.test_router.Controller.do_stuff2", routes.get("/index2.html"))
        
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
        self.assertEqual("fantastico.routing_engine.router.tests.test_router.Controller.do_stuff", routes.get("/index.html"))
        self.assertEqual("fantastico.routing_engine.router.tests.test_router.Controller.do_stuff2", routes.get("/index2.html"))

    def test_no_loaders_error(self):
        '''Test case that ensures router will not work correctly without loaders configured in current configuration.'''
        
        self._settings_facade.get = Mock(return_value=None)
        
        self.assertRaises(FantasticoNoRoutesError, self._router.get_loaders)
        
    def test_no_routes_error(self):
        '''Test case that ensures no register routes causes registration process to raise an exception.'''
        
        self._settings_facade.get = Mock(return_value=["fantastico.routing_engine.tests.test_router.TestLoaderEmpty"])
        
        self.assertRaises(FantasticoNoRoutesError, self._router.register_routes)
        
class TestLoader(RouteLoader):
    '''Simple route loader used for unit testing.'''
    
    def load_routes(self):
        return {"/index.html": "fantastico.routing_engine.router.tests.test_router.Controller.do_stuff"}
    
class TestLoader2(RouteLoader):
    '''Simple route loader used for unit testing.'''
    
    def load_routes(self):
        return {"/index2.html": "fantastico.routing_engine.router.tests.test_router.Controller.do_stuff2"}
    
class TestLoader3(RouteLoader):
    '''Simple route loader used for unit testing.'''
    
    def load_routes(self):
        return {"/index.html": "fantastico.routing_engine.router.tests.test_router.Controller.do_stuff2"}
    
class TestLoaderEmpty(RouteLoader):
    '''Simple route loader meant to return no routes - unit testing purposes.'''
    
    def load_routes(self):
        return {}