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

        return self._dictionary

    def __init__(self, desc, immutable=True):
        if desc is None:
            desc = {}

        self.__setattr__("_internals", set(), internal=True)
        self.__setattr__("_immutable", immutable, internal=True)
        self.__setattr__("_dictionary", desc, internal=True)
        self.__setattr__("_internal_data", self._build_internal_structure(desc), internal=True)

    def _build_internal_structure(self, dictionary):
        '''This method recursively build an hierarchical data structure starting from a complex dictionary. When a value
        from dictionary is of type dictionary this is automatically converted to a DictionaryObject.'''

        result = {}

        for key in dictionary.keys():
            value = dictionary[key]

            if isinstance(value, dict):
                result[key] = DictionaryObject(value, self._immutable)
            else:
                result[key] = value

        return result

    def __getattr__(self, attr_name):
        '''This method returns the attr_name value if found. Otherwise it throws an AttributeError exception.'''

        if attr_name == "_internals" or attr_name in self._internals:
            return super(DictionaryObject, self).__getattribute__(attr_name)

        try:
            return self._internal_data[attr_name]
        except KeyError:
            raise AttributeError("Attribute %s is not found." % attr_name)

    def __setattr__(self, attr_name, attr_value, internal=False):
        '''This method set the attr_name with the given value either on the underlining dictionary or  on the current object
        instance.'''

        if internal:
            super(DictionaryObject, self).__setattr__(attr_name, attr_value)

            return

        if self._immutable:
            raise AttributeError("DictionaryObject is immutable so you can not set %s attribute." % attr_name)

        internal_data = self._internal_data
        dictionary = self._dictionary

        if attr_value is None:
            if not attr_name in internal_data:
                return

            del internal_data[attr_name]
            del dictionary[attr_name]

        internal_data[attr_name] = attr_value
        if attr_name in dictionary:
            dictionary[attr_name] = attr_value

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
