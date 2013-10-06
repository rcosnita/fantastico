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
.. py:module:: fantastico.roa.tests.test_resource_json_serializer
'''
from fantastico.mvc import BASEMODEL
from fantastico.roa.resource_decorator import Resource
from fantastico.roa.resource_json_serializer import ResourceJsonSerializer
from fantastico.roa.roa_exceptions import FantasticoRoaError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Float

class ResourceJsonSerializerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for resource json serializer.'''

    resource_ref = None
    _serializer = None

    @classmethod
    def setup_once(cls):
        '''This method is invoked once for setting up common dependencies for all test cases.'''

        FantasticoUnitTestsCase.setup_once()

        from fantastico.roa.resources_registry import ResourcesRegistry

        cls.resource_ref = ResourcesRegistry().find_by_name("Invoice")

    def init(self):
        '''This method is invoked before each test case in order to set transient dependencies.'''

        self._serializer = ResourceJsonSerializer(self.resource_ref)

    def test_resource_deserialize_ok(self):
        '''This test case ensures a given dictionary is correctly converted into the resource type requested.'''

        body = {"id": 1,
                "series": "RR",
                "number": 11111,
                "total": 20.00,
                "vat_percent": 0.24,
                "vat": 4.8}

        resource = self._serializer.deserialize(body)

        self.assertIsInstance(resource, self.resource_ref.model)
        self.assertEqual(resource.id, body["id"])
        self.assertEqual(resource.series, body["series"])
        self.assertEqual(resource.number, body["number"])
        self.assertEqual(resource.total, body["total"])
        self.assertEqual(resource.vat_percent, body["vat_percent"])
        self.assertEqual(resource.vat, body["vat"])

    def test_deserialize_unknown_attr(self):
        '''This test case ensures an exception is raised whenever we try to set an unknown attribute to the underlining
        resource model.'''

        body = {"unknown_column": "unknown_value"}

        with self.assertRaises(FantasticoRoaError) as ctx:
            self._serializer.deserialize(body)

        self.assertTrue(str(ctx.exception).find("unknown_column") > -1)

    def test_serialize_mainresource_ok(self):
        '''This test case ensures a given resource model is correctly serialized into a json object.'''

        model = InvoiceMock(series="RR", number=111, total=20.00, vat_percent=0.24, vat=0.19)
        model.id = 1

        json_obj = self._serializer.serialize(model)

        self.assertIsInstance(json_obj, dict)
        self.assertEqual(json_obj["id"], model.id)
        self.assertEqual(json_obj["series"], model.series)
        self.assertEqual(json_obj["number"], model.number)
        self.assertEqual(json_obj["total"], model.total)
        self.assertEqual(json_obj["vat_percent"], model.vat_percent)
        self.assertEqual(json_obj["vat"], model.vat)

    def test_serialize_mainresource_partial_ok(self):
        '''This test case ensures a resource partial serialization work as expected.'''

        fields = "  series, number    "

        model = InvoiceMock(series="RR", number=111, total=20.00, vat_percent=0.24, vat=0.19)
        model.id = 1

        json_obj = self._serializer.serialize(model, fields)

        self.assertIsInstance(json_obj, dict)
        self.assertEqual(json_obj["series"], model.series)
        self.assertEqual(json_obj["number"], model.number)
        self.assertNotIn("id", json_obj)
        self.assertNotIn("total", json_obj)
        self.assertNotIn("vat_percent", json_obj)
        self.assertNotIn("vat", json_obj)

@Resource(name="Invoice", url="/invoices")
class InvoiceMock(BASEMODEL):
    __tablename__ = "invoices_mock"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    series = Column("series", String(10), nullable=False)
    number = Column("number", Integer, nullable=False)
    total = Column("total", Float)
    vat_percent = Column("vat_percent", Float)
    vat = Column("vat", Float)

    def __init__(self, series=None, number=None, total=None, vat_percent=None, vat=None):
        self.series = series
        self.number = number
        self.total = total
        self.vat_percent = vat_percent
        self.vat = vat
