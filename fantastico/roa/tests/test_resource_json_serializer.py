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
from fantastico.roa.resource_json_serializer_exceptions import ResourceJsonSerializerError
from fantastico.roa.roa_exceptions import FantasticoRoaError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Float
import json

class ResourceJsonSerializerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for resource json serializer.'''

    resource_ref = None
    _serializer = None

    @classmethod
    def setup_once(cls):
        '''This method is invoked once for setting up common dependencies for all test cases.'''

        FantasticoUnitTestsCase.setup_once()

        resource = Resource(name="Invoice", url="/invoices", subresources={"items": []})
        resource._model = InvoiceMock
        cls.resource_ref = resource

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

        resource = self._serializer.deserialize(json.dumps(body))

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
            self._serializer.deserialize(json.dumps(body))

        self.assertIsInstance(ctx.exception, ResourceJsonSerializerError)
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
        self.assertIsNone(json_obj.get("items"))

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

    def test_serialize_resource_composed_1tomany_ok(self):
        '''This test case ensures resource 1 to many relations can be serialized.'''

        fields = "series,number,items(quantity,price)"

        items = [InvoiceLineItemMock(name="Product 1", quantity=5, price=3.0),
                 InvoiceLineItemMock(name="Product 2", quantity=2, price=1.0)]

        model = InvoiceMock(series="RR", number=111, total=20.00, vat_percent=0.24, vat=0.19, items=items)
        model.id = 1

        json_obj = self._serializer.serialize(model, fields)

        self.assertIsInstance(json_obj, dict)
        self.assertEqual(json_obj["series"], model.series)
        self.assertEqual(json_obj["number"], model.number)
        self.assertNotIn("id", json_obj)
        self.assertNotIn("total", json_obj)
        self.assertNotIn("vat_percent", json_obj)
        self.assertNotIn("vat", json_obj)

        idx = 0

        for item in json_obj.get("items"):
            self.assertIsInstance(item, dict)
            self.assertEqual(item["quantity"], items[idx].quantity)
            self.assertEqual(item["price"], items[idx].price)
            self.assertNotIn("id", item)
            self.assertNotIn("name", item)

            idx += 1

    def test_serialize_resource_composed_partial_1to1(self):
        '''This test case ensures 1to1 relation of resources are correctly rendered.'''

        fields = "series,number,items(quantity,price)"

        items = InvoiceLineItemMock(name="Product 1", quantity=5, price=3.0)

        model = InvoiceMock(series="RR", number=111, total=20.00, vat_percent=0.24, vat=0.19, items=items)
        model.id = 1

        json_obj = self._serializer.serialize(model, fields)

        self.assertIsInstance(json_obj, dict)
        self.assertEqual(json_obj["series"], model.series)
        self.assertEqual(json_obj["number"], model.number)
        self.assertNotIn("id", json_obj)
        self.assertNotIn("total", json_obj)
        self.assertNotIn("vat_percent", json_obj)
        self.assertNotIn("vat", json_obj)

        item = json_obj.get("items")

        self.assertIsInstance(item, dict)
        self.assertEqual(item["quantity"], items.quantity)
        self.assertEqual(item["price"], items.price)
        self.assertNotIn("id", item)
        self.assertNotIn("name", item)

    def test_serialize_mainresource_unknown_attr(self):
        '''This test case ensures an exception is raised when an unknown field is requested for partial representation.'''

        fields = "unknown_attribute"

        model = InvoiceMock()

        with self.assertRaises(FantasticoRoaError) as ctx:
            self._serializer.serialize(model, fields)

        self.assertIsInstance(ctx.exception, ResourceJsonSerializerError)
        self.assertTrue(str(ctx.exception).find("unknown_attribute") > -1)

    def _test_serialize_subresource_1ton_unknown(self, fields, subfield_name, attr_name, items):
        '''This method provides a template for generating errors into subresources partial serialization.'''

        model = InvoiceMock(items=items)
        model.id = 1

        with self.assertRaises(FantasticoRoaError) as ctx:
            self._serializer.serialize(model, fields)

        self.assertIsInstance(ctx.exception, ResourceJsonSerializerError)
        self.assertTrue(str(ctx.exception).find(attr_name) > -1)
        self.assertTrue(str(ctx.exception).find(subfield_name) > -1)

    def test_serialize_subresource_1to1_unknown_attr(self):
        '''This test case ensures an exception is raised when an unknown field belonging to a subresource is requested for
        partial representation.'''

        self._test_serialize_subresource_1ton_unknown("id,items(unknown_attr)", "items", "unknown_attr",
                                                      InvoiceLineItemMock())

    def test_serialize_subresource_1ton_unknown_attr(self):
        '''This test case ensures an exception is raised when an unknown field belonging to a subresource is requested for one
        to many partial representation.'''

        self._test_serialize_subresource_1ton_unknown("id,items(unknown_attr)", "items", "unknown_attr",
                                                      [InvoiceLineItemMock(), InvoiceLineItemMock()])

class InvoiceMock(BASEMODEL):
    __tablename__ = "invoices_mock"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    series = Column("series", String(10), nullable=False)
    number = Column("number", Integer, nullable=False)
    total = Column("total", Float)
    vat_percent = Column("vat_percent", Float)
    vat = Column("vat", Float)
    items = []

    def __init__(self, series=None, number=None, total=None, vat_percent=None, vat=None,
                 items=None):
        self.series = series
        self.number = number
        self.total = total
        self.vat_percent = vat_percent
        self.vat = vat
        self.items = items

class InvoiceLineItemMock(BASEMODEL):
    __tablename__ = "invoice_lineitems"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(100), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("price", Float, nullable=False)

    def __init__(self, name=None, quantity=None, price=None):
        self.name = name
        self.quantity = quantity
        self.price = price
