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
.. py:module:: fantastico.sdk.commands.tests.itest_command_syncdb
'''
from fantastico.sdk.commands.tests.itest_command_integration_base import CommandBaseIntegration
from fantastico.sdk.fantastico import SdkCore, main
from fantastico.settings import BasicSettings
from fantastico.utils import instantiator

class SdkSyncDbCommandIntegration(CommandBaseIntegration):
    '''This class provides the integration tests suite for ensuring syncdb command works as expected.'''

    _comp_root = None

    def init(self):
        '''This method is executed before each test case in order to setup common dependencies.'''

        self._comp_root = instantiator.get_class_abslocation(BasicSettings)

    def test_syncdb_mysql(self):
        '''This test case ensures syncdb works great for mysql database.'''

        argv = [SdkCore.get_name(), "syncdb", "--comp-root", self._comp_root, "--db-command", "/usr/bin/mysql"]

        main(argv)
