Dynamic pages
=============

Most of the time, when a developer create a new web site or web application he follows the steps:

   #. Create a set of templates (can be delegated to a web designer)
   #. Create a new API or create a proxy API.
   #. Create pages over the templates.

Many web sites / applications have a minimal set of master templates and all web pages follow those templates. This kind of
approach keeps site consistency and decouple layouts from actual content. In **Fantastico**, it is extremely easy to work in this
manner thanks to **Dynamic pages** extension.

Dynamic pages divides pages into two main parts:

   #. Page meta information (title, keywords, description, language)
   #. Page model / content (markup, text keys or any other kind of information).

Using dynamic pages you can easily add new web pages to your project without writing a single line of server side code.

Integration
-----------

#. Activate **Dynamic pages** extension.

   .. code-block:: bash

      fsdk activate-extension --name dynamic_pages --comp-root <comp_root>

#. Add new dynamic pages to your project using **<comp_root>/sql/create_data.sql**.

   .. code-block:: sql

      INSERT INTO pages(id, name, url, template, keywords, description, title, language)
      VALUES(1, '/en/home', '/en/home', '/frontend/views/master.html', 'keyword 1, ...', 'Home page', 'description', 'en-US');

      INSERT INTO page_models(page_id, name, value)
      VALUES(1, 'article_left', '<p class="hello_world">Hello world.</p>');

      INSERT INTO page_models(page_id, name, value)
      VALUES(1, 'article_right', '<p class="hello_world_right">Hello world right.</p>');

#. Update your project database

   .. code-block:: bash

      fsdk syncdb --db-command /usr/bin/mysql --comp-root <comp_root>

#. Create **master.html** template file under **<comp_root>/frontend/views/**.

   .. code-block:: html

      <!DOCTYPE html>

      <html lang="{{page.language}}">
         <head>
            <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="keywords" content="{{page.keywords}}" />
            <meta name="description" content="{{page.description}}" />

            <title>{{page.title}}</title>
         </head>

         <body>
            <h1>{{page.article_left.value}}</h1>

            <h2>{{page.article_right.value}}</h2>
         </body>
       </html>

After you integrated **dynamic pages** extension into your project you can access
http://localhost:12000/dynamic/test/default/page from a browser. You should see a very simple dynamic page rendered.

Current limitations
-------------------

In the first version of this component (part of **Fantastico 0.4**) there are some known limitations:

   * Create / Delete / Update / Bulk listing API are not provided. You can do this through create_data.sql script.
   * There is no way to rewrite dynamic pages url so that they do not contain */dynamic* prefix.

Technical summary
-----------------

.. autoclass:: fantastico.contrib.dynamic_pages.pages_router.PagesRouter
   :members:

.. autoclass:: fantastico.contrib.dynamic_pages.models.pages.DynamicPage
   :members:

.. autoclass:: fantastico.contrib.dynamic_pages.models.pages.DynamicPageModel
   :members: