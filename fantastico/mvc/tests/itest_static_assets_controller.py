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
.. py:module:: fantastico.mvc.tests.itest_static_assets_controller
'''
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from fantastico.settings import BasicSettings
from fantastico.utils import instantiator
from urllib.request import Request
import os
import urllib

class StaticAssetsIntegration(DevServerIntegration):
    '''This class provides the integration tests for ensuring StaticAssets controller works as expected.'''

    _response = None
    _root_folder = None

    def init(self):
        self._response = None
        self._root_folder = os.path.realpath(instantiator.get_class_abslocation(BasicSettings))

    def test_image_serve_ok(self):
        '''This test case requests a binary jpg file from dev server.'''

        img_route = "/samples/mvc/static/sample.jpg"

        def request_logic(server):
            request = Request(self._get_server_base_url(server, img_route))

            self._response = urllib.request.urlopen(request)

        def assert_logic(server):
            self.assertEqual(200, self._response.getcode())
            self.assertEqual("image/jpeg", self._response.info()["Content-Type"])

            expected_filepath = "%s/samples/mvc/static/sample.jpg" % self._root_folder

            with open(expected_filepath, "rb") as file_input:
                expected_content = file_input.read()

            self.assertIsNotNone(expected_content)
            self.assertEqual(expected_content, self._response.read())

        self._run_test_against_dev_server(request_logic, assert_logic)

    def test_icon_serve_notfound(self):
        '''This test case makes sure a favicon request is ignored if no icon is present on disk.'''

        icon_route = "/favicon.ico"

        def request_logic(server):
            request = Request(self._get_server_base_url(server, icon_route))

            self._response = urllib.request.urlopen(request)

        def assert_logic(server):
            self.assertEqual(200, self._response.getcode())
            self.assertTrue(self._response.info()["Content-Type"] in ["image/vnd.microsoft.icon", "image/x-icon"])

        self._run_test_against_dev_server(request_logic, assert_logic)
