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
.. py:module:: fantastico.sdk.commands.tests.itest_command_activate_extension
'''
from fantastico.sdk.fantastico import main, SdkCore
from fantastico.sdk.commands.tests.itest_command_integration_base import CommandBaseIntegration
from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator
import os
import shutil

class SdkCommandActivateExtensionIntegration(CommandBaseIntegration):
    '''This class provides the test cases for ensuring correct functionality of activate-extension command.'''

    def test_activate_ok(self):
        '''This test case ensures an extension is activated correctly.'''

        extensions_folder = "tmp_modules"
        root_folder = instantiator.get_component_path_data(SettingsFacade().get_config().__class__)[1]

        extensions_path = "%s%s" % (root_folder, extensions_folder)

        if os.path.exists(extensions_path):
            shutil.rmtree(extensions_path)

        os.mkdir(extensions_path)

        argv = ["fantastico", "activate-extension", "--name", "dynamic_menu", "--comp-root", "tmp_modules"]

        main(argv)

        comp_path = "%s/dynamic_menu" % (extensions_path)

        self.assertTrue(os.path.exists(comp_path))
        self.assertTrue(os.path.exists("%s/tests" % comp_path))
        self.assertTrue(os.path.exists("%s/sql" % comp_path))
        self.assertTrue(os.path.exists("%s/menu_controller.py" % comp_path))
        self.assertTrue(os.path.exists("%s/menu_exceptions.py" % comp_path))
        self.assertTrue(os.path.exists("%s/__init__.py" % comp_path))
        self.assertFalse(os.path.exists("%s/models" % comp_path))

    def test_activate_help(self):
        '''This test case ensures help works as expected for activate-extension.'''

        from fantastico.sdk.commands.command_activate_extension import SdkCommandActivateExtension

        def assert_action(help_str):
            self.assertTrue(help_str.startswith("usage: %s" % SdkCommandActivateExtension.get_help()))
            self.assertTrue(help_str.find("-n NAME, --name NAME") > -1)
            self.assertTrue(help_str.find("-p COMP_ROOT, --comp-root COMP_ROOT") > -1)

        argv = [SdkCore.get_name(), "activate-extension"]

        self._exec_command_help_scenario(argv, assert_action, "activate-extension")
