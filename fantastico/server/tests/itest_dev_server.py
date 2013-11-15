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
.. py:module:: fantastico.server.tests.itest_dev_server
'''
from fantastico.server.dev_server import DevServer
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from fantastico import mvc
import threading
import time

class DevServerIntegration(FantasticoIntegrationTestCase):
    '''This class provides the foundation for writing integration tests that do http requests against a fantastico server.

    .. code-block:: python

        class DummyLoaderIntegration(DevServerIntegration):
            def init(self):
                self._exception = None

            def test_server_runs_ok(self):
                def request_logic(server):
                    request = Request(self._get_server_base_url(server, DummyRouteLoader.DUMMY_ROUTE))
                    with self.assertRaises(HTTPError) as cm:
                        urllib.request.urlopen(request)

                    self._exception = cm.exception

                def assert_logic(server):
                    self.assertEqual(400, self._exception.code)
                    self.assertEqual("Hello world.", self._exception.read().decode())

                self._run_test_all_envs(lambda env, settings_cls: self._run_test_against_dev_server(request_logic, assert_logic))

                # you can also pass only request logic without assert logic
                # self._run_test_all_envs(lambda env, settings_cls: self._run_test_against_dev_server(request_logic))

    As you can see from above listed code, when you write a new integration test against Fantastico server you only need
    to provide the request logic and assert logic functions. Request logic is executed while the server is up and running.
    Assert logic is executed after the server has stopped.
    '''

    def _run_test_against_dev_server(self, request_logic, assert_logic=None):
        '''This method provides a template for writing integration tests that requires a development server being active.
        It accepts a request logic (code that actually do the http request) and an assert logic for making sure
        code is correct.'''

        assert_logic = assert_logic or self._check_server_started

        server = DevServer()

        def start_server():
            server.start()

        def stop_server():
            try:
                while not server.started:
                    time.sleep(0.01)

                request_logic(server)

                self.assertTrue(server.started)
            finally:
                server.stop()

        thread_start = threading.Thread(target=start_server)
        thread_start.start()

        thread_stop = threading.Thread(target=stop_server)
        thread_stop.start()

        thread_stop.join()

        self._check_server_started(server)
        assert_logic(server)

    def _check_server_started(self, server):
        '''This method holds the sanity checks to ensure a server is started correctly.'''

        self.assertEqual(12000, server.port)
        self.assertEqual("localhost", server.hostname)

    def _get_server_base_url(self, server, route):
        '''This method returns the absolute url for a given relative url (route).'''

        return "http://%s:%s%s" % (server.hostname, server.port, route)
