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
.. py:module:: fantastico.utils.singleton
'''

class Singleton(object):
    '''This class provides a very simple decorator for creating singleton classes. It uses the approach proposed in PEP-318.

    .. code-block:: python

        @Singleton()
        class Person(object):
            pass

        assert Person() == Person()
    '''
    def __init__(self):
        self._instance = None

    def __call__(self, cls_arg):
        '''This method is invoked automatically when the class is imported into vm.'''

        old_newmeth = cls_arg.__new__

        def new_method(cls, *args, **kwargs):
            '''This method replaces the original __new__ method of the object and replaces the __init__ method from the class with
            a no operation __init__ method.'''

            if self._instance:
                return self._instance

            self._instance = old_newmeth(cls)
            cls.__init__(self._instance, *args, **kwargs)

            cls.__init__ = lambda instance, *args, **kwargs: None

            return self._instance

        cls_arg.__new__ = new_method

        return cls_arg
