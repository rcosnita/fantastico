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
.. py:module:: fantastico.utils.tests.test_dictionaryobject
'''
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils.dictionary_object import DictionaryObject

class DictionaryObjectTests(FantasticoUnitTestsCase):
    '''This class provides the test suite for DictionaryObject class.'''

    def test_dictionaryobject_get(self):
        '''This method ensures get operation on existing dictionary keys work as expected.'''

        dict_obj = {"first_name": "John",
                    "last_name": "Doe",
                    "address": {"street": "17, Dreams Street"}}

        obj = MockDictionaryObject(dict_obj)

        self.assertEqual(dict_obj["first_name"], obj.first_name)
        self.assertEqual(dict_obj["last_name"], obj.last_name)

        address = obj.address
        self.assertIsInstance(address, DictionaryObject)
        self.assertEqual(dict_obj["address"]["street"], address.street)

    def test_dictionaryobject_get_notfound(self):
        '''This test case ensures non existent members access raise an exception.'''

        obj = MockDictionaryObject(None)

        self.assertRaises(AttributeError, lambda: obj.name)

    def test_dictionaryobject_set(self):
        '''This test case ensures the dictionary object is immutable and raises an exception if someone tries to change its
        members.'''

        obj = MockDictionaryObject({})

        def add_name(obj):
            obj.name = "cool name"

        self.assertRaises(AttributeError, add_name, obj)

class MockDictionaryObject(DictionaryObject):
    '''A very simple mock object used for testing dictionary object.'''

    pass
