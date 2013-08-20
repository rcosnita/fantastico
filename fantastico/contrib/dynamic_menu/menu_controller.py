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
.. py:module:: fantastico.contrib.dynamic_menu.menu_controller
'''
from fantastico.contrib.dynamic_menu.menu_exceptions import FantasticoMenuNotFoundException
from fantastico.contrib.dynamic_menu.models.menus import DynamicMenuItem, DynamicMenu
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import ControllerProvider, Controller
from fantastico.mvc.models.model_filter import ModelFilter
from webob.response import Response
import json

@ControllerProvider()
class DynamicMenuController(BaseController):
    '''This class provides the controller for dynamic menus. The following routes are automatically made available
    when dynamic menu component is deployed:

        **/dynamic-menu/menus/<menu_id>/items/** -- This route loads menu items from database and retrieve them in json format.

    Below you can see a diagram describing relation model of the menu:

    .. image:: /images/components/dynamic_menu/erd.png
    '''

    ITEMS_URL = "/dynamic-menu/menus/(?P<menu_id>\\d{1,})/items/$"

    @property
    def max_items(self):
        '''This property retrieves the maximum number of items allowed for a menu.'''

        return 100

    @Controller(url=ITEMS_URL, method="GET",
                models={"Menus": "fantastico.contrib.dynamic_menu.models.menus.DynamicMenu",
                        "Items": "fantastico.contrib.dynamic_menu.models.menus.DynamicMenuItem"})
    def retrieve_menu_items(self, request, menu_id):
        '''This method is used to retrieve all items associated with a specified menu.

        :param request: Http request being processed.
        :type request: HTTP request
        :param menu_id: Menu unique identifier we want to retrieve information for.
        :type menu_id: int
        :returns: A JSON array containing all available menu items.
        :raises fantastico.contrib.dynamic_menu.menu_exceptions.FantasticoMenuNotFoundException:
            Whenever the requested menu does not exist.
        '''

        menu_id = int(menu_id)

        menus_facade = request.models.Menus

        if not menus_facade.find_by_pk({DynamicMenu.id: menu_id}):
            raise FantasticoMenuNotFoundException("Menu %s does not exist." % menu_id)

        items_facade = request.models.Items

        items = items_facade.get_records_paged(start_record=0, end_record=self.max_items,
                                               filter_expr=[ModelFilter(DynamicMenuItem.menu_id, menu_id, ModelFilter.EQ)])
        items = [{"url": item.url,
                  "target": item.target,
                  "title": item.title,
                  "label": item.label} for item in items or []]

        body = json.dumps({"items": items})

        return Response(body, content_type="application/json")
