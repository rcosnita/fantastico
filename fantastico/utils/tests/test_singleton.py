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
.. py:module:: fantastico.utils.tests.singleton
'''
from fantastico.utils.singleton import Singleton
from fantastico.tests.base_case import FantasticoUnitTestsCase

@Singleton()
class SingleClass(object):
    init_count = 0

    def __init__(self):
        SingleClass.init_count += 1

class SingletonTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for singleton decorator.'''

    def test_singleton_ok(self):
        '''This test case ensures only one instance of a given class can be built.'''

        instance1 = SingleClass()
        instance2 = SingleClass()

        self.assertEqual(instance1, instance2)
        self.assertEqual(SingleClass.init_count, 1)
