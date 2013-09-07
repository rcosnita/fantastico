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
.. py:module:: fantastico.sdk.sdk_decorators
'''
from fantastico.sdk.sdk_core import SdkCommandsRegistry
from fantastico.settings import SettingsFacade

class SdkCommand(object):
    '''This decorator describe the sdk commands metadata:

    #. name
    #. target (which is the main purpose of the command. E.g: fantastico - this mean command is designed to work as a subcommand for fantastico cmd).
    #. help (which describes what this method does). It will automatically contain a link to official fantastico documentation of the command.

    It is used in conjunction with :py:class:`fantastico.sdk.sdk_core.SdkCommand`. Each sdk command decorated with this
    decorator automatically receives **get_name** and **get_target** methods.'''

    def __init__(self, name, help, target=None, settings_facade_cls=SettingsFacade):
        self._name = name
        self._target = target
        self._help = help
        self._settings_facade = settings_facade_cls()

    def _get_help(self):
        '''This method returns the friendly help message describing the method.'''

        doc_link = "%sfeatures/sdk/command_%s.html" % (self._settings_facade.get("doc_base"), self._name.replace("-", "_"))

        return "%s...  See: %s" % (self._help, doc_link)

    def __call__(self, cls):
        '''This method simply adds get_name method to the command class.'''

        cls.get_name = lambda ctx = None: self._name
        cls.get_help = self._get_help
        cls.get_target = lambda ctx = None: self._target

        SdkCommandsRegistry.add_command(self._name, cls)

        return cls
