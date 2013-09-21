ROA (Resource Oriented Architecture)
====================================

Resource Oriented Architecture (REST) is incredible popular nowadays for the following reasons:

   * Increased scalability of applications.
   * Easy integration of systems.
   * Intuitive modelling of business problems.
   * Stateful imperative programming pains removed.

You can find many information about advantages of REST and why it is recommended to use such an architecure. For further reading
you can visit http://en.wikipedia.org/wiki/Representational_state_transfer.

In Fantastisco framework we firmly encourage REST approach into projects. We even go a step further in this direction, by
standardising REST APIs and providing REST APIs generator over implemented models.

Simple use cases
----------------

Application settings stored in database
---------------------------------------

Imagine you have a model called **AppSetting** meant to define custom settings attributes which influence your application.

.. code-block:: python

   class AppSetting(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      name = Column("name", String(50), unique=True, nullable=False)
      value = Column("value", Text, nullable=False)
      
      def __init__(self, name, value):
         self.name = name
         self.value = value

In a standard **MVC** (:doc:`/features/mvc`) web application once you have defined the above mentioned fantastico model you would
have to do the following: (for providing minimal CRUD)

   #. Create a :py:class:`fantastico.mvc.controller_decorators.Controller`
   #. Implement listing of custom settings

      #. Support pagination.
      #. Support filtering.
      #. Support ordering.

   #. Implement individual custom setting retrieval (by id).
   #. Implement Create custom setting.
   #. Implement Update custom setting.
   #. Implement Delete custom setting.
   #. For each operation implemented provide validation logic.
   #. For each operation implemented provide error handling logic.

This is an extremely repetitive task and involves quite a lot of boiler plate. In addition no standard is imposed for how
pagination, sorting and filtering work.

A more convenient way for this problem is to provide some additional information about the model:

.. code-block:: python

   @Resource(name="app-setting", url="/app-settings")
   class AppSetting(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      name = Column("name", String(50), unique=True, nullable=False)
      value = Column("value", Text, nullable=False)
      
      def __init__(self, name, value):
         self.name = name
         self.value = value

Once the model is decorated, I expect to have a fully functional API which I can easily invoke through HTTP calls:

   * GET    - /api/latest/app-settings - list all application settings (supports filtering, ordering and pagination)
   * POST   - /api/latest/app-settings - create a new app setting.
   * PUT    - /api/latest/app-settings/:id - update an existing application setting.
   * DELETE - /api/latest/app-settings/:id - delete an existing application setting.

Versioning
----------

It is always a good practice to support API versioning. Going a step further with AppSetting resource:

.. code-block:: python

   @Resource(name="app-setting", url="/app-settings", version=1.0)
   class AppSetting(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      name = Column("name", String(50), unique=True, nullable=False)
      value = Column("value", Text, nullable=False)
      
      def __init__(self, name, value):
         self.name = name
         self.value = value
   
   @Resource(name="app-setting", url="/app-settings", version=2.0)
   class AppSettingV2(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      name = Column("name", String(80), unique=True, nullable=False)
      value = Column("value", Text, nullable=False)
      
      def __init__(self, name, value):
         self.name = name
         self.value = value

The above example will actually provide the following endpoints which can be easily accessible:

   * /api/1.0/app-settings
   * /api/2.0/app-settings
   * /api/latest/app-settings (which at this moment points to the most recent version of the api)

If we want to retrieve all application settings using version 1.0 we open a browser and point it to **/api/1.0/app-settings**. For
avoiding multiple APIs chaos we strongly encourage to use the latest available API.

Advantages
----------

   * Extremely fast development of uniform APIs which behave predictable.
   * Extremely easy to enforce exception handling logic.
   * Extremely easy to enforce security for APIs.
   * Extremely easy to keep APIs in sync with resource changes.
   * DRY (don't repeat yourself).

Fantastico ROA APIs standard
----------------------------

Please read :doc:`/features/roa/rest_standard` for understanding how the generated API will behave and which are the routes
provided out of the box.