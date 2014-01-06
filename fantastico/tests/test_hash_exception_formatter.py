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
.. py:module:: fantastico.tests.test_hash_exception_formatter
'''
from fantastico.exception_formatters import HashUrlEncodedExceptionFormatter
from fantastico.tests.base_case import FantasticoUnitTestsCase
import urllib

class HashUrlEncodedExceptionFormatterTests(FantasticoUnitTestsCase):
    '''This class provides tests suite for HashUrlEncodedExceptionFormatter class.'''

    _formatter = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies for all test cases.'''

        self._formatter = HashUrlEncodedExceptionFormatter()

    def test_format_ex_ok(self):
        '''This test case ensures the correct string is returned when redirect uri does not have query parameters or
        hash section.'''

        ex_desc = {"attr2": "value", "attr1": "sample cool"}
        ctx = {"redirect_uri": "/example/cb"}

        expected_url = "/example/cb#attr1=%s&attr2=%s" % (urllib.parse.quote(ex_desc["attr1"]), ex_desc["attr2"])

        self.assertEqual(expected_url, self._formatter.format_ex(ex_desc, ctx))

    def test_format_ex_redirectwithhash_ok(self):
        '''This test case ensures the correct string is returned when redirect uri already contains a hash fragment.'''

        ex_desc = {"attr2": "value", "attr1": "sample"}
        ctx = {"redirect_uri": "/example/cb#hashf"}

        expected_url = "/example/cb#hashf&attr1=sample&attr2=value"

        self.assertEqual(expected_url, self._formatter.format_ex(ex_desc, ctx))

    def test_format_ex_redirectqparams_ok(self):
        '''This test case ensures the correct string is returned when redirect uri already contains query parameters.'''

        ex_desc = {"attr2": "value", "attr1": "sample"}
        ctx = {"redirect_uri": "/example/cb?q1=search"}

        expected_url = "/example/cb?q1=search#attr1=sample&attr2=value"

        self.assertEqual(expected_url, self._formatter.format_ex(ex_desc, ctx))

    def test_format_ex_nodesc(self):
        '''This test case ensures no exception is raised even though exception descriptor is None.'''

        ctx = {"redirect_uri": "/example/cb?q1=search"}

        for ex_desc in [None, {}]:
            self.assertEqual(ctx["redirect_uri"], self._formatter.format_ex(ex_desc, ctx))

    def test_format_ex_invalidctx(self):
        '''This test case ensures an exception is raised if no valid context is provided.'''

        for formatter_ctx in [None, {}, {"attr": "invalid"}]:
            with self.assertRaises(KeyError) as ctx:
                self._formatter.format_ex(None, formatter_ctx)

            self.assertTrue(str(ctx.exception).find("redirect_uri") > -1)
