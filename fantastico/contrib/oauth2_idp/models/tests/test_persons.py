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
.. py:module:: fantastico.contrib.oauth2_idp.models.tests.test_persons
'''
from fantastico.contrib.oauth2_idp.models.persons import Person
from fantastico.tests.base_case import FantasticoUnitTestsCase

class PersonTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for ensuring correct functionality of person entity.'''

    def test_init_noargs(self):
        '''This test case ensures a person can be instantiated without arguments.'''

        person = Person()

        self.assertIsNone(person.first_name)
        self.assertIsNone(person.last_name)
        self.assertIsNone(person.email_address)
        self.assertIsNone(person.cell_number)
        self.assertIsNone(person.phone_number)

    def test_init_with_args(self):
        '''This test case ensures a person can be instantiated with arguments.'''

        first_name = "John"
        last_name = "Doe"
        email_address = "john.doe@email.com"
        cell_number = "+4 (0727) 000 000"
        phone_number = "+4 (021) 000 00 00"

        person = Person(first_name, last_name, email_address, cell_number, phone_number)

        self.assertEqual(first_name, person.first_name)
        self.assertEqual(last_name, person.last_name)
        self.assertEqual(email_address, person.email_address)
        self.assertEqual(cell_number, person.cell_number)
        self.assertEqual(phone_number, person.phone_number)
