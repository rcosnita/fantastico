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
.. py:module:: fantastico.sdk.commands.tests.test_command_version
'''
from fantastico.sdk.commands.command_version import SdkCommandVersion
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class SdkCommandVersionTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for ensuring sdk version command works as expected.'''

    def test_version_ok(self):
        '''This test case ensures correct version is retrieved by the command.'''

        expected_version = "0.99"

        argv = ["version"]
        version_reader = Mock()
        version_reader.__version__ = expected_version

        cmd = SdkCommandVersion(argv, Mock(), version_reader)

        mock_print = Mock()

        cmd.exec(mock_print)

        mock_print.assert_called_with(expected_version)
