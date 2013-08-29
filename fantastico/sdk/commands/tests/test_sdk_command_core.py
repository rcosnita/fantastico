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
.. py:module:: fantastico.sdk.tests.test_sdk_command_core
'''

from fantastico.sdk.sdk_core import SdkCommandsRegistry
from fantastico.tests.base_case import FantasticoUnitTestsCase

class SdkCommandCoreTests(FantasticoUnitTestsCase):
    '''This class provides the unit tests for sdk command core. It covers autodiscovery of submodules.'''

    def init(self):
        '''This method is invoked automatically for preparing dependencies.'''

        SdkCommandsRegistry.COMMANDS.clear()

    def cleanup(self):
        '''This method is invoked automatically for cleaning dependencies.'''

        SdkCommandsRegistry.COMMANDS.clear()

    def test_core_command_ok(self):
        '''This test case ensures fantastico sdk main command works as expected.'''

        from fantastico.sdk.fantastico import SdkCore

        argv = ["fantastico", "test_cmd", "-h"]

        cmd = SdkCore(argv, SdkCommandsRegistry, ["tests", "commands_for_bdd_test"])

        SdkCommandsRegistry.add_command("fantastico", SdkCore)
        SdkCommandsRegistry.add_command("test_cmd", SdkCore)

        self.assertEqual("fantastico", cmd.get_name())
        self.assertIsNotNone(SdkCommandsRegistry.get_command("fantastico", argv))
