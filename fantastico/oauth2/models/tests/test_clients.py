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
.. py:module:: fantastico.oauth2.models.tests.test_clients
'''
from fantastico.oauth2.models.clients import Client
from fantastico.tests.base_case import FantasticoUnitTestsCase
import uuid

class ClientTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for client entity.'''

    def test_init_noargs(self):
        '''This test case ensures a client can be instantiated without arguments.'''

        obj = Client()

        self.assertIsNone(obj.client_id)
        self.assertIsNone(obj.name)
        self.assertIsNone(obj.description)
        self.assertIsNone(obj.grant_types)
        self.assertIsNone(obj.token_iv)
        self.assertIsNone(obj.token_key)
        self.assertIsNone(obj.revoked)

    def test_init_ok(self):
        '''This test case ensures a client can be instantiated with arguments.'''

        client_id = str(uuid.uuid4())
        name = "simple app"
        description = "simple app description."
        grant_types = "token,code"
        token_iv = "simple iv"
        token_key = "simple key"
        revoked = False

        obj = Client(client_id, name, description, grant_types, token_iv, token_key, revoked)

        self.assertEqual(client_id, obj.client_id)
        self.assertEqual(name, obj.name)
        self.assertEqual(description, obj.description)
        self.assertEqual(grant_types, obj.grant_types)
        self.assertEqual(token_iv, obj.token_iv)
        self.assertEqual(token_key, obj.token_key)
        self.assertEqual(revoked, obj.revoked)
