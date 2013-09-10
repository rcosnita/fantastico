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
.. py:module:: fantastico.contrib.dynamic_pages.tests.test_dynamicpage
'''
from fantastico.contrib.dynamic_pages.models.pages import DynamicPageModel
from fantastico.tests.base_case import FantasticoUnitTestsCase

class DynamicPageModelTests(FantasticoUnitTestsCase):
    '''This class provides all test cases required to ensure DynamicPageModel works as expected.'''

    def test_dynamicpage_model_defaults(self):
        '''This test case make sure a dynamic page model can be instantiated without any attribute.'''

        page_model = DynamicPageModel()

        self.assertIsNone(page_model.entry_id)
        self.assertIsNone(page_model.page_id)
        self.assertIsNone(page_model.name)
        self.assertIsNone(page_model.value)

    def test_dynamic_pagemodel_instantiation(self):
        '''This test case ensures given attributes are set correctly to page model.'''

        expected_page_id = 1
        expected_name = "simple_attribute"
        expected_value = "<p>Simple test</p>"

        page_model = DynamicPageModel(page_id=expected_page_id,
                                      name=expected_name,
                                      value=expected_value)

        self.assertIsNone(page_model.entry_id)
        self.assertEqual(page_model.name, expected_name)
        self.assertEqual(page_model.value, expected_value)
