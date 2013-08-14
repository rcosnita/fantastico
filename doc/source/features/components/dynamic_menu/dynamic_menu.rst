Dynamic menu
============

Menus are a core part of every web site / application as well as mobile applications. More over, again and again
developers will want a quick way to define menu items without actually redefining menu data structure again and again.
This component which we generic named dynamic menu simply provides the controller and the model for easy development of menus.

Integration
-----------

In order to use dynamic menu component within your project follow the steps below:

#. Create a symbolic link to your root component folder to dynamic_menu.

   .. code-block:: bash

      ln -s pip-deps/python[version]/site-packages/fantastico/contrib/dynamic_menu .

#. Create a template in one of your components in which you define the menu view:

   .. code-block:: html

      <!-- *sample_menu.html* - simple snippet for creating a left / right side dockable menu. -->
      {% for menu_item in model.menu_items %}
         <a href="{{menu_item.url}}" title="{{menu_item.title}}" target="{{menu_item.target}}">{{menu_item.label}}</a><br/>
      {% endfor %}

#. In all views where you want to reuse the component you can paste the following snippet:

   .. code-block:: html

      {% component template="sample_menu.html", url="/dynamic-menu/menu/1" %}{% endcomponent %}

#. Make sure you run **dynamic_menu/sql/module_setup.sql** against your configured database.

#. This script will create **menus** and **menu_items** tables into your database. Below you can find a sample script for creating a menu:

   .. code-block:: sql

      INSERT INTO menus(name) VALUES('My First Menu');
      INSERT INTO menu_items(target, url, title, label)
      VALUES ('_blank', '/homepage', 'Simple and friendly description', 'Home'),
             ('_blank', '/page2', 'Simple and friendly description', 'Page 2'),
             ('_blank', '/page3', 'Simple and friendly description', 'Page 3');

Current limitations
-------------------

Because **Fantastico** framework is developed using an Agile mindset, only the minimum valuable scope was delivered for
**Dynamic Menu** component. This mean is not currently possible to:

   * Localize your menu items.
   * Display the menu items in the request language dynamically.
   * Only first 100 menu items can be currently retrieved.

Technical summary
-----------------

.. autoclass:: fantastico.contrib.dynamic_menu.menu_controller.DynamicMenuController
   :members:

.. autoclass:: fantastico.contrib.dynamic_menu.menu_exceptions.FantasticoMenuNotFoundException
   :members:
