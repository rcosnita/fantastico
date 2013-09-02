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
.. py:module:: fantastico.sdk.commands.command_activate_extension
'''
from fantastico import contrib
from fantastico.sdk import sdk_decorators
from fantastico.sdk.sdk_core import SdkCommand, SdkCommandArgument
from fantastico.utils import instantiator
import os
from fantastico.sdk.sdk_exceptions import FantasticoSdkCommandNotFoundError
from fantastico.settings import SettingsFacade

CMD_HELP = "%s %s" % \
        ("Activates a local extension provided by fantastico. Currently it supports only local components found into",
         "fantastico.contrib package.")

@sdk_decorators.SdkCommand(
        name="activate-extension",
        help=CMD_HELP,
        target="fantastico")
class SdkCommandActivateExtension(SdkCommand):
    '''This class provides the functionality for activating off the shelf fantastico extensions. As developer, it is extremely
    easy to integrate provided functionality into fantastico. For now, it supports only local extensions provided into
    fantastico.contrib package. In the future, we plan to support activation of remote components into projects.

    .. code-block:: bash

        # replace <project_root_path> with your fantastico project location.
        cd <project_root_path>

        # replace <component_root_path> with your actual folder.
        fsdk activate-extension --name dynamic_menu --comp-root <component_root_path>'''

    def get_arguments(self):
        '''This method returns support arguments of activate-extension command.'''

        return [SdkCommandArgument(arg_short_name="-n",
                                   arg_name="--name",
                                   arg_type=str,
                                   arg_help="Holds the name of extension we want to activate."),
                SdkCommandArgument(arg_short_name="-p",
                                   arg_name="--comp-root",
                                   arg_type=str,
                                   arg_help="Holds the name of the folder where project components are placed.")]

    def exec(self, os_lib=os):
        '''This method is executed to activate the given extension name.'''

        comp_name = self._arguments.name
        contrib_path = instantiator.get_package_abslocation(contrib)
        comp_path = "%s%s" % (contrib_path, comp_name)

        if not os_lib.path.exists(comp_path):
            raise FantasticoSdkCommandNotFoundError("Extension %s does not exist." % comp_name)

        file_matcher = lambda abspath, filename: True
        root_folder = instantiator.get_component_path_data(SettingsFacade().get_config().__class__)[1]
        comp_root_folder = "%s%s/%s" % (root_folder, self._arguments.comp_root, comp_name)

        if not os_lib.path.exists(comp_root_folder):
            os_lib.mkdir(comp_root_folder)

        instantiator.scan_folder_by_criteria(
                            comp_path, file_matcher,
                            action=lambda abspath, filename: \
                                self._link_files(abspath, filename, contrib_path, root_folder, os_lib),
                            os_lib=os_lib)

    def _link_files(self, abspath, filename, contrib_path, root_folder, os_lib=os):
        '''This method holds the logic for linking a given comp repository absolute path to local repository.'''

        if filename == "models":
            return

        src = abspath
        dest = "%s%s/%s" % (root_folder, self._arguments.comp_root, src.replace(contrib_path, ""))

        if os_lib.path.exists(dest):
            os_lib.remove(dest)

        os_lib.symlink(src, dest)
