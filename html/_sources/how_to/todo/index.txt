Creating a simple TODO application
==================================

In this how to article you can find information of how you can create a TODO web application using Fantastico framework. This
tutorial works with Fantastico versions greater or equal than `0.5.0 <http://pypi.python.org/pypi/fantastico/0.5.0>`_.

Functional requirements
-----------------------

The application we are going to develop must meet the following requirements:

   * User must be able to create tasks.
   * User must be able to see all tasks.
   * User must be able to quickly filter tasks.
   * User must be able to complete tasks.
   * User must be able to use an web application for managing tasks.

Overview
--------

.. figure:: /images/how_to/todo/main_page.png
   :scale: 100 %
   :align: center
   :alt: TODO web application implemented using Fantastico framework.

   TODO web application powered by Fantastico.

The frontend is powered by the following API endpoints:

+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| **Endpoint**    | **HTTP verb** | **HTTP Body**                                                            | **Description**                                  |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks          | GET           | None                                                                     | Retrieves available tasks in a paginated manner. |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks          | POST          | {"name": "Task name", "description": "Task description"}                 | Creates a new task described by the given body.  |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks/:task_id | GET           | None                                                                     | Retrieves a specific task from tasks collection. |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks/:task_id | PUT           | {"name": "Task name changed", "description": "Task description changed"} | Updates a specific task from tasks collection.   |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks/:task_id | DELETE        | None                                                                     | Deletes a specific task from tasks collection.   |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+

How to sources
--------------

All tutorial source files are available on github: `<https://github.com/rcosnita/fantastico-todo>`_. Each step of the tutorial
has a corresponding branch in the github repository so you can easily skip steps of this tutuorial. Though you can skip steps
we recommend you take 30 minutes and finish this step by step how to in order to fully understand the power of Fantastico
framework and how easy it is to build modern web applications using it.

Requirements
------------

This tutorial requires developer to have:

   #. A Debian based operating system
   #. Access to a mysql database.
   #. Python 3.2 or newer.

Next steps
----------

.. toctree::
   :maxdepth: 2
   
   setup
   step_1_settings
   step_2_create_api
   step_3_create_frontend
   step_4_activate_googleanalytics
   step_5_final_notes