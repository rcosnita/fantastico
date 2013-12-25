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
.. py:module:: fantastico.oauth2.tests
'''
from fantastico.oauth2.token import Token
from fantastico.tests.base_case import FantasticoUnitTestsCase
import time
import uuid

class TokenTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for token class.'''

    def test_token_build(self):
        '''This test case ensures a token correctly provides get properties for a given token descriptor.'''

        creation_time = time.time()
        expiration_time = creation_time + 300

        token_desc = {"client_id": uuid.uuid4(),
                      "type": "login",
                      "user_id": 1,
                      "creation_time": int(creation_time),
                      "expiration_time": int(expiration_time)}

        token = Token(token_desc)

        self.assertEqual(token_desc["client_id"], token.client_id)
        self.assertEqual(token_desc["type"], token.type)
        self.assertEqual(token_desc["user_id"], token.user_id)
        self.assertEqual(token_desc["creation_time"], token.creation_time)
        self.assertEqual(token_desc["expiration_time"], token.expiration_time)
