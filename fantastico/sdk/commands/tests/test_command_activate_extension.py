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
.. py:module:: fantastico.sdk.commands.tests.test_command_activate_extension
'''
from fantastico import contrib
from fantastico.sdk.commands.command_activate_extension import SdkCommandActivateExtension
from fantastico.sdk.sdk_exceptions import FantasticoSdkCommandNotFoundError
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils import instantiator
from mock import Mock


class SdkCommandActivateExtensionTests(FantasticoUnitTestsCase):
    '''This class provides the test cases required to make sure activate-extension command works as expected.'''

    _mocked_os = None
    _mocked_os_path = None

    def init(self):
        '''This method mocks all common dependencies.'''

        self._mocked_os = Mock()
        self._mocked_os_path = Mock()

        self._mocked_os.path = self._mocked_os_path

    def test_activate_extenstion_notfound(self):
        '''This test case ensures a concrete exception is thrown when we try to activate an inexistent extension.'''

        comp_name = "component-not-found-triplex"
        expected_comp_path = "%s%s" % (instantiator.get_package_abslocation(contrib), comp_name)

        self._mocked_os_path.exists = Mock(return_value=False)

        argv = [SdkCommandActivateExtension.get_name(), "--name", comp_name, "--comp-root", "samples"]

        cmd_activate = SdkCommandActivateExtension(argv, cmd_factory=None)

        with self.assertRaises(FantasticoSdkCommandNotFoundError):
            cmd_activate.exec_command(self._mocked_os)

        self._mocked_os_path.exists.assert_called_once_with(expected_comp_path)

    def test_activate_extension_short_ok(self):
        '''This method ensures activate-extension correctly creates the symlink on filesystem.'''

        comp_name = "dynamic-menu"
        comp_root_folder = "fantastico/samples"
        argv = [SdkCommandActivateExtension.get_name(), "-n", comp_name, "-p", comp_root_folder]

        self._mock_activate_ok_scenario(comp_name, comp_root_folder, argv)

    def test_activate_extension_long_ok(self):
        '''This method ensures activate-extension correctly creates the symlink on filesystem.'''

        comp_name = "dynamic-menu"
        comp_root_folder = "fantastico/samples"
        argv = [SdkCommandActivateExtension.get_name(), "--name", comp_name, "--comp-root", comp_root_folder]

        self._mock_activate_ok_scenario(comp_name, comp_root_folder, argv)

    def _mock_activate_ok_scenario(self, comp_name, comp_root_folder, argv):
        '''This method mocks the success scenario for activate extension.'''

        root_folder = instantiator.get_component_path_data(SettingsFacade().get_config().__class__)[1]
        comp_root = "%s%s/%s" % (root_folder, comp_root_folder, comp_name)
        expected_comp_path = "%s%s" % (instantiator.get_package_abslocation(contrib), comp_name)

        comp_structure = ["__init__.py", "sql", "models", "dynamic_menus.py"]

        linking_trace = {}
        remove_trace = []

        def list_comp(dirname):
            '''This method mocks listdir method from os library.'''

            if dirname == expected_comp_path:
                return comp_structure

        def symlink(src, dest, holder=linking_trace):
            '''This method mocks the symlink method from os library.'''

            holder[src] = dest

        def file_exists(filename):
            if filename == comp_root:
                return False

            return True

        def remove(filename, remove_trace=remove_trace):
            remove_trace.append(filename)

        self._mocked_os.path.exists = file_exists
        self._mocked_os.remove = remove
        self._mocked_os.mkdir = Mock()
        self._mocked_os.listdir = list_comp
        self._mocked_os.symlink = symlink

        cmd_activate = SdkCommandActivateExtension(argv, cmd_factory=None)

        cmd_activate.exec_command(os_lib=self._mocked_os)

        self._assert_ok_scenario_results(comp_structure, expected_comp_path, linking_trace, remove_trace, comp_root)

    def _assert_ok_scenario_results(self, comp_structure, expected_comp_path, linking_trace, remove_trace, comp_root):
        '''This method asserts the result of ok scenario.'''

        for expected_file in comp_structure:
            src = "%s/%s" % (expected_comp_path, expected_file)

            if expected_file == "models":
                self.assertIsNone(linking_trace.get(src))

                continue

            dest = "%s/%s" % (comp_root, expected_file)

            self.assertEqual(linking_trace[src], dest)
            self.assertTrue(dest in remove_trace)

        self._mocked_os.mkdir.assert_called_with(comp_root)
