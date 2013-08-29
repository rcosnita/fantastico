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
.. py:module:: fantastico.sdk.tests.test_sdk_command_registry
'''
from fantastico.sdk.sdk_core import SdkCommandsRegistry, SdkCommand
from fantastico.sdk.sdk_exceptions import FantasticoSdkCommandError, FantasticoSdkCommandNotFoundError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class SdkCommandsRegistryTests(FantasticoUnitTestsCase):
    '''This class provides the test cases which ensure sdk commands registry works as expected.'''

    _test_cmd_name = "test_cmd"

    _cmd_registry = None

    def init(self):
        '''This method setup a registry testing instance.'''

        self._cmd_registry = SdkCommandsRegistry
        self._cmd_registry.COMMANDS.clear()

    def cleanup(self):
        self._cmd_registry.COMMANDS.clear()

    def test_command_registration_ok(self):
        '''This test case ensures commands are registered correctly.'''

        self.assertEqual(0, len(self._cmd_registry.COMMANDS))

        self._cmd_registry.add_command(self._test_cmd_name, SdkCommandMock)

        self.assertEqual(1, len(self._cmd_registry.COMMANDS))
        self.assertEqual(SdkCommandMock, self._cmd_registry.COMMANDS.get(self._test_cmd_name))

    def test_command_registration_notunique(self):
        '''This test case ensures duplicates command registration fails.'''

        self.test_command_registration_ok()

        with self.assertRaises(FantasticoSdkCommandError):
            self._cmd_registry.add_command(self._test_cmd_name, SdkCommandMock)

    def test_command_registration_notacommand(self):
        '''This test case ensures that only SdkCommand subclasses can be registered.'''

        with self.assertRaises(FantasticoSdkCommandError):
            self._cmd_registry.add_command(self._test_cmd_name, Mock())

    def test_command_registration_noname(self):
        '''This test case ensures that an error is raised if no command name is given.'''

        for cmd_name in [None, "", "     "]:
            with self.assertRaises(FantasticoSdkCommandError):
                self._cmd_registry.add_command(cmd_name, SdkCommandMock)

    def test_command_retrieve_ok(self):
        '''This test case ensures command instantiation works as expected.'''

        self.test_command_registration_ok()

        cmd = self._cmd_registry.get_command(self._test_cmd_name, [self._test_cmd_name])

        self.assertIsInstance(cmd, SdkCommandMock)
        self.assertIsInstance(cmd.cmd_factory, SdkCommandsRegistry)

    def test_command_retrieve_notfound(self):
        '''This test case ensures a concrete exception is raised when we try to obtain a sdk command which is not registered.'''

        with self.assertRaises(FantasticoSdkCommandNotFoundError):
            self._cmd_registry.get_command("not_found", ["not_found"])

class SdkCommandMock(SdkCommand):
    '''Very simple sdk mock command.'''

    @property
    def cmd_factory(self):
        return self._cmd_factory

    def get_name(self):
        return "test_cmd"

    def get_arguments(self):
        return []

    def get_help(self):
        return ""

    def exec(self):
        pass
