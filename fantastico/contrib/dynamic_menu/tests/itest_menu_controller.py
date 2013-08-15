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
.. py:module:: fantastico.contrib.dynamic_menu.tests.itest_menu_controller
'''
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from urllib.error import HTTPError
from urllib.request import Request
import json
import urllib

class DynamicMenuIntegration(DevServerIntegration):
    '''This class provides integration tests for making sure dynamic menu provides specified functionality.'''

    _response = None
    _exception = None

    def init(self):
        '''This method is invoked automatically before each test case.'''

        self._response = None
        self._exception = None

    def test_dynamic_menu_items_retrieve(self):
        '''This test case ensures items belonging to an existing menu are retrieved correctly.'''

        endpoint = "/dynamic-menu/menus/1/items/"

        def retrieve_menu_items(server):
            request = Request(self._get_server_base_url(server, endpoint))

            self._response = urllib.request.urlopen(request)

        def assert_ok(server):
            expected_items = [{"url": "/homepage", "label": "Home", "target": "_blank",
                               "title": "Simple and friendly description"},
                              {"url": "/page2", "label": "Page 2", "target": "_blank",
                               "title": "Simple and friendly description"},
                              {"url": "/page3", "label": "Page 3", "target": "_blank",
                               "title": "Simple and friendly description"}]

            self.assertIsNotNone(self._response)
            self.assertEqual(200, self._response.getcode())
            self.assertEqual("application/json; charset=UTF-8", self._response.info()["Content-Type"])

            body = self._response.read().decode()

            self.assertIsNotNone(body)

            body = json.loads(body)

            items = body.get("items")

            self.assertEqual(len(expected_items), len(items))

            for i, item in enumerate(expected_items):
                self.assertEqual(item["url"], items[i]["url"])
                self.assertEqual(item["label"], items[i]["label"])
                self.assertEqual(item["target"], items[i]["target"])
                self.assertEqual(item["title"], items[i]["title"])

        self._run_test_against_dev_server(retrieve_menu_items, assert_ok)

    def test_dynamic_menu_items_retrieve_not_found_ex(self):
        '''This test case ensures an exception is raised whenever we try to retrieve items for an inexistent menu.'''

        endpoint = "/dynamic-menu/menus/9999/items/"

        def retrieve_menu_items(server):
            request = Request(self._get_server_base_url(server, endpoint))

            with self.assertRaises(HTTPError) as cm:
                urllib.request.urlopen(request)

            self._exception = cm.exception

        def assert_menu_not_found(server):
            self.assertIsNotNone(self._exception)

        self._run_test_against_dev_server(retrieve_menu_items, assert_menu_not_found)
