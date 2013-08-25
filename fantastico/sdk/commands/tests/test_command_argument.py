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
.. py:module:: fantastico.sdk.test.test_command_argument
'''
from fantastico.sdk.sdk_core import SdkCommandArgument
from fantastico.tests.base_case import FantasticoUnitTestsCase

class SdkCommandArgumentTests(FantasticoUnitTestsCase):
    '''This class provides the test cases which ensure command argument object provide the specified functionality.'''

    def test_arg_instantiation(self):
        '''This test case instantiate a command argument and ensures all attributes are correctly set. Moreover it ensures
        command argument attributes are readonly.'''

        expected_short_name = "t"
        expected_name = "test_argument"
        expected_type = int
        expected_help = "Simple help message"

        arg = SdkCommandArgument(arg_short_name=expected_short_name,
                                 arg_name=expected_name,
                                 arg_type=expected_type,
                                 arg_help=expected_help)

        self.assertEqual(expected_short_name, arg.short_name)
        self.assertEqual(expected_name, arg.name)
        self.assertEqual(expected_type, arg.type)
        self.assertEqual(expected_help, arg.help)

        for attr_name in ["short_name", "name", "type", "help"]:
            with self.assertRaises(AttributeError):
                setattr(arg, attr_name, "Simple test")
