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
.. py:module:: fantastico.sdk.sdk_core
'''
from abc import ABCMeta, abstractmethod # pylint: disable=W0611
from argparse import Namespace
from fantastico.sdk.sdk_exceptions import FantasticoSdkCommandError, FantasticoSdkCommandNotFoundError
import argparse

class SdkCommandArgument(object):
    '''This class describe the attributes supported by a command argument. For a simple example of how arguments are used
    read :py:class:`fantastico.sdk.sdk_core.SdkCommand`'''

    @property
    def short_name(self):
        '''This read only property holds the argument short name. Short name property will represent the short name argument
        available for sdk commands. E.g: **-n**.'''

        return self._short_name

    @property
    def name(self):
        '''This read only property holds the argument name. Name property will represent the long name argument available for
        sdk commands. E.g: **--name**.'''

        return self._name

    @property
    def type(self):
        '''This read only property holds the argument type.'''

        return self._type

    @property
    def help(self):
        '''This read only property holds the argument help message.'''

        return self._help

    def __init__(self, arg_short_name, arg_name, arg_type, arg_help):
        self._short_name = arg_short_name
        self._name = arg_name
        self._type = arg_type
        self._help = arg_help

class SdkCommandsRegistry(object):
    '''This class holds all registered commands available to use in the sdk. It is important to understand that commands and
    subcommands are registered by name and must be unique. This is because, by design, each command can easily become a
    subcommand for another command. It facilitates very flexible extension of sdk and reusage of existing commands.'''

    COMMANDS = {}

    @staticmethod
    def add_command(cmd_name, cmd_cls):
        '''This method registers a new command using the given name.

        :param cmd_name: Command name used to uniquely identify the command.
        :type cmd_name: str
        :param cmd_class: A subclass of sdk command.
        :type cmd_class: :py:class:`fantastico.sdk.sdk_core.SdkCommand`
        :raise fantastico.sdk.sdk_exceptions.FantasticoSdkError: If the given name is not unique or cmd class is wrong.
        '''

        if not cmd_name or not cmd_name.strip():
            raise FantasticoSdkCommandError("No command name given for class %s." % cmd_cls)

        existing_cmd = SdkCommandsRegistry.COMMANDS.get(cmd_name)

        if existing_cmd:
            raise FantasticoSdkCommandError("Command %s already registered by class %s." % (cmd_name, existing_cmd))

        if not issubclass(cmd_cls, SdkCommand):
            raise FantasticoSdkCommandError("Command %s does not inherit fantastico.sdk.sdk_core.SdkCommand." % existing_cmd)

        SdkCommandsRegistry.COMMANDS[cmd_name] = cmd_cls

    @staticmethod
    def get_command(cmd_name, cmd_args):
        '''This method retrieve a concrete sdk command by name with the give args passed.

        :param cmd_name: The registered command name we want to instantiate.
        :type cmd_name: str
        :param cmd_args: a list of arguments received from command line.
        :type cmd_args: list
        :returns: Command instance.
        :rtype: :py:class:`fantastico.sdk.sdk_core.SdkCommand`
        :raise fantastico.sdk.sdk_exceptions.FantasticoSdkCommandNotFoundError: if command is not registered.
        '''

        cmd = SdkCommandsRegistry.COMMANDS.get(cmd_name)

        if not cmd:
            raise FantasticoSdkCommandNotFoundError("Command %s is not registered into sdk." % cmd_name)

        return cmd(cmd_args, SdkCommandsRegistry())

class SdkCommand(object, metaclass=ABCMeta):
    '''This class provides the contract which must be provided by each concrete command. A command of sdk is just and extension
    which can provide custom actions being executed by Fantastico in a uniform manner.

    Below you can find a simple example of how to implement a concrete command:

    .. code - block:: python

        from fantastico.sdk import sdk_decorators

        @sdk_decorators.SdkCommand(name="greet", cmd_help="This is a very simple greeting command supported by fantastico.")
        class SdkCommandSayHello(SdkCommand):
            \'\'\'This class provides an extremely simple command which greets the user.\'\'\'

            CMD_NAME = "greet"

            def get_arguments(self):
                return [SdkCommandArgument("-m", "--message", int, "Message used to greet the user."),
                        SdkCommandArgument(SdkCommandSayHello.CMD_NAME, SdkCommandSayHello.CMD_NAME, SdkCommandSayHello,
                                           "Recursive subcommand sample."]

            def exec(self):
                print(self._arguments.message)

        # now, when you execute: **fantastico greet --message "Hello world"**, Hello world message will be printed.

    In the previous example, we have shown that all received arguments from command line are magically provided into
    **self._arguments** attribute of the command.

    When a sdk command is instantiated with a list of command line arguments the first element from the list must be the command
    name. This happens because all arguments passed after a command name belongs only to that command.
    '''

    def __init__(self, argv, cmd_factory):
        '''
            :param argv: A list of arguments received from command line.
            :type argv: list
            :param cmd_factory: The factory currently used to instantiate commands by name.
            :type cmd_factory: :py:class:`fantastico.sdk.sdk_core.FantasticoCommandRegistry`
            :throws fantastico.sdk.sdk_exceptions.FantasticoSdkCommandError: If the list of arguments is not valid.'''

        if not argv:
            raise FantasticoSdkCommandError("You must provide arguments for sdk command %s" % self.get_name())

        if argv[0] != self.get_name():
            raise FantasticoSdkCommandError("Command %s is not equal with the current command %s" % \
                                            (argv[0], self.get_name()))

        self._cmd_factory = cmd_factory
        self._argv = argv[1:]
        self._arguments = None
        self._args_parser = None
        self._args_namespace = None

    @abstractmethod
    def get_arguments(self):
        '''This method must be overriden by each concrete command and must return the command supported arguments.'''

    @abstractmethod
    def exec(self):
        '''This method must be overriden by each concrete command and must provide the command execution logic.

        :raise fantastico.sdk.sdk_exceptions.FantasticoSdkCommandError: if an exception occurs while executing the command.'''

    def exec_command(self, *args, **kwargs):
        '''This method provides a template for executing the current command if subcommands are present. Internally it invokes
        overriden exec method.

        :raise fantastico.sdk.sdk_exceptions.FantasticoSdkCommandError: if an exception occurs while executing the command.
        :raise fantastico.sdk.sdk_exceptions.FantasticoSdkCommandNotFoundError: if a subcommand does not exist.'''

        self._arguments.subcommand = self._get_subcommand()

        if self._arguments.subcommand:
            try:
                return self._cmd_factory.get_command(self._argv[0], self._argv[0:]).exec_command(*args, **kwargs)
            except Exception as ex:
                raise FantasticoSdkCommandNotFoundError(ex)

        return self.exec(*args, **kwargs)

    def _get_subcommand(self):
        '''This method returns the subcommand given to current command.'''

        if len(self._argv) > 0 and not self._argv[0].startswith("-"):
            return self._argv[0]

    def _build_arguments(self):
        '''This method is invoked automatically by getattribute when _arguments attribute is first accessed. It builds the
        _arguments object which holds all attributes value passed from command line.'''

        self._args_parser = args_parser = argparse.ArgumentParser(self.get_help())

        supported_args = self.get_arguments()

        for cmd_arg in supported_args:
            if issubclass(cmd_arg.type, SdkCommand):
                args_parser.add_argument(cmd_arg.name, metavar=cmd_arg.name, type=str,
                                         help=cmd_arg.help, default=None, nargs="?")

        for cmd_arg in supported_args:
            if not issubclass(cmd_arg.type, SdkCommand):
                args_parser.add_argument(cmd_arg.short_name, cmd_arg.name, type=cmd_arg.type, help=cmd_arg.help)

        if self._get_subcommand():
            args_parser.parse_args([self._argv[0]], self._args_namespace)
        else:
            args_parser.parse_args(self._argv, self._args_namespace)

    def __getattribute__(self, attr_name):
        '''This method is invoked dynamically by python when trying to access object attributes. For SdkCommand it lazy build the
        arguments list at first invocation.'''

        if attr_name == "_arguments":
            if not self._args_namespace:
                self._args_namespace = Namespace()

                self._build_arguments()

            return self._args_namespace

        return super(SdkCommand, self).__getattribute__(attr_name)
