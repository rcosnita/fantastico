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
.. py:module:: fantastico.sdk.sdk_exceptions
'''
from fantastico.exceptions import FantasticoError

class FantasticoSdkError(FantasticoError):
    '''This is the base exception used to describe unexpected situations occuring into fantastico sdk. Below you can see the
    sdk hierarchy of concrete exceptions.

    .. image:: /images/sdk/exceptions.png
    '''

class FantasticoSdkCommandError(FantasticoSdkError):
    '''This class describe an exception which occured into one of fantastico sdk commands.'''

class FantasticoSdkCommandNotFoundError(FantasticoSdkError):
    '''This class describe an exception which occurs when we try to execute an inexistent command.'''
