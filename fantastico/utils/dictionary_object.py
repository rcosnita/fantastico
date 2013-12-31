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
.. py:module:: fantastico.utils.dictionary_object
'''

class DictionaryObject(object):
    '''This class provides a model for giving a dictionary support for attributes like keys access. This is an immutable read
    object which raises exception if you try to change it's attributes once instantiated.

    .. code-block:: python

        class SimpleObject(DictionaryObject):
            pass

        obj = SimpleObject({"first_name": "John", "last_name": "Doe"})

        print(obj.first_name)'''

    @property
    def dictionary(self):
        '''This property returns a dictionary representation of this object.'''

        return self._members

    def __init__(self, members):
        self.__setattr__("_members", members or {}, True)

    def __getattr__(self, attr_name):
        '''This method search attribute name into _members dictionary.'''

        member = self._members.get(attr_name)

        if member is None:
            raise AttributeError("DictionaryObject does not have attribute %s" % attr_name)

        if isinstance(member, dict):
            return DictionaryObject(member)

        return member

    def __setattr__(self, attr_name, value, inner=False):
        '''Thie method raises an exception every time is called because dictionary object is immutable.'''

        if not inner:
            raise AttributeError("DictionaryObject is immutable. You can not set attribute %s" % attr_name)

        super(DictionaryObject, self).__setattr__(attr_name, value)

    def __eq__(self, obj):
        '''This method is overriden in order to correctly provide equality of dictionary objects.'''

        if not isinstance(obj, type(self)):
            return False

        return obj.dictionary == self.dictionary

    def __hash__(self):
        '''This method is overriden so that it correctly generates hash codes for dictionary objects.'''

        result = 0

        for key in self.dictionary.keys():
            result ^= hash(key)
            result ^= hash(self.dictionary[key])

        return result
