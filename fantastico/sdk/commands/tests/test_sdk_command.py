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
.. py:module:: fantastico.sdk.tests.test_sdk_command
'''

from fantastico.sdk import sdk_decorators
from fantastico.sdk.sdk_core import SdkCommand, SdkCommandArgument
from fantastico.sdk.sdk_exceptions import FantasticoSdkCommandError, FantasticoSdkCommandNotFoundError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class SdkCommandTests(FantasticoUnitTestsCase):
    '''This class provides test cases for ensuring sdk command behaves as expected. The logic of this test suite is fairly simple:

        # It provides the command described into :py:class:`fantastico.sdk.sdk_core.SdkCommand`.
        # It ensures each single method work as expected when executed.'''

    def test_cmd_short_exec_ok(self):
        '''This test case ensures normal flow execution of the command works as expected for short arguments.'''

        expected_msg = "Message used to greet the user."

        args = [SdkCommandSayHello.CMD_NAME, "-m", expected_msg]

        self._exec_ok_scenario(args, expected_msg)

    def test_cmd_long_exec_ok(self):
        '''This test case ensures normal flow execution of the command works as expected for long arguments.'''

        expected_msg = "Message used to greet the user."

        args = [SdkCommandSayHello.CMD_NAME, "--message", expected_msg]

        self._exec_ok_scenario(args, expected_msg)

    def test_instantiation_fails_command_name_incompatible(self):
        '''This test case ensures the command instantiation fails if the first argument is not the command name.'''

        with self.assertRaises(FantasticoSdkCommandError):
            SdkCommandSayHello(["bla bla bla"], None)

    def test_instantiation_fails_no_args(self):
        '''This test case ensures command can not be instantiated when no arguments are given.'''

        for args in [None, []]:
            with self.assertRaises(FantasticoSdkCommandError):
                SdkCommandSayHello(args, None)

    def test_subcommand_sayhello_ok(self):
        '''This test case ensures subcommands execution works as expected.'''

        expected_msg = "Message used to greet the user."
        args = ["greet", "greet", "-m", expected_msg]
        cmd_factory = Mock()
        cmd_factory.get_command = Mock(return_value=SdkCommandSayHello(args[1:], None))

        self._exec_ok_scenario(args, expected_msg, cmd_factory)

        cmd_factory.get_command.assert_called_with("greet", args[1:])

    def test_subcommand_sayhello_cmdnotfound(self):
        '''This test case ensures not found subcommands are signaled through a concrete exception.'''

        expected_err_msg = "Command not found"
        expected_msg = "Message used to greet the user."
        args = ["greet", "greet", "-m", expected_msg]
        cmd_factory = Mock()
        cmd_factory.get_command = Mock(side_effect=Exception(expected_err_msg))

        with self.assertRaises(FantasticoSdkCommandNotFoundError) as ctx:
            self._exec_ok_scenario(args, expected_msg, cmd_factory)

        self.assertEqual(expected_err_msg, str(ctx.exception))

    def test_subcommand_gethelp_with_doclink(self):
        '''This test case ensures help message also include a link to official documentation.'''

        args = ["greet"]
        expected_doc_link = "See: https://rcosnita.github.io/fantastico/html/features/sdk/command_greet.html"

        cmd = SdkCommandSayHello(args, cmd_factory=Mock())

        help_msg = cmd.get_help()

        self.assertTrue(help_msg.startswith("This is a very simple greeting command supported by fantastico."))
        self.assertGreater(help_msg.find(expected_doc_link), -1)

    def _exec_ok_scenario(self, args, expected_msg, cmd_factory=None):
        '''This test case provides the template for checking correct behavior of exec method.'''

        mock_print = Mock(return_value=None)

        cmd = SdkCommandSayHello(args, cmd_factory)

        self.assertEqual("greet", cmd.get_name())
        self.assertEqual("example", cmd.get_target())

        cmd.exec_command(mock_print)

        mock_print.assert_called_with(expected_msg)

class SettingsFacadeMock():
    '''A very simple mock object which simulates settings facade. It only supports doc base property.'''

    def get(self, name):
        return "https://rcosnita.github.io/fantastico/html/"

@sdk_decorators.SdkCommand(name="greet",
                           help="This is a very simple greeting command supported by fantastico.",
                           target="example",
                           settings_facade_cls=SettingsFacadeMock)
class SdkCommandSayHello(SdkCommand):
    '''This class provides an extremely simple command which greets the user.'''

    CMD_NAME = "greet"

    def get_arguments(self):
        return [SdkCommandArgument("-m", "--message", str, "Message used to greet the user."),
                SdkCommandArgument(arg_short_name=SdkCommandSayHello.CMD_NAME,
                                   arg_name=SdkCommandSayHello.CMD_NAME,
                                   arg_type=SdkCommandSayHello,
                                   arg_help="Subcommand greet recursive execution.")]

    def exec(self, print_fn=print):
        print_fn(self._arguments.message)
