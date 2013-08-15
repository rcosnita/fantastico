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
.. py:module:: fantastico.rendering.tests.itest_component_reusage
'''
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from urllib.request import Request
import urllib

class ComponentReusageIntegration(DevServerIntegration):
    '''This class provides the integration tests for ensuring component reusage works as expected within the framework.'''

    _response = None

    def init(self):
        '''This method is invoked automatically before each test case.'''

        self._response = None

    def test_component_html_rendering_ok(self):
        '''This test case ensures that a url which reuses components internally the result is retrieved correctly.'''

        endpoint = "/mvc/reuse-component"

        def retrieve_menu_items(server):
            request = Request(self._get_server_base_url(server, endpoint))

            self._response = urllib.request.urlopen(request)

        def assert_ok(server):
            self.assertIsNotNone(self._response)
            self.assertEqual(200, self._response.getcode())
            self.assertEqual("text/html; charset=UTF-8", self._response.info()["Content-Type"])

            body = self._response.read().decode()

            self.assertTrue(body.find("'inner_message': {'message': 'inner_message'}") > -1)
            self.assertTrue(body.find("'message': 'Hello world'") > -1)

        self._run_test_against_dev_server(retrieve_menu_items, assert_ok)

    def test_component_remote_model_local_view_rendering(self):
        '''This test case covers the scenario where a remote model is plugged into a local view.'''

        endpoint = "/simple-component/foreign-component-reusage"

        def retrieve_menu_items(server):
            request = Request(self._get_server_base_url(server, endpoint))

            self._response = urllib.request.urlopen(request)

        def assert_ok(server):
            self.assertIsNotNone(self._response)
            self.assertEqual(200, self._response.getcode())
            self.assertEqual("text/html; charset=UTF-8", self._response.info()["Content-Type"])

            body = self._response.read().decode()

            self.assertTrue(body.find("Hello inner_message") > -1)

        self._run_test_against_dev_server(retrieve_menu_items, assert_ok)
