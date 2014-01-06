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
.. py:module:: fantastico.tests.test_form_exception_formatter
'''
from fantastico.exception_formatters import FormUrlEncodedExceptionFormatter
from fantastico.tests.base_case import FantasticoUnitTestsCase
import urllib

class FormUrlEncodedExceptionFormatterTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for FormUrlEncodedExceptionFormatter.'''

    _formatter = None

    def init(self):
        '''This method is invoked automatically to setup common dependencies for all test cases.'''

        self._formatter = FormUrlEncodedExceptionFormatter()

    def test_format_ex_ok(self):
        '''This test case ensures a given exception descriptor is correctly formatted.'''

        ex_desc = {"attr1": "sample", "attr2": "value cool"}
        ctx = {"redirect_uri": "/example/cb"}

        expected_response = "%s?attr1=%s&attr2=%s" % (ctx["redirect_uri"], ex_desc["attr1"],
                                                      urllib.parse.quote(ex_desc["attr2"]))

        self.assertEqual(expected_response, self._formatter.format_ex(ex_desc, ctx))

    def test_format_ex_withhash_ok(self):
        '''This test case ensures all query parameters are correctly appended even when the redirect uri contains hash part.'''

        ex_desc = {"attr1": "sample", "attr2": "value"}
        ctx = {"redirect_uri": "/example/cb#hashf"}

        expected_response = "/example/cb?attr1=%s&attr2=%s#hashf" % (ex_desc["attr1"], ex_desc["attr2"])

        self.assertEqual(expected_response, self._formatter.format_ex(ex_desc, ctx))

    def test_format_ex_withqueryparams_ok(self):
        '''This test case ensures all query parameters are correctly appended even when redirect_uri already contains query
        params.'''

        ex_desc = {"attr1": "sample", "attr2": "value"}
        ctx = {"redirect_uri": "/example/cb?existing_param=q1"}

        expected_response = "%s&attr1=%s&attr2=%s" % (ctx["redirect_uri"], ex_desc["attr1"], ex_desc["attr2"])

        self.assertEqual(expected_response, self._formatter.format_ex(ex_desc, ctx))

    def test_format_ex_nodescriptor(self):
        '''This test case ensures the redirect uri is not altered if the given exception descriptor is None.'''

        ctx = {"redirect_uri": "/example/cb?existing_param=q1"}

        self.assertEqual(ctx["redirect_uri"], self._formatter.format_ex(None, ctx))

    def test_format_ex_novalidctx(self):
        '''This test case ensures an exception is raised if redirect_uri is not specified in the context.'''

        for formatter_ctx in [None, {}, {"attr": "abc"}]:
            with self.assertRaises(KeyError) as ctx:
                self._formatter.format_ex({}, formatter_ctx)

            self.assertTrue(str(ctx.exception).find("redirect_uri") > -1)
