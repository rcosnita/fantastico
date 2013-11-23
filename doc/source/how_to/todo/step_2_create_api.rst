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
| /tasks/:task_id | GET           |                                                                          | Retrieves a specific task from tasks collection. |
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

         CREATE TABLE IF NOT EXISTS tasks(
            task_id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            status SMALLINT,
            PRIMARY KEY(task_id)
         );

   #. Execute the following command in order to create the table into **tododb** database:

      .. code-block:: bash

         fsdk syncdb --db-command /usr/bin/mysql --comp-root todo

   #. Create some sample uncompleted tasks in your database:

      #. Paste the code below in fantastico-todo/todo/frontend/sql/create_data.sql:

         .. code-block:: sql

            INSERT INTO tasks(name, description, status)
            SELECT * FROM (SELECT 'Go buy some dog food.', 'It is extremely important to have this by noon.', 0) as tmp
            WHERE NOT EXISTS(SELECT name FROM tasks WHERE name = 'Go buy some dog food.');

            INSERT INTO tasks(name, description, status)
            SELECT * FROM (SELECT 'Write some clean code.', 'You decide when to start this.', 0) as tmp
            WHERE NOT EXISTS(SELECT name FROM tasks WHERE name = 'Write some clean code.');

      #. Execute the following command in order to insert above mentioned tasks into **tododb** database:

         .. code-block:: bash

            fsdk syncdb --db-command /usr/bin/mysql --comp-root todo

Create APIs
-----------

Now that the storage is ensured and our project is configured correctly we have to create the APIs. In order to do this
follow the steps below:

   #. fsdk activate-extension --name roa_discovery --comp-root todo
   #. Paste the code below in fantastico-todo/todo/frontend/models/tasks.py

      .. code-block:: python

         from fantastico.mvc import BASEMODEL
         from fantastico.roa.resource_decorator import Resource
         from sqlalchemy.schema import Column
         from sqlalchemy.types import Integer, String, Text, SmallInteger
         from todo.frontend.validators.task_validator import TaskValidator

         @Resource(name="Task", url="/tasks", validator=TaskValidator)
         class Task(BASEMODEL):
             '''This class provides the task model required for todo application.'''

             __tablename__ = "tasks"

             id = Column("task_id", Integer, primary_key=True, autoincrement=True)
             name = Column("name", String(200), nullable=False)
             description = Column("description", Text)
             status = Column("status", SmallInteger, nullable=False)

             def __init__(self, name=None, description=None, status=0):
                 self.name = name
                 self.description = description
                 self.status = status

   #. Paste the code below in fantastico-todo/todo/frontend/validators/task_validator.py

      .. code-block:: python

         from fantastico.roa.resource_validator import ResourceValidator
         from fantastico.roa.roa_exceptions import FantasticoRoaError

         class TaskValidator(ResourceValidator):
             '''This is the task validator invoked automatically in create / update operations.'''

             def validate(self, resource):
                 '''This method is invoked automatically in order to validate resource body.'''

                 errors = []

                 if resource.name is None or len(resource.name) == 0:
                     errors.append("Name attribute is mandatory.")

                 if resource.status is None:
                     errors.append("Status attribute is mandatory.")

                 if len(errors) == 0:
                     return

                 raise FantasticoRoaError("\n".join(errors))

   #. Run the following command in an activate fantastico-todo virtual environment:

      .. code-block:: bash

         fantastico_run_dev_server

   #. Visit `<http://localhost:12000/roa/resources>`_. You should see a response similar to the one below:

      .. image:: /images/how_to/todo/roa_discovered_resources.png

   #. Visit `<http://localhost:12000/api/latest/tasks>`_. You should see a response similar to the one below:

      .. image:: /images/how_to/todo/roa_tasks_initial_listing.png

   #. Visit `<http://localhost:12000/api/latest/tasks/1>`_. You should receive the details for the task with unique identifier 1.
   #. Additionally Create / Update / Delete operations are already working.