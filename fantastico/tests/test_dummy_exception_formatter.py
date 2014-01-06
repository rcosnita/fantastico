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
.. py:module:: fantastico.tests.test_dummy_exception_formatter
'''
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.exception_formatters import DummyExceptionFormatter

class DummyExceptionFormatterTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for DummyExceptionFormatter class.'''

    _formatter = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies for all test cases.'''

        self._formatter = DummyExceptionFormatter()

    def test_format_ex_ok(self):
        '''This test case ensures dummy formatter format_ex works as expected.'''

        for ex_desc in [None, {}, {"attr": "ok"}]:
            for ctx in [None, {}, {"attr": "ok"}]:
                self.assertEqual("", self._formatter.format_ex(ex_desc, ctx))
