Step 5 - TODO final notes
=========================

During the last 30 minutes you have created a **TODO** web application using **Fantastico** framework. You have already noticed
how easily it is to create resources and REST apis in a declarative manner without actually writing any line of code for
pagination, filtering and sorting.

Moreover, you have seen how you can keep clean markup in your projects by using **Fantastico** components. In the end you added
Google Analytics for tracking the performance of your **TODO** web application.

What's next?
------------

It is recommended to first take the challenges below before implementing your real life **Fantastico** project:

   #. Send a uniquely generated cookie for uniquely identify the user session.
   #. Make tasks belong to a unique user (identified by the cookie from previous step).
   #. Add a category resource and try to make tasks belong to one or more categories. Be aware, that GET collection and GET item
      from collection ROA APIs works perfectly with relationships.
   #. Separate ROA APIs domain from application domain. (e.g `http://api.todo.com`_).
   #. You are ready to rock.

Resources
---------

It is recommended to read Fantastico documentation in order to get full details about each concept which was presented in this
tutorial. You can see the application from this tutorial together with user session improvements
and separation of api from application domain deployed on: `<http://todo.fantastico.scrum-expert.ro/frontend/ui/index>`_.