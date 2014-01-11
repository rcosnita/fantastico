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

        new_street = "street changed"

        obj = MockDictionaryObject(dict_obj, immutable=False)

        self.assertEqual(dict_obj["first_name"], obj.first_name)
        self.assertEqual(dict_obj["last_name"], obj.last_name)

        address = obj.address
        self.assertIsInstance(address, DictionaryObject)

        address.street = new_street
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

    def test_dictionaryobject_get_dict(self):
        '''This test case ensures a token dictionary representation can be retrieved correctly.'''

        descriptor = {"attr1": "test attr1",
                      "attr2": "test attr2"}

        obj = MockDictionaryObject(descriptor)

        self.assertEqual(descriptor, obj.dictionary)

    def test_dictionary_eq_ok(self):
        '''This test case ensures two dictionary objects built using two equal dictionaries are equal.'''

        desc = {"attr1": "abc",
                "attr2": "abcd"}

        desc2 = {"attr1": "abc",
                 "attr2": "abcd"}

        obj1 = MockDictionaryObject(desc)
        obj2 = MockDictionaryObject(desc2)

        self.assertEqual(obj1, obj2)
        self.assertEqual(hash(obj1), hash(obj2))

    def test_dictionary_notimmutable(self):
        '''This test case ensures a dictionary object can be built so that his attributes and underlining dictionaries can be
        changed at runtime.'''

        new_attr2 = "abc_altered"

        desc = {"attr1": "abcd",
                "attr2": "abc"}

        obj = DictionaryObject(desc, immutable=False)

        self.assertEqual(desc["attr1"], obj.attr1)
        self.assertEqual(desc["attr2"], obj.attr2)

        obj.attr2 = new_attr2
        obj.new_attr2 = new_attr2

        self.assertEqual(new_attr2, desc["attr2"])
        self.assertEqual(new_attr2, obj.attr2)
        self.assertEqual(new_attr2, obj.new_attr2)

    def test_dictionary_setnone_deletekey(self):
        '''This test case ensures that None values set on non immutable objects trigger a delete of the specified key.'''

        desc = {"attr1": "test",
                "attr2": "value"}

        obj = DictionaryObject(desc, immutable=False)

        obj.attr1 = None

        self.assertFalse("attr1" in desc)

    def test_dictionary_eq_differentdicts(self):
        '''This test case ensures two dictionary objects build using different dictionaries are not equal.'''

        desc = {"attr1": "abc"}

        desc2 = {"attr1": "abcd"}

        obj1 = MockDictionaryObject(desc)
        obj2 = MockDictionaryObject(desc2)

        self.assertNotEqual(obj1, obj2)
        self.assertNotEqual(hash(obj1), hash(obj2))

    def test_dictionary_eq_differenttype(self):
        '''This test case ensures dictionary objects equality comparison fails when the term checked for equality is not of type
        DictionaryObject.'''

        obj1 = MockDictionaryObject({"attr1": "abcd"})
        obj2 = object()

        self.assertNotEqual(obj1, obj2)
        self.assertNotEqual(hash(obj1), hash(obj2))

class MockDictionaryObject(DictionaryObject):
    '''A very simple mock object used for testing dictionary object.'''

    pass
