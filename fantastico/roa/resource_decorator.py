'''
Copyright 2013 Cosnita Radu Viorel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. codeauthor:: Radu Viorel Cosnita <radu.cosnita@gmail.com>
.. py:module:: fantastico.roa.resource_decorator
'''

class Resource(object):
    '''
    .. image:: /images/roa/roa_classes.png

    This class provides the main way for defining resources. Below you can find a very simple example for defining new resources:

    .. code-block:: python

        @Resource(name="app-setting", url="/app-settings")
        class AppSetting(BASEMODEL):
            id = Column("id", Integer, primary_key=True, autoincrement=True)
            name = Column("name", String(50), unique=True, nullable=False)
            value = Column("value", Text, nullable=False)

            def __init__(self, name=None, value=None):
               self.name = name
               self.value = value

    Starting from **Fantastico** version 0.6 ROA resources support OAuth2 authorization. Because of this, resources can now be
    user dependent or user independent. In order for authorization to work as expected for resources which are available only
    to certain users you can use the following code snippet:

    .. code-block:: python

        @Resource(name="app-setting", url="/app-settings", user_dependent=True)
        class AppSetting(BASEMODEL):
            id = Column("id", Integer, primary_key=True, autoincrement=True)
            name = Column("name", String(50), unique=True, nullable=False)
            value = Column("value", Text, nullable=False)
            user_id = Column("user_id", Integer, nullable=False)

            def __init__(self, name=None, value=None, user_id=None):
               self.name = name
               self.value = value
               self.user_id = user_id

    If you do not define a user_id property for user dependent resources a runtime exception is raised. In order to find out more
    about OAuth2 authorization implemented into fantastico please read: :doc:`/features/oauth2`.
    '''

    @property
    def name(self):
        '''This read only property holds the name of the resource.'''

        return self._name

    @property
    def url(self):
        '''This read only property holds the url of the resource.'''

        return self._url

    @property
    def version(self):
        '''This read only property holds the version of the resource.'''

        return self._version

    @property
    def model(self):
        '''This read only property holds the model of the resource.'''

        return self._model

    @property
    def user_dependent(self):
        '''This read only property returns True if user is owned only by one resource and False otherwise. It is really important
        to understand the impact of the property when set to True:

        #. Every GET on resource root url will also receive a filter user_id from access_token == resource.model.user_id
        #. Every GET on a specific resource id will be validated also on user_id field.
        #. Every POST for creating a new resource will automatically assign resource to user_id found in access_token. There is an
            exception when the resource does not require create scopes.
        #. Every PUT on a specific resource id will also check to ensure the user from the access_token owns the resource.
        #. Every DELETE on a specific resource id will also check to ensure the user from the access_token owns the resource.'''

        return self._user_dependent

    @property
    def subresources(self):
        '''This read only property holds the subresources of this resource. A resource can identify a subresource by one
        or multiple (composite uniquely identified resources) resource attributes.

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
        '''

        return self._subresources

    @property
    def validator(self):
        '''This property returns the validator type which must be used for this resource for creating / updating it. You can
        read more about it on :py:class:`fantastico.roa.resource_validator.ResourceValidator`.'''

        return self._validator

    def __init__(self, name, url, version=1.0, subresources=None, validator=None, user_dependent=False):
        self._name = name
        self._url = url
        self._version = float(version)
        self._model = None
        self._subresources = subresources or {}
        self._validator = validator
        self._user_dependent = user_dependent

    def __call__(self, model_cls, resources_registry=None):
        '''This method is invoked when the model class is first imported into python virtual machine.'''

        from fantastico.roa.resources_registry import ResourcesRegistry

        resources_registry = resources_registry or ResourcesRegistry()

        self._model = model_cls

        resources_registry.register_resource(self)

        return model_cls

    def __lt__(self, resource):
        '''This method puts order between resources by  name and version comparisons.'''

        if self.name == resource.name and self.version == resource.version:
            return False

        if self.name == resource.name:
            if self.version == "latest":
                return True

            return self.version < resource.version

        return self.name < resource.name
