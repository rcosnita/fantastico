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
.. py:module:: fantastico.sdk.commands.command_syncdb
'''
from fantastico.sdk import sdk_decorators
from fantastico.sdk.sdk_core import SdkCommand, SdkCommandArgument
from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator
from subprocess import call
import os
from fantastico.sdk.sdk_exceptions import FantasticoSdkCommandError

CMD_NAME = "syncdb"

@sdk_decorators.SdkCommand(
        name=CMD_NAME,
        help="Create modules database structure and then insert data into all tables.",
        target="fantastico")
class SdkCommandSyncDb(SdkCommand):
    '''This class provides the algorithm for synchronizing **Fantastico** projects database scripts with the current configured
    database connection. Below you can find the order in which scripts are executed:

    #. Scan and execute all activated extensions sql/module_setup.sql scripts.
    #. Scan and execute all activated extensions for sql/create_data.sql scripts.

    **syncdb** command first required database structure for all modules and the it populates them with necessary data. It is
    important to understand that rollback procedures are not currently in place and there is no way to guarantee data integrity.
    All components providers are responsible for writing module_setup in such a way that in case of error data is left in a
    consistent state.

    For possible examples of how to structure a component read :doc:`/features/component_model`

    .. code-block:: bash

        fsdk syncdb --db-command /usr/bin/mysql --comp-root samples

    It is important to understand that this command will synchronize all module_setup / create_data sql scripts for current active
    settings. Read more about configuring fantastico on :doc:`/get_started/settings`.
    '''

    def __init__(self, args, cmd_factory, settings_facade_cls=SettingsFacade):
        super(SdkCommandSyncDb, self).__init__(args, cmd_factory)

        self._settings_facade = settings_facade_cls()

    def get_arguments(self):
        '''This method returns support arguments for **syncdb**:

        #. -d --db-command path to mysql command.
        #. -p --comp-root component root folder.
        '''

        return [SdkCommandArgument("-d", "--db-command", str, "Holds the location of sql command line. E.g: /usr/bin/mysql"),
                SdkCommandArgument("-p", "--comp-root", str, "Holds the name of the folder where project components are placed.")]

    def _is_file_supported(self):
        '''This method detects if the given filename is supported (module_setup.sql, create_data.sql).'''

        return True

    def _execute_script(self, filename, call_cmd):
        '''This method execute a given file using the sql command line.'''

        db_command = self._arguments.db_command
        db_config = self._settings_facade.get("database_config")

        cmd_args = {"cmd_name": db_command,
                    "script": filename}
        cmd_args.update(db_config)

        cmd = ["%(cmd_name)s --user=%(username)s --password=%(password)s -h %(host)s --database=%(database)s",
               " --port=%(port)s"]

        cmd_str = "".join(cmd) % cmd_args
        cmd = cmd_str.split(" ")
        cmd.append("-e")
        cmd.append("source %s" % filename)

        cmd_str += " -e \"source %s\"" % filename

        try:
            retcode = call_cmd(cmd)

            if retcode != 0:
                raise FantasticoSdkCommandError("Command %s execution failed. Error code: %s" % (cmd_str, retcode))
        except Exception as ex:
            raise FantasticoSdkCommandError(ex)

    def _execute_scripts(self, scripts, call_cmd):
        '''This method iterate over cached scripts and execute them using mysql command.'''

        for mod_setup in scripts["module_setup.sql"]:
            self._execute_script(mod_setup, call_cmd)

        for create_data in scripts["create_data.sql"]:
            self._execute_script(create_data, call_cmd)

    def exec(self, os_lib=os, call_cmd=call):
        '''This method executes module_setup.sql and create_data.sql scripts.

        :raises fantastico.sdk.sdk_exceptions.FantasticoSdkCommandError: When scripts execution fails unexpectedly.
        '''

        comp_folder = self._arguments.comp_root

        files = {"module_setup.sql": [],
                 "create_data.sql": []}

        scan_folder = lambda folder: instantiator.scan_folder_by_criteria(folder,
                                             file_matcher=lambda abspath, filename: self._is_file_supported(),
                                             action=store_file,
                                             os_lib=os_lib)

        def store_file(location, filename):
            '''This method stores all module_setup.sql and create_data.sql into a dictionary for future execution.'''

            if os_lib.path.isdir(location):
                return scan_folder(location)

            if filename not in ["module_setup.sql", "create_data.sql"]:
                return

            files[filename].append(location)

        scan_folder(comp_folder)

        self._execute_scripts(files, call_cmd)
