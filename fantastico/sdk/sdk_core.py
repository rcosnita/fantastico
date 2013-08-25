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

class SdkCore(object):
    '''This class provides the core functionality of Fantastico Software Development Kit. It
    wires all available commands together and handles requests accordingly.
    To better understand how sdk is designed see the following class diagram:

    .. image:: /images/sdk/design.png

    As you can see in above diagram, sdk core is just the main entry point of Fantastico Software Development Kit. It wires
    all available sdk commands together and it adds support for uniformly executes them and pass them arguments..'''

class SdkCommandArgument(object):
    '''This class describe the attributes supported by a command argument.'''

    @property
    def name(self):
        '''This read only property holds the argument name.'''

        return self._name

    @property
    def type(self):
        '''This read only property holds the argument type.'''

        return self._type

    @property
    def help(self):
        '''This read only property holds the argument help message.'''

        return self._help

    def __init__(self, arg_name, arg_type, arg_help):
        self._name = arg_name
        self._type = arg_type
        self._help = arg_help
