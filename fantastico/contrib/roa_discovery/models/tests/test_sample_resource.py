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
.. py:module:: fantastico.contrib.roa_discovery.models.tests.test_sample_resource
'''
from fantastico.contrib.roa_discovery.models.sample_resource import SampleResource
from fantastico.tests.base_case import FantasticoUnitTestsCase

class SampleResourceTests(FantasticoUnitTestsCase):
    '''Ths class provides the test cases for ensuring sample resource works as expected.'''

    def test_instantiation_ok(self):
        '''This test case ensures sample resource can be correctly instantiated.'''

        expected_name = "test"
        expected_desc = "Friendly description"
        expected_total = 5.0
        expected_vat = 0.19

        model = SampleResource(name=expected_name, description=expected_desc, total=expected_total,
                               vat=expected_vat)

        self.assertEqual(model.name, expected_name)
        self.assertEqual(model.description, expected_desc)
        self.assertEqual(model.total, expected_total)
        self.assertEqual(model.vat, expected_vat)
