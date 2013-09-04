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
.. py:module:: fantastico.sdk.commands.tests.itest_command_integration_base
'''

from fantastico.sdk.fantastico import main
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoIntegrationTestCase
import io
import sys

class CommandBaseIntegration(FantasticoIntegrationTestCase):
    '''This class provides the raw frame for easily writing integration tests for fantastico sdk commands.'''

    _stdout = None
    _old_stdout = None

    def init(self):
        '''This method ensures standard output stream is replaced with a controllable one.'''

        self._old_stdout = sys.stdout
        sys.stdout = self._stdout = io.StringIO()

    def clean(self):
        '''This method ensures standard output stream is restored after each test case.'''

        sys.stdout = self._old_stdout
        self._stdout.close()

    def _exec_command_help_scenario(self, argv, assert_action, cmd_name):
        '''This method defines a template for testing subcommands --help option. Once the subcommand is executed, the help
        string is captured and passed to assert action.

        .. code-block:: python

            class SampleSubcommandTest(CommandBaseIntegration):
                def test_sample_help(self):
                    def assert_action(help_str):
                        self.help_str.startswith("usage: %s" % SampleSubcommand.get_help())

                    self._exec_command_help_scenario(["fantastico", "sample"], "sample")'''

        if argv[-1] != "--help" or "-h":
            argv.append("--help")

        with self.assertRaises(SystemExit):
            main(argv)

        help_str = self._stdout.getvalue()

        assert_action(help_str)

        expected_doc_link = "See: %sfeatures/sdk/command_%s.html" % (SettingsFacade().get("doc_base"), cmd_name.replace("-", "_"))
        self.assertGreater(help_str.find(expected_doc_link), -1)

