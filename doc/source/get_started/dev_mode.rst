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