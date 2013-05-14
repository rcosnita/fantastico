Development mode
================

**Fantastico** framework is a web framework designed to be developers friendly. In order to simplify setup sequence, fantastico
provides a standalone WSGI compatible server that can be started from command line. This server is fully compliant with WSGI
standard. Below you can find some easy steps to achieve this:

#. Goto fantastico framework or project location
#. sh run_dev_server.sh

This is it. Now you have a running fantastico server on which you can test your work.

By default, **Fantastico** dev server starts on port 12000, but you can customize it from 
:py:class:`fantastico.settings.BasicSettings`.

Hot deploy
----------

Currently, this is not implemented, but it is on todo list on short term.

API
---

For more information about Fantastico development server see the API below.

.. autoclass:: fantastico.server.dev_server.DevServer
    :members:
    
Database config
---------------

Usually you will use **Fantastico** framework together with a database. When we develop new core features of **Fantastico**
we use a sample database for integration. You can easily use it as well to play around:

#. Goto fantastico framework location
#. export MYSQL_PASSWD=***** (your mysql password)
#. export MYSQL_HOST=localhost (your mysql localhost)
#. sh run_setup_db.sh

**run_setup_db.sh** create an initial fantastico database and a user called fantastico identified by **12345** password. After
database is successfully created, it scans for all available **module_setup.sql** files and execute them against newly created
database.    