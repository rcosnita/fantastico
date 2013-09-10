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
.. py:module:: fantastico.contrib.dynamic_pages.tests.itest_pages_router
'''

from fantastico.server.tests.itest_dev_server import DevServerIntegration
from urllib.error import HTTPError
from urllib.request import Request
import urllib

class PagesRouterIntegration(DevServerIntegration):
    '''This class is used to check correct behavior of pages router.'''

    _exception = None
    _response = None

    def init(self):
        '''This method automatically set common dependencies for all tests.'''

        self._exception = None
        self._response = None

    def test_page_not_found(self):
        '''This test case is used to ensure 404 error code is retrieved for pages which are not mapped into
        database.'''

        def request_logic(server):
            request = Request(self._get_server_base_url(server, "/dynamic/default/page-not-found/for/sure"))
            with self.assertRaises(HTTPError) as cm:
                urllib.request.urlopen(request)

            self._exception = cm.exception

        def assert_logic(server):
            self.assertEqual(404, self._exception.code)

        self._run_test_against_dev_server(request_logic, assert_logic)

    def test_local_page_found(self):
        '''This test case is used to correctly access a mapped paged.'''

        def request_logic(server):
            request = Request(self._get_server_base_url(server, "/dynamic/test/default/page"))
            self._response = urllib.request.urlopen(request)

        def assert_logic(server):
            self.assertIsNotNone(self._response)
            self.assertEqual(200, self._response.status)

            body = self._response.read().decode()

            self.assertTrue(body.find("<html lang=\"ro-RO\">") > -1, "language not rendered correctly")
            self.assertTrue(body.find("<meta name=\"keywords\" content=\"keyword1\" />") > -1,
                            "keywords not rendered correctly")
            self.assertTrue(body.find("<meta name=\"description\" content=\"description\" />") > -1,
                            "description not rendered correctly")
            self.assertTrue(body.find("<title>title</title>") > -1, "title not rendered correctly")
            self.assertTrue(body.find("<h1>article title</h1>") > -1, "article title from model not rendered correctly")
            self.assertTrue(body.find("<h2>article content</h2>") > -1, "article content from model not rendered correctly")

        self._run_test_against_dev_server(request_logic, assert_logic)
