Creating a new project
======================

A new Fantastico based project can be easily setup by following this how to. In this how to we are going to create
a project named **fantastico_first**.

#. cd ~/
#. mkdir fantastico_first
#. cd fantastico_first
#. virtualenv-3.2 --distribute pip-deps
#. . pip-deps/bin/activate
#. pip install fantastico
#. fantastico_setup_project.sh python3.2 my_project

The last step might take a while because it will also install all fantastico dependencies (e.g sphinx, sqlalchemy, ...).
Please make sure your replace python3.2 with the correct python version.
In order to test the current project do the following:

#. run_dev_server
#. Access `http://localhost:12000/fantastico/samples/mvc/static/sample.jpg`_
#. Access `http://localhost:12000/mvc/hello-world`_

Your newly project is setup correctly and it runs fantastico default samples project.

Create first component
----------------------

After the new project it's correctly setup we can start to create our first component.

#. cd my_project
#. mkdir component1
#. cd component1
#. mkdir static
#. Paste an image into static folder (e.g first_photo.jpg)
#. touch __init__.py
#. touch hello_world.py
#. Paste the code listed below into hello_world.py

.. code-block:: python