Step 1 - TODO settings
======================

In this section of the tutorial you can find information about how to correctly configure database parameters. Follow the steps
below in order to have correct settings for TODO web applications:

   #. git checkout -b step-1-settings
   #. Paste the code below under fantastico-todo/pip-deps/bin/activate at the end of the file.

      .. code-block:: bash

         # fantastico-todo/pip-deps/bin/activate

         export FANTASTICO_ACTIVE_CONFIG=todo.settings.BaseProfile
         export PYTHONPATH=.

   #. Paste the code below under fantastico-todo/todo/settings.py

      .. code-block:: python

         # fantastico-todo/todo/settings.py

         from fantastico.settings import BasicSettings

         class BaseProfile(BasicSettings):
             '''todo web application base profile.'''

             @property
             def database_config(self):
                 '''This property is automatically invoked by fantastico in order to connect to database.'''

                 db_config = super(BaseProfile, self).database_config

                 db_config["database"] = "tododb"
                 db_config["username"] = "todo_user"
                 db_config["password"] = "12345"

                 return db_config

   #. Run the command below in order to make sure sdk is working:

      .. code-block:: bash

         fsdk --help

      You should see a screen similar to the one below:

      .. image:: /images/how_to/todo/fsdk_help.png
         :scale: 100 %

   #. Execute the code below in order to create **tododb** database.

      .. code-block:: bash

         /usr/bin/mysql --host=localhost --user=root --password=**** --verbose -e "source sql/setup_database.sql"

Explanation
-----------

We have just configured our virtual development environment for **TODO** web application to use **tododb** with
**todo_user/12345** credentials. You can of course configure more details of your connection:

   * MySql host.
   * MySql port.
   * MySql charset.

For a complete list of database configuration in **Fantastico framework** please read :doc:`/get_started/settings`.

In addition, we created a dedicated database for **TODO** web application.