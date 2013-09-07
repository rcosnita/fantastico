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
.. py:module:: fantastico.sdk.commands.tests.test_command_syncdb
'''
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from fantastico.sdk.commands.command_syncdb import SdkCommandSyncDb
from fantastico.sdk.sdk_exceptions import FantasticoSdkCommandError

class SdkCommandSyncDbTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for checking that syncdb command works as expected.'''

    def test_syncdb_ok_long(self):
        '''This test case ensures syncdb command detects all module_setup / create_data sql files using long name arguments.'''

        db_command = "/usr/bin/mysql"
        comp_root = "samples"
        args = ["syncdb", "--db-command", db_command, "--comp-root", comp_root]

        self._test_syncdb_ok_scenario(args, db_command, comp_root)

    def test_syncdb_ok_short(self):
        '''This test case ensures syncdb command detects all module_setup / create_data sql files using short name arguments.'''

        db_command = "/usr/bin/mysql"
        comp_root = "samples"
        args = ["syncdb", "-d", db_command, "-p", comp_root]

        self._test_syncdb_ok_scenario(args, db_command, comp_root)

    def test_syncdb_unexpected_code(self):
        '''This test case covers scenario where one script execution is failing (exit code <> 0).'''

        db_command = "/usr/bin/mysql"
        comp_root = "samples"
        args = ["syncdb", "-d", db_command, "-p", comp_root]

        call_cmd = Mock(return_value= -5)

        with self.assertRaises(FantasticoSdkCommandError):
            self._test_syncdb_ok_scenario(args, db_command, comp_root, call_cmd=call_cmd)

    def test_syncdb_unexpected_oserror(self):
        '''This test case cover scenario where an os error is raised when invoking a command.'''

        self._test_syncdb_errors_scenario(OSError, "Unexpected exception")

    def test_syncdb_unexpected_exception(self):
        '''This test case cover scenario where an exception is raised when invoking a command.'''

        self._test_syncdb_errors_scenario(Exception, "Unexpected exception")

    def _test_syncdb_errors_scenario(self, err_cls, err_msg):
        '''This method defines a reusable test scenario for syncdb command which covers unexpected errors.'''

        db_command = "/usr/bin/mysql"
        comp_root = "samples"
        args = ["syncdb", "-d", db_command, "-p", comp_root]

        call_cmd = Mock(side_effect=err_cls(err_msg))

        with self.assertRaises(FantasticoSdkCommandError) as ctx:
            self._test_syncdb_ok_scenario(args, db_command, comp_root, call_cmd=call_cmd)

        self.assertEqual(str(ctx.exception), err_msg)


    def _mock_list_dir(self, folders_visited, main_folders, sql_content):
        '''This method return a mocked listdir function.'''

        def list_dirs(filename):
            folders_visited.append(filename)

            if filename == "samples":
                return main_folders

            if filename == "samples/sql":
                return sql_content

        return list_dirs

    def _mock_isdir(self, files_visited):
        '''This method return a mocked isdir function.'''

        def isdir(folder):
            if folder in ["samples/sql", "samples"]:
                return True

            files_visited.append(folder)

        return isdir

    def _mock_callcmd(self, cmd, cmd_executed):
        '''This method mocks shell command invocation. It appends all executed commands to a given array.'''

        self.assertIsInstance(cmd, list)

        cmd_executed.append(" ".join(cmd))

        return 0

    def _test_syncdb_ok_scenario(self, args, db_command, comp_root, listdir=None, isdir=None, call_cmd=None):
        '''This method provides a template for syncdb success scenario.'''

        folders_visited = []
        files_visited = []
        cmd_executed = []

        main_folders = ["sql", "test_script.sql"]
        sql_content = ["module_setup.sql", "create_data.sql"]

        listdir = listdir or self._mock_list_dir(folders_visited, main_folders, sql_content)
        isdir = isdir or self._mock_isdir(files_visited)
        call_cmd = call_cmd or (lambda cmd: self._mock_callcmd(cmd, cmd_executed))

        def get(name):
            self.assertEqual(name, "database_config")

            return {"username": "test_user",
                    "password": "12345",
                    "port": 3306,
                    "host": "localhost",
                    "database": "testdb"}

        settings_facade = Mock()
        settings_facade.get = get
        settings_facade_cls = Mock(return_value=settings_facade)

        mock_os = Mock()

        mock_os.listdir = listdir
        mock_os.path = Mock(return_value=mock_os)
        mock_os.path.isdir = isdir

        cmd = SdkCommandSyncDb(args, cmd_factory=Mock(), settings_facade_cls=settings_facade_cls)
        cmd.exec_command(os_lib=mock_os, call_cmd=call_cmd)

        self.assertTrue(comp_root in folders_visited)
        self.assertTrue("%s/sql" % comp_root in folders_visited)
        self.assertTrue("%s/sql/module_setup.sql" % comp_root in files_visited)
        self.assertTrue("%s/sql/create_data.sql" % comp_root in files_visited)

        expected_cmds = ["%s --user=test_user --password=12345 -h localhost --database=testdb --port=3306 -e source samples/sql/module_setup.sql" % db_command,
                         "%s --user=test_user --password=12345 -h localhost --database=testdb --port=3306 -e source samples/sql/create_data.sql" % db_command]

        for cmd in expected_cmds:
            self.assertTrue(cmd in cmd_executed)
