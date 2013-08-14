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
.. py:module:: fantastico.contrib.dynamic_menu.tests.test_menu_controller
'''

from fantastico.contrib.dynamic_menu.menu_exceptions import FantasticoMenuNotFoundException
from fantastico.contrib.dynamic_menu.models.menus import DynamicMenuItem, DynamicMenu
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import json

class DynamicMenuControllerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases required for making sure dynamic menu offers specified functionality.'''

    _menu_contr = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies.'''

        from fantastico.contrib.dynamic_menu.menu_controller import DynamicMenuController

        self.check_original_methods(DynamicMenuController)

        self._menu_contr = DynamicMenuController(Mock())

    def test_menu_items_retrieved_ok(self):
        '''This test case ensures menu items are retrieved correctly for an existing menu identifier.'''

        menu_id = 1
        mock_items = [DynamicMenuItem("self", "test url", "Simple title", "Simple label", menu_id),
                      DynamicMenuItem("self", "test url 2", "Simple title 2", "Simple label 2", menu_id)]
        expected_items = [{"url": "test url", "target": "self", "title": "Simple title", "label": "Simple label"},
                          {"url": "test url 2", "target": "self", "title": "Simple title 2", "label": "Simple label 2"}]

        self._exec_retrieve_items_scenario(menu_id, mock_items, 2, expected_items)

    def test_no_menu_items_available(self):
        '''This test case ensures a menu without menu items retrieves a valid JSON object.'''

        menu_id = 1
        mock_items = None
        expected_items = []

        self._exec_retrieve_items_scenario(menu_id, mock_items, 0, expected_items)

    def test_menu_notfound(self):
        '''This test case ensures a concrete exception is thrown if the given menu identifier does not exist.'''

        menu_id = 1500
        menus_facade = Mock()

        request = Mock()
        request.models = Mock()
        request.models.Menus = menus_facade

        def find_by_pk(pk_value):
            self.assertEqual(pk_value, {DynamicMenu.id: menu_id})

            return None

        menus_facade.find_by_pk = find_by_pk

        with self.assertRaises(FantasticoMenuNotFoundException):
            self._menu_contr.retrieve_menu_items(request, menu_id)

    def _exec_retrieve_items_scenario(self, menu_id, mock_items, expected_items_len, expected_items):
        request = self._mock_retrieve_items_request(menu_id, mock_items)

        response = self._menu_contr.retrieve_menu_items(request, menu_id)

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.body)
        self.assertEqual(response.content_type, "application/json")

        body = json.loads(response.body.decode())

        self.assertIsNotNone(body)

        items = body.get("items")

        self.assertIsNotNone(items)
        self.assertEqual(len(items), expected_items_len)

        for i, item in enumerate(expected_items):
            self.assertEquals(items[i]["url"], item["url"])
            self.assertEquals(items[i]["target"], item["target"])
            self.assertEquals(items[i]["title"], item["title"])
            self.assertEquals(items[i]["label"], item["label"])

    def _mock_retrieve_items_request(self, menu_id, expected_items):
        '''This method is mocking all dependencies required in invoking retrieve_menu_items successfully. Mocks will return
        expected_items input'''

        request = Mock()
        items_facade = Mock()

        request.models = request
        request.models.Items = items_facade

        def get_records_paged(start_record, end_record, filter_expr):
            '''This method is used to simulate model facade get_records_paged method.'''

            self.assertEqual(start_record, 0)
            self.assertEqual(end_record, self._menu_contr.max_items)
            self.assertEqual(len(filter_expr), 1)

            filter_expr = filter_expr[0]
            self.assertEqual(filter_expr.column, DynamicMenuItem.menu_id)
            self.assertEqual(filter_expr.ref_value, menu_id)
            self.assertEqual(filter_expr.operation, ModelFilter.EQ)

            return expected_items

        items_facade.get_records_paged = get_records_paged

        return request
