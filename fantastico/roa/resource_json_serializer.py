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
.. py:module:: fantastico.roa.resource_json_serializer
'''
from fantastico.roa.roa_exceptions import FantasticoRoaError

class ResourceJsonSerializer(object):
    '''This class provides the methods for serializing a given resource into a dictionary and deserializing a dictionary into
    a resource.

    .. code-block:: python

        # serialize / deserialize a resource without subresources
        json_serializer = ResourceJsonSerializer(AppSetting)
        resource_json = json_serializer.serialize(AppSetting("simple-setting", "0.19"))
        resource = json_serializer.deserialize(resource)
    '''

    def __init__(self, resource_ref):
        self._resource_ref = resource_ref
        self._supported_attrs = self._identify_public_attrs(self._resource_ref.model)

    def _identify_public_attrs(self, model_cls):
        '''This method returns a dictionary containing all public atttributes of a given model class.'''

        public_attrs = {}

        for attr_name in model_cls.__dict__.keys():
            if attr_name.startswith("_") or attr_name.startswith("__"):
                continue

            public_attrs[attr_name] = True

        return public_attrs

    def deserialize(self, body):
        '''This method converts the given body into a concrete model (if possible).

        :param body: A JSON object we want to convert to the model compatible with this serializer.
        :type body: dict
        :returns: A model instance initiated with attributes from the given dictionary.
        '''

        model_cls = self._resource_ref.model

        model = model_cls()

        for attr_name, attr_value in body.items():
            if not self._supported_attrs.get(attr_name):
                raise FantasticoRoaError("Resource %s model does not support attibute %s." % (self._resource_ref.name, attr_name))

            setattr(model, attr_name, attr_value)

        return model

    def _parse_fields(self, fields):
        '''This method convert a string expression for fields into a list of fields we want to list.'''

        if not fields:
            return self._supported_attrs.keys()

        attrs = []

        for field in fields.split(","):
            attrs.append(field.strip())

        return attrs

    def serialize(self, model, fields=None):
        '''This method serialize the given model into a json object.

        :param model: The model we want to convert to JSON object.
        :param fields: A list of fields we want to include in result. Read more on :ref:`partial-object-representation`
        :type fields: str
        :returns: A dictionary containing all required attributes.
        :rtype: dict
        '''

        fields = self._parse_fields(fields)

        result = {}

        for field in fields:
            result[field] = getattr(model, field)

        return result
