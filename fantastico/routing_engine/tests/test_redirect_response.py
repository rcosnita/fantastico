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

.. py:module:: fantastico.routing_engine.tests.test_redirect_response
'''
from fantastico.exceptions import FantasticoError
from fantastico.routing_engine.custom_responses import RedirectResponse
from fantastico.tests.base_case import FantasticoUnitTestsCase
from webob.response import Response

class RedirectResponseTests(FantasticoUnitTestsCase):
    '''This class provides test cases for ensuring redirect response class works.'''

    def test_redirect_response_simple(self):
        '''This test case ensures simple redirects work as expected (no query params appended).'''

        response = RedirectResponse(destination="http://www.google.ro")

        self.assertIsInstance(response, Response)
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://www.google.ro", response.headers["Location"])
        self.assertTrue(response.headers["Content-Type"].find("text/html") > -1)

    def test_redirect_response_with_params(self):
        '''This test case ensures a redirect response with query params correctly builds destination.'''

        query_params = [("q", "where can I find a restaurant"),
                        ("sourceid", "chrome")]

        response = RedirectResponse(destination="http://www.google.ro/search", query_params=query_params)

        self.assertIsInstance(response, Response)
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://www.google.ro/search?q=where can I find a restaurant&sourceid=chrome",
                         response.headers["Location"])
        self.assertTrue(response.headers["Content-Type"].find("text/html") > -1)

    def test_nodestination_given(self):
        '''This test case ensures redirect response can not be instantiated without a valid destination.'''

        with self.assertRaises(TypeError):
            RedirectResponse()

        for destination in [None, "", "     "]:
            with self.assertRaises(FantasticoError):
                RedirectResponse(destination)
