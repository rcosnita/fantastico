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
.. py:module:: fantastico.contrib.oauth2_idp.models.tests.test_users
'''
from fantastico.contrib.oauth2_idp.models.users import User
from fantastico.tests.base_case import FantasticoUnitTestsCase

class UserTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for ensuring user entity works as expected.'''

    def test_init_noargs(self):
        '''This test case ensures an user can be instantiated without arguments.'''

        user = User()

        self.assertIsNone(user.username)
        self.assertIsNone(user.password)
        self.assertIsNone(user.person_id)

    def test_init_with_args(self):
        '''This test case ensures an user can be instantiated with arguments.'''

        username = "john.doe@email.com"
        password = "very simple password"
        person_id = 1

        user = User(username, password, person_id)

        self.assertEqual(username, user.username)
        self.assertEqual(password, user.password)
        self.assertEqual(person_id, user.person_id)
