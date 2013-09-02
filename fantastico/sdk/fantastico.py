#!/usr/bin/env python3

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
.. py:module:: fantastico.sdk.fantastico
'''
from fantastico.sdk import sdk_decorators
from fantastico.sdk.sdk_core import SdkCommand, SdkCommandsRegistry, SdkCommandArgument
from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator

@sdk_decorators.SdkCommand(
            name="fantastico",
            help="Fantastico Software Development Kit command line. Please use [subcommands] --help for more information.")
class SdkCore(SdkCommand):
    '''This class provides the core functionality of Fantastico Software Development Kit. It
    wires all available commands together and handles requests accordingly.
    To better understand how sdk is designed see the following class diagram:

    .. image:: /images/sdk/design.png

    As you can see in above diagram, sdk core is just the main entry point of Fantastico Software Development Kit. It wires
    all available sdk commands together and it adds support for uniformly executes them and pass them arguments..'''

    _COMMANDS_FOLDER = "commands"
    _COMMANDS_PREFIX = "command_"

    def __init__(self, argv, cmd_factory=SdkCommandsRegistry, supported_prefixes=None, settings_facade_cls=SettingsFacade):
        super(SdkCore, self).__init__(argv, cmd_factory)

        self._settings_facade = settings_facade_cls()
        self._core_args = []

        self._register_subcommands(supported_prefixes or [SdkCore._COMMANDS_PREFIX])

    def _register_subcommands(self, supported_prefixes):
        '''This methods loads all available subcommands from sdk and build _arguments supported by fantastico sdk directly.'''

        def is_file_supported(filename):
            '''This method decides if a filename is supported as possible subcommand provider module or not.'''

            for prefix in supported_prefixes:
                if filename.startswith(prefix):
                    return True

            return False

        local_folder = "%s%s/" % (instantiator.get_class_abslocation(SdkCore), SdkCore._COMMANDS_FOLDER)

        instantiator.import_modules_from_folder(local_folder,
                                                lambda folder, filename: is_file_supported(filename),
                                                self._settings_facade)

        self._register_root_subcommands()

    def _register_root_subcommands(self):
        '''This methods looks into the registry of available commands and obtain only those with target = 'fantastico'.'''

        for cmd in SdkCommandsRegistry.COMMANDS.values():
            if cmd.get_target() != self.get_name() or cmd.get_name() == self.get_name():
                continue

            self._core_args.append(SdkCommandArgument(cmd.get_name(), cmd.get_name(), cmd, cmd.get_help()))

    def get_arguments(self):
        '''This property retrieves support fantastico arguments.'''

        return self._core_args

    def exec(self):
        '''This method does nothing because fantastico is designed to accept only registered subcommands.'''

        pass

def main(argv):
    '''This method is used to trigger fantastico command line sdk.'''

    cmd_name = SdkCore.get_name()
    argv[0] = cmd_name

    cmd = SdkCommandsRegistry.get_command(cmd_name, argv)
    cmd.exec_command()
