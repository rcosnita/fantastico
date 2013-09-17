REST API standard
=================

In this document you can find the standard behavior imposed for Resource generated apis (:doc:`/features/roa`). For better
understanding how APIs will behave let's assume we have the following resource defined:

.. code-block:: python

   @Resource(name="app-setting", url="/app-settings", version=2.0)
   class AppSettingV2(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      name = Column("name", String(80), unique=True, nullable=False)
      value = Column("value", Text, nullable=False)
      
      def __init__(self, name, value):
         self.name = name
         self.value = value


Resource collection
-------------------

Each resource will have an API entry point which lists all available resources of same type (e.g **AppSettingV2**).
This entry point supports the following additional operations:

   * Pagination of resources.
   * Sorting of resources.
   * Filtering of resources.

The main entry point for **AppSettingV2** collection of resources is **/api/app-settings/2.0**.

+---------------+----------------------------------------------------------+----------------------------------------------------------------------+
| **HTTP Verb** | **URL**                                                  | **Description**                                                      |
+---------------+----------------------------------------------------------+----------------------------------------------------------------------+
| GET           | /api/app-settings/2.0?offset=0&limit=100                 | Get the first 100 settings.                                          |
+---------------+----------------------------------------------------------+----------------------------------------------------------------------+
| GET           | /api/app-settings/2.0?order=[{name: desc}, {value: asc}] | Order settings by name (descending) and values (ascending).          |
+---------------+----------------------------------------------------------+----------------------------------------------------------------------+
| GET           | /api/app-settings/2.0?filter=<complex filter>            | Read filtering section for understanding how you can define filters. |
+---------------+----------------------------------------------------------+----------------------------------------------------------------------+
| POST          | /api/app-settings/2.0                                    | Create a new custom setting                                          |
+---------------+----------------------------------------------------------+----------------------------------------------------------------------+

Pagination
~~~~~~~~~~

When requesting a given resource collection a subset of this collection will be retrived.

   * **offset** - defines which is the start record of the API.
   * **limit** - defines the maximum number of items I want to retrieve.

A possible result for **AppSettingV2** collection retrieval looks like:

.. code-block:: javascript

   {
      "items":
         [{"id": 1, "name": "default_locale", "value": "en_US"},
          {"id": 2, "name": "vat", "value": 0.19}],
      "totalItems": 1000
   }

Sorting
~~~~~~~

When requesting a given resource collection sorted you can specify the sorting criteria:

   * **order** - a JSON list containing dictionary where each dictionary key is the field used for sorting and each dictionary value is sorting direction.
   * If you don't specify the order items will be retrieved in the order in which they are stored (consider this random order).
   * Order list is evaluated from left to right with left most element having the highest priority.

A possible result for **AppSettingV2** collection retrieval looks like:

.. code-block:: javascript

   {
      "items":
         [{"id": 2, "name": "vat", "value": 0.19},
          {"id": 1, "name": "default_locale", "value": "en_US"}],
      "totalItems": 1000
   }

Filtering
~~~~~~~~~
