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
.. py:module:: fantastico.oauth2.models.tests.test_returnurls
'''
from fantastico.oauth2.models.return_urls import ClientReturnUrl
from fantastico.tests.base_case import FantasticoUnitTestsCase
import uuid

class ClientReturnUrlTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for client return url model.'''

    def test_init_noargs(self):
        '''This test case ensures the model can be instantiated without arguments.'''

        obj = ClientReturnUrl()

        self.assertIsNone(obj.url_id)
        self.assertIsNone(obj.client_id)
        self.assertIsNone(obj.return_url)

    def test_init_ok(self):
        '''This test case ensures the model can be instantiated with arguments specified.'''

        client_id = str(uuid.uuid4())
        return_url = "http://simple-test"

        obj = ClientReturnUrl(client_id, return_url)

        self.assertIsNone(obj.url_id)
        self.assertEqual(client_id, obj.client_id)
        self.assertEqual(return_url, obj.return_url)
