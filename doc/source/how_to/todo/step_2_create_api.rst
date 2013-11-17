Step 2 - TODO API endpoints
===========================

In this section of **TODO** how to we are going to create the following API endpoints:

+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| **Endpoint**    | **HTTP verb** | **HTTP Body**                                                            | **Description**                                  |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks          | GET           | None                                                                     | Retrieves available tasks in a paginated manner. |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks          | POST          | {"name": "Task name", "description": "Task description"}                 | Creates a new task described by the given body.  |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks/:task_id | GET           | {"task_id": 1, "name": "Task name", "description": "Task description"}   | Retrieves a specific task from tasks collection. |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks/:task_id | PUT           | {"name": "Task name changed", "description": "Task description changed"} | Updates a specific task from tasks collection.   |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+
| /tasks/:task_id | DELETE        | None                                                                     | Deletes a specific task from tasks collection.   |
+-----------------+---------------+--------------------------------------------------------------------------+--------------------------------------------------+

These are going to provide support for various clients which want to provide TODO functionality:

   * Javascript frontend client.
   * Mobile app client.

Create database
---------------

Our TODO tasks are going to be persisted by the endpoints into a MySql database (already created in previous steps). Now,
we are going to create tasks tables:

   #. git checkout -b step-2-create-api
   #. Paste the code below under fantastico-todo/todo/frontend/sql/module_setup.sql

      .. code-block:: sql

         CREATE TABLE tasks(
            task_id INT NOT NULL,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            status SMALLINT,
            PRIMARY KEY(task_id)
         );

   #. Execute the following command:

      .. code-block:: bash

         fsdk syncdb --db-command /usr/bin/mysql --comp-root todo
