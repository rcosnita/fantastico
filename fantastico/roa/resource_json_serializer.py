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
from fantastico.roa.resource_json_serializer_exceptions import ResourceJsonSerializerError
import inspect
import json
import re

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
        self._subresources_attrs = self._identify_subres_attributes()
        self._supported_attrs = self._identify_public_attrs(self._resource_ref.model)


    def _identify_subres_attributes(self):
        '''This method returns all subresource attributes which must be ignored by serializer.'''

        attrs = {}

        subresources = self._resource_ref.subresources

        if not subresources:
            return attrs

        for subresource_attr in subresources.keys():
            attrs[subresource_attr] = True

        return attrs

    def _identify_public_attrs(self, model_cls):
        '''This method returns a dictionary containing all public attributes of a given model class.'''

        public_attrs = {}

        for attr_name in model_cls.__dict__.keys():
            if attr_name.startswith("_") or attr_name.startswith("__"):
                continue

            if self._subresources_attrs.get(attr_name):
                continue

            attr = getattr(model_cls, attr_name)

            if inspect.ismethod(attr) or inspect.isfunction(attr):
                continue

            public_attrs[attr_name] = True

        return public_attrs

    def deserialize(self, body):
        '''This method converts the given body into a concrete model (if possible).

        :param body: A JSON object we want to convert to the model compatible with this serializer.
        :type body: dict
        :returns: A model instance initiated with attributes from the given dictionary.
        :raises fantastico.roa.resource_json_serializer_exceptions.ResourceJsonSerializerError:
            Whenever given body contains entries which are not supported by resource underlining model.
        '''

        model_cls = self._resource_ref.model

        model = model_cls()

        body = json.loads(body)
        for attr_name, attr_value in body.items():
            if not self._supported_attrs.get(attr_name):
                raise ResourceJsonSerializerError("Resource %s model does not support attibute %s." % \
                                                  (self._resource_ref.name, attr_name))

            setattr(model, attr_name, attr_value)

        return model

    def _parse_fields(self, fields):
        '''This method convert a string expression for fields into a list of fields we want to list.'''

        if not fields:
            return self._supported_attrs.keys()

        attrs = []

        composed_attrs = re.findall(r"[a-z]{1,}\(.*?\)", fields)

        for composed_attr in composed_attrs:
            fields = fields.replace(composed_attr, "")

            paranthesis = composed_attr.find("(")
            attr_parent = composed_attr[:paranthesis].strip()

            attr_children = composed_attr[paranthesis + 1:-1].split(",")

            for attr in attr_children:
                field = "%s.%s" % (attr_parent, attr.strip())

                attrs.append(field)

        for field in fields.split(","):
            field = field.strip()

            if not field:
                continue

            attrs.append(field)

        return attrs

    def _serialize_subfield_list(self, subfield, subfield_name, attr_name, result):
        '''This method serializes the subfield list mapped under subfield_name into result dictionary.'''

        if not result.get(subfield_name):
            result[subfield_name] = []

        idx = 0

        for item in subfield:
            if len(result[subfield_name]) < idx + 1:
                result[subfield_name].append({})

            try:
                result[subfield_name][idx][attr_name] = getattr(item, attr_name)
            except AttributeError:
                raise ResourceJsonSerializerError("Submodel %s does not have attribute %s." % \
                                                  (subfield_name, attr_name))

            idx += 1

    def _serialize_subfield_obj(self, subfield, subfield_name, attr_name, result):
        '''This method serializes the subfield object mapped under subfield_name into result dictionary.'''

        if not result.get(subfield_name):
            result[subfield_name] = {}

        try:
            result[subfield_name][attr_name] = getattr(subfield, attr_name)
        except AttributeError:
            raise ResourceJsonSerializerError("Submodel %s does not have attribute %s." % \
                                              (subfield_name, attr_name))

    def serialize(self, model, fields=None):
        '''This method serialize the given model into a json object.

        :param model: The model we want to convert to JSON object.
        :param fields: A list of fields we want to include in result. Read more on :ref:`partial-object-representation`
        :type fields: str
        :returns: A dictionary containing all required attributes.
        :rtype: dict
        :raises fantastico.roa.resource_json_serializer_exceptions.ResourceJsonSerializerError:
            Whenever requested fields for serialization are not found in model attributes.
        '''

        fields = self._parse_fields(fields)

        result = {}

        for field in fields:
            if field.find(".") == -1:
                try:
                    result[field] = getattr(model, field)
                except AttributeError:
                    raise ResourceJsonSerializerError("Model does not have attribute %s." % field)

                continue

            subfield_name, subfield_attr = field.split(".")

            subfield = getattr(model, subfield_name)

            if isinstance(subfield, list):
                self._serialize_subfield_list(subfield, subfield_name, subfield_attr, result)
            else:
                self._serialize_subfield_obj(subfield, subfield_name, subfield_attr, result)

        return result
