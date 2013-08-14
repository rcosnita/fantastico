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
.. py:module:: fantastico.contrib.dynamic_menu.models.menu
'''
from fantastico.mvc import BASEMODEL
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship

class DynamicMenu(BASEMODEL):
    '''This class defines supported attributes for a dynamic menu. In this version, users can easily define the following menu
    attributes:

    #. Menu unique identifier (read only).
    #. Menu name.'''

    __tablename__ = "menus"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(150), nullable=False)

    def __init__(self, name):
        '''This constructor initialize the menu with desired name.

        :param name: Dynamic menu friendly name.
        :type name: string
        '''

        self.name = name

class DynamicMenuItem(BASEMODEL):
    '''This class defines supported attributes for a dynamic menu item. In this version, users can easily define the following
    menu item attributes:

    #. Item unique identifier.
    #. A target which will display the menu url. Currently, all http targets are valid.
    #. Item url where user will be redirected after click / tap.
    #. Item friendly title which will be displayed in environments which support tooltips.
    #. Item label displayed to user.
    '''

    __tablename__ = "menu_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    target = Column("target", String(50), nullable=False)
    url = Column("url", String(255), nullable=False)
    title = Column("title", String(255), nullable=False)
    label = Column("label", String(255), nullable=False)

    menu_id = Column("menu_id", Integer, ForeignKey(DynamicMenu.id))
    menu = relationship(DynamicMenu, primaryjoin=menu_id == DynamicMenu.id)

    def __init__(self, target, url, title, label, menu_id):
        '''This constructor initialized all mandatory attributes of a dynamic menu item.'''

        self.target = target
        self.url = url
        self.title = title
        self.label = label
        self.menu_id = menu_id
