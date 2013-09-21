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

+---------------+----------------------------------------------------------+-------------------------------------------------------------+
| **HTTP Verb** | **URL**                                                  | **Description**                                             |
+---------------+----------------------------------------------------------+-------------------------------------------------------------+
| GET           | /api/2.0/app-settings?offset=0&limit=100                 | Get the first 100 settings.                                 |
+---------------+----------------------------------------------------------+-------------------------------------------------------------+
| GET           | /api/2.0/app-settings?order=[{name: desc}, {value: asc}] | Order settings by name (descending) and values (ascending). |
+---------------+----------------------------------------------------------+-------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=<complex filter>            | See :ref:`roa-filtering`.                                   |
+---------------+----------------------------------------------------------+-------------------------------------------------------------+
| POST          | /api/2.0/app-settings                                    | Create a new custom setting                                 |
+---------------+----------------------------------------------------------+-------------------------------------------------------------+

Pagination
~~~~~~~~~~

When requesting a given resource collection a subset of this collection will be retrived.

   * **offset** - defines which is the start record of the API. (Default value is 0)
   * **limit** - defines the maximum number of items I want to retrieve. (Default value is 10)

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

.. _roa-filtering:

Filtering
~~~~~~~~~

In fantastico, APIs filtering is done by following a very simple Resource Query Language (RQL):

+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| **HTTP Verb** | **URL**                                                               | **Description**                                                          |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=eq(name, "vat")                          | Get all settings named **vat**.                                          |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=like(name, "%vat%")                      | Get all settings which name contains **vat**.                            |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=gt(value, 0.19)                          | Get all settings which have value greater than **0.19**.                 |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=ge(value, 0.19)                          | Get all settings which have value greater / equals than / with **0.19**. |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=lt(value, 0.19)                          | Get all settings which have value less than **0.19**.                    |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=le(value, 0.19)                          | Get all settings which have value less / equals than / with **0.19**.    |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=in(name, ["vat", "default_locale"])      | Get all settings which name is **vat** or **default_locale**.            |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?filter=and(eq(name, "vat"), eq(value, "en_US")) | Get all settings which name is **vat** and value is **en_US**.           |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+
| GET           | /api/2.0/app-settings?&filter=or(eq(name, "vat"), eq(value, "en_US")) | Get all settings which name is **vat** or value is **en_US**.            |
+---------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------+

You can see in the above example that the query language supported by Fantastico APIs facilitate very complex filtering on resources. It is always
recommended to send pagination parameters in order to limit the number of resources retrieved from each API.