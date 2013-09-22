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

Examples
--------

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

Validation
----------

Each resource requires validation for create / update operations. Validation is harder to be achieved through code introspection
so in Fantastico for each defined resource you can define a validator which will be invoked automatically.

.. code-block:: python

   class AppSettingValidator(ResourceValidator):
      def validate(self, resource):
         errors = []
         
         if resource.name == "unsupported":
            errors.append("Invalid setting name: %s" % resource.name)
         
         if len(resource.value) == 0:
            errors.append("Setting %s value can not be empty. %s" % resource.name)
         
         if len(errors) == 0:
            return
         
         raise FantasticoResourceError(errors)

.. code-block:: python

   @Resource(name="app-setting", url="/app-settings", version=2.0, validator=AppSettingValidator)
   class AppSettingV2(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      name = Column("name", String(80), unique=True, nullable=False)
      value = Column("value", Text, nullable=False)
      
      def __init__(self, name, value):
         self.name = name
         self.value = value

If no validator is provided no validation is done on the given resource. Also, it is important to always remember that validators
are only invoked for **Create** and **Update**:

   * POST   - /api/latest/app-settings - create a new app setting. (validate method will be invoked).
   * PUT    - /api/latest/app-settings/:id - update an existing app setting. (validate method will be invoked).

We are aware that there are some common validation cases which can be reused:

   #. Email validation
   #. Phone number validation
   #. Credit Card number validation

All common validation cases  are provided out of the box as methods part of ResourceValidator class. You can easily use them into
your resource validator.

Partial object representation
-----------------------------

There are cases when a resource contains many fields but you actually need only a few of them:

.. code-block:: python

   @Resource(name="address", url="/addresses", version=1.0)
   class Address(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      line1 = Column("line1", String(200), nullable=False)
      line2 = Column("line2", String(200))
      line3 = Column("line3", String(200))
      line4 = Column("line4", String(200))
      line5 = Column("line5", String(200))
      line6 = Column("line6", String(200))
      city = Column("city", String(80))
      country = Column("country", String(80))
      zip_code = Column("zip_code", String(10))
      
      def __init__(self, line1=None, line2=None, line3=None, line4=None, line5=None, line6=None,
                  city=None, country=None, zip_code=None):
         self.line1 = line1
         self.line2 = line2
         self.line3 = line3
         self.line4 = line4
         self.line5 = line5
         self.line6 = line6
         self.city = city
         self.country = country
         self.zip_code = zip_code

When working with the Address resource there will be cases when we do not need all fields to be transferred to client. For this,
partial representation is supported out of the box into Fantastico:

.. code-block:: javascript

   // retrieve only city,zip_code and line1 of a given address
   var url = "/api/1.0/addresses/1?fields=city,zip_code,line1";

A possible response for this request might be:

.. code-block:: javascript

   {
       city: "Bucharest", 
       zip_code: "B00001", 
       line1: "First line of this wonderful address"
   }

**fields** Query parameter is optional. If you omit this query parameter all fields are retrieved in the response. **fields**
query parameter makes sense for:

   #. Listing a collection
   #. Retrieving information about an individual item.

All other operations simply ignore **fields**.

Resource composed attributes
----------------------------

There are resources which have attributes which points to another resource:

.. code-block:: python

   @Resource(name="person", url="/persons", version=1.0,
             subresources={"bill_address": ["bill_address_id"],
                           "mail_address": ["mail_address_id"],
                           "ship_address:" ["ship_address_id"])
   class Person(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      first_name = Column("first_name", String(80))
      last_name = Column("last_name", String(50))
      bill_address_id = Column("bill_address_id", ForeignKey("addresses.id"))
      bill_address = relationship(Address, primaryjoin=bill_address_id == Address.id)
      ship_address_id = Column("ship_address_id", ForeignKey("addresses.id"))
      ship_address = relationship(Address, primaryjoin=ship_address_id == Address.id)
      mail_address_id = Column("ship_address_id", ForeignKey("addresses.id"))
      ship_address = relationship(Address, primaryjoin=mail_address_id == Address.id)

The above definition shows you how to mark the subresources of **person** resource. By default they will not be retrieved in
requests. Only subresource identifier keys pointing from **person** to various **address** objects are retrieved. If you want
to obtain details about a specific address (e.g bill_address) you can use example below:

.. code-block:: python

   var url = "/api/1.0/persons/1?fields=first_name, last_name, bill_address(line1, city, zip_code)"

The above example url might return:

.. code-block:: javascript

   {
      "first_name": "John",
      "last_name": "Doe",
      "bill_address": {
         "line1": "First line of this wonderful address",
         "city": "Bucharest",
         "zip_code": "B00001"
      }
   }

Composed attributes usage is limited to below mentioned operations:

   * Listing collections.
   * Retrieving information about an individual item.

We do not support update / create of multiple resources in one single request.

Advantages
----------

   * Extremely fast development of uniform APIs which behave predictable.
   * Extremely easy to enforce exception handling logic.
   * Extremely easy to enforce security for APIs.
   * Extremely easy to keep APIs in sync with resource changes.
   * DRY (don't repeat yourself).

.. toctree::
   :maxdepth: 2
   
   roa/rest_standard
   roa/rest_exception_handling
