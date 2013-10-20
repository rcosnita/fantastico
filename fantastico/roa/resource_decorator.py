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

            def __init__(self, name, value):
               self.name = name
               self.value = value
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

    def __init__(self, name, url, version=1.0, subresources=None, validator=None):
        self._name = name
        self._url = url
        self._version = float(version)
        self._model = None
        self._subresources = subresources or {}
        self._validator = validator

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
