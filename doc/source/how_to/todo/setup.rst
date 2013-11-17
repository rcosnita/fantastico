Step 0 - TODO setup
===================

Follow the steps below in order to setup todo web application project correctly:

   #. git clone https://github.com/rcosnita/fantastico-todo.git fantastico-todo
   #. cd fantastico-todo
   #. virtualenv-3.2 --distribute pip-deps
   #. . pip-deps/bin/activate
   #. pip install fantastico
   #. fantastico_setup_project.sh python3.2 todo
      * (this will take a couple of minutes because it installs all dependencies).

At this moment you have a **Fantastico** project created and a component module holder named todo initialized.
For more information about advanced project setup you can always read :doc:`/how_to/new_project_how_to`.