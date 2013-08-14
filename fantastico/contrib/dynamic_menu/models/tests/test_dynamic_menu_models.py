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
.. py:module:: fantastico.contrib.dynamic_menu.tests.test_dynamic_menu_models
'''
from fantastico.contrib.dynamic_menu.models.menus import DynamicMenu, DynamicMenuItem
from fantastico.tests.base_case import FantasticoUnitTestsCase

class DynamicMenuModelTests(FantasticoUnitTestsCase):
    '''This class provides the unit tests for ensuring dynamic menu model objects can be correctly built.'''

    def test_dynamic_menu_ok(self):
        '''This test ensures DynamicMenu model object can be instantiated correctly.'''

        expected_name = "test menu"

        model = DynamicMenu(name=expected_name)

        self.assertEqual(model.name, expected_name)

    def test_dynamic_menu_item_ok(self):
        '''This test ensures DynamicMenuItem model object can be instantiated correctly.'''

        expected_target = "self"
        expected_url = "/test/url"
        expected_title = "test title"
        expected_label = "Simple label"
        expected_menu_id = 1

        model = DynamicMenuItem(expected_target, expected_url, expected_title, expected_label, expected_menu_id)

        self.assertEqual(model.target, expected_target)
        self.assertEqual(model.url, expected_url)
        self.assertEqual(model.title, expected_title)
        self.assertEqual(model.label, expected_label)
        self.assertEqual(model.menu_id, expected_menu_id)
