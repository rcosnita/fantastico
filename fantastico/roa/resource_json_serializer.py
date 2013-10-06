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

    def deserialize(self, body):
        '''This method converts the given body into a concrete model (if possible).'''

        model_cls = self._resource_ref.model

        model = model_cls()

        for attr_key, attr_value in body.items():
            if not hasattr(model, attr_key):
                raise FantasticoRoaError("Resource %s model does not support attibute %s." % (self._resource_ref.name, attr_key))

            setattr(model, attr_key, attr_value)

        return model
