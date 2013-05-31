Component model
===============

In Fantastico there is no enforced component model for your code but there are a set of recommendations 
that will make your life a lot easier when organizing projects. A typical **component** structure looks like:

- <your project folder>
   - component_1
      - models (sql alchemy models)
      - static (static files holder)
      - views (all views used by this component controllers')
      - sql (sql scripts required to setup the component)
      - __init__.py
      - *.py (controller module files)

You can usually structure your code as you want, but Fantastico default :doc:`/features/mvc` registrators are assuming
component name is the parent folder of the controller module. This is why is best to follow the above mentioned structure.
None of the above folders are mandatory which gives you, developer, plenty of flexibility but also responsibility. For 
more information about **models**, **views** and **controllers** read :doc:`/how_to/mvc_how_to` section.

Static folder
-------------

By default, static folder holds all static assets belonging to a component. You can find more information about this
in :doc:`/how_to/static_assets` section.

Sql folder
----------

Sql folder is used to hold all sql scripts required for a component to work correctly. In our continuous delivery
process we scan all available sql folders and execute **module_setup.sql** scripts. By default, we want to give
developers the chance to provide a setup script for each component in order to easily install the component database
dependencies.

Sql folder example
~~~~~~~~~~~~~~~~~~

Assume you want to create a blog module that requires a storage for **Authors** and **Posts**. module_setup.sql script
is the perfect place to provide the code. We recommend to make this code idempotent, meaning that once dependencies are
created they should not be altered anymore by this script.

An example of such a script we use in integration tests can be found under: **/<fantastico_framework>/samples/mvc/sql/module_setup.sql**.

.. code-block:: sql

   ###############################################################################################
   # Copyright 2013 Cosnita Radu Viorel
   #
   # Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
   # and associated documentation files (the "Software"), to deal in the Software without  
   # restriction, including without limitation the rights to use, copy, modify, merge, publish,  
   # distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom 
   # the Software is furnished to do so, subject to the following conditions:
   #
   # The above copyright notice and this permission notice shall be included in all copies or 
   # substantial portions of the Software.
   #
   # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,  
   # INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR  
   # PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR  
   # ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,  
   # ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
   # IN THE SOFTWARE.
   ###############################################################################################


   DROP TABLE IF EXISTS mvc_friendly_messages;
   CREATE TABLE mvc_friendly_messages(
      Id INT AUTO_INCREMENT,
      Message TEXT,
      PRIMARY KEY(id));