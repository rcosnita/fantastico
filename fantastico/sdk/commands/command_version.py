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
.. py:module:: fantastico.sdk.commands.command_version
'''

from fantastico.sdk import sdk_decorators
from fantastico.sdk.sdk_core import SdkCommand
import fantastico

@sdk_decorators.SdkCommand(name="version", target="fantastico",
                           help="Displays fantastico sdk installed version.")
class SdkCommandVersion(SdkCommand):
    '''This class provides the command for finding out installed version of Fantastico SDK. The value is defined in fantastico
    root module code.

    .. code-block:: python

        # display help information for version command in sdk context
        fsdk version --help

        # display the current sdk version
        fsdk version
    '''

    def __init__(self, argv, cmd_factory, version_reader=fantastico):
        super(SdkCommandVersion, self).__init__(argv, cmd_factory)

        self._version = version_reader.__version__

    def get_arguments(self):
        return []

    def exec(self, print_fn=print):
        '''This method prints the current fantastico framework version.'''

        print_fn(self._version)
