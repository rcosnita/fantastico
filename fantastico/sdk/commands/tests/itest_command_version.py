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
.. py:module:: fantastico.sdk.commands.tests.itest_command_version
'''

from fantastico.sdk.fantastico import SdkCore, main
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from mock import Mock
import fantastico
import io
import sys


class SdkCommandVersionIntegration(FantasticoIntegrationTestCase):
    '''This class provides the integration scenarios for sdk command **version**.'''

    _stdout = None
    _old_stdout = None
    _old_exit = None

    def init(self):
        '''This method ensures standard output stream is replaced with a controllable one.'''

        _old_exit = sys.exit
        sys.exit = Mock()

        self._old_stdout = sys.stdout
        sys.stdout = self._stdout = io.StringIO()

    def clean(self):
        '''This method ensures standard output stream is restored after each test case.'''

        sys.exit = self._old_exit
        sys.stdout = self._old_stdout
        self._stdout.close()

    def test_version_ok(self):
        '''This test case check version command integration into sdk.'''

        argv = [SdkCore.get_name(), "version"]

        main(argv)

        version = self._stdout.getvalue()

        self.assertTrue(version.startswith(fantastico.__version__))

    def test_version_help_ok(self):
        '''This test case check version command help screen is correctly generated.'''

        from fantastico.sdk.commands.command_version import SdkCommandVersion

        argv = [SdkCore.get_name(), "version", "--info"]

        main(argv)

        help_str = self._stdout.getvalue()

        self.assertTrue(help_str.startswith("usage: %s" % SdkCommandVersion.get_help()))
