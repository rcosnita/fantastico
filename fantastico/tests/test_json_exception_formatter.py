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
.. py:module:: fantastico.tests.test_json_exception_formatter
'''
from fantastico.exception_formatters import JsonExceptionFormatter
from fantastico.tests.base_case import FantasticoUnitTestsCase
import json

class JsonExceptionFormatterTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for JsonExceptionFormatter.'''

    _formatter = None

    def init(self):
        '''This method is invoked automatically to setup common dependencies for all test cases.'''

        self._formatter = JsonExceptionFormatter()

    def test_format_ex_ok(self):
        '''This test case ensures exceptions are correctly converted to json strings.'''

        ex_desc = {"attr1": "sample",
                   "attr2": "value"}

        expected_response = json.dumps(ex_desc)

        self.assertEqual(expected_response, self._formatter.format_ex(ex_desc))

    def test_format_ex_none(self):
        '''This test case ensures no exception is raised when formatting a None exception descriptor.'''

        self.assertEqual("\"{}\"", self._formatter.format_ex(None))
