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
.. py:module:: fantastico.exception_formatters.test_exception_formatter_factory
'''
from fantastico.exception_formatters import ExceptionFormattersFactory, JsonExceptionFormatter, FormUrlEncodedExceptionFormatter, \
    DummyExceptionFormatter, HashUrlEncodedExceptionFormatter
from fantastico.tests.base_case import FantasticoUnitTestsCase

class ExceptionFormattersFactoryTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for exception formatters factory.'''

    _factory = None

    def init(self):
        '''This method is invoked automatically to setup common dependencies for all test cases.'''

        self._factory = ExceptionFormattersFactory()

    def test_get_formatter_json(self):
        '''This test case ensures a json exception formatter can be built using the factory of formatters.'''

        result = self._factory.get_formatter(ExceptionFormattersFactory.JSON)

        self.assertIsInstance(result, JsonExceptionFormatter)

    def test_get_formatter_urlencoded(self):
        '''This test case ensures an url encoded exception formatter can be built using the factory of formatters.'''

        result = self._factory.get_formatter(ExceptionFormattersFactory.FORM)

        self.assertIsInstance(result, FormUrlEncodedExceptionFormatter)

    def test_get_formatter_hashencoded(self):
        '''This test case ensures an hash encoded exception formatter can be built using the factory of formatters.'''

        result = self._factory.get_formatter(ExceptionFormattersFactory.HASH)

        self.assertIsInstance(result, HashUrlEncodedExceptionFormatter)

    def test_get_formatter_unknown(self):
        '''This test case ensures a dummy formatter is returned when a formatter type is not supported by exception formatters
        factory.'''

        result = self._factory.get_formatter("unknown formatter for good")

        self.assertIsInstance(result, DummyExceptionFormatter)
