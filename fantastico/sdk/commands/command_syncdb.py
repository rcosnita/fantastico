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
from fantastico.sdk.sdk_core import SdkCommand
from fantastico.sdk import sdk_decorators

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
    '''
