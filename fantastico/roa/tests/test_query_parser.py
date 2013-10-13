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
.. py:module:: fantastico.roa.tests.test_query_parser
'''

from fantastico.mvc import BASEMODEL
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.mvc.models.model_filter_compound import ModelFilterOr, ModelFilterAnd
from fantastico.roa.query_parser import QueryParser
from fantastico.roa.query_parser_exceptions import QueryParserOperationInvalidError
from fantastico.roa.roa_exceptions import FantasticoRoaError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text
from fantastico.mvc.models.model_sort import ModelSort

class QueryParserTests(FantasticoUnitTestsCase):
    '''This class provides the tests cases for query parser.'''

    _query_parser = None

    def init(self):
        '''This method setup common dependencies for all test cases: query_parser'''

        self._query_parser = QueryParser()

    def test_parse_filter_empty(self):
        '''This test case ensures None is returned for an empty filter passed as argument.'''

        filters = [None, "", "      "]
        model = Mock()

        for filter_expr in filters:
            result = self._query_parser.parse_filter(filter_expr, model)

            self.assertIsNone(result)

    def test_parse_filter_binary_invalidcolumn(self):
        '''This test case ensures an exception is raised if a column name not found in the model is given for
        binary operations.'''

        filter_expr = "eq(not_supported, vat)"

        with self.assertRaises(FantasticoRoaError) as ctx:
            self._query_parser.parse_filter(filter_expr, AppSettingMock)

        self.assertTrue(str(ctx.exception).find("not_supported") > -1)

    def test_parse_filter_binary_notenougharguments(self):
        '''This test case ensures an exception is raised if a binary operation does not receive enough arguments.'''

        filters = ["eq()", "eq(a,)", "eq(,b)"]

        for filter_expr in filters:
            with self.assertRaises(FantasticoRoaError) as ctx:
                self._query_parser.parse_filter(filter_expr, Mock())

            self.assertTrue(str(ctx.exception).find("eq") > -1)

    def test_parse_filter_invalidoperation(self):
        '''This test case ensures an exception is raised when the given operation is not found.'''

        filter_expr = "invalid_operation(a, b)"

        with self.assertRaises(FantasticoRoaError):
            self._query_parser.parse_filter(filter_expr, Mock())

    def _test_parse_binary_filter(self, filter_expr, expected_column, expected_value, expected_operation):
        '''This is a template method for executing test cases against binary operation: eq, like, gt, ge, lt, le, in.'''

        result = self._query_parser.parse_filter(filter_expr, AppSettingMock)

        self.assertIsInstance(result, ModelFilter)
        self.assertEqual(result.column, expected_column)
        self.assertEqual(result.ref_value, expected_value)
        self.assertEqual(result.operation, expected_operation)

    def test_parse_filter_eq(self):
        '''This test case ensures an equality filter can be parsed to a query object.'''

        filter_expr = "eq(name   , \"vat\")"

        self._test_parse_binary_filter(filter_expr, AppSettingMock.name, "vat", ModelFilter.EQ)

    def test_parse_filter_like(self):
        '''This test case ensures like operation is correctly parsed'''

        filter_expr = "like    (name   , \"%vat%\"   )"

        self._test_parse_binary_filter(filter_expr, AppSettingMock.name, "%vat%", ModelFilter.LIKE)

    def test_parse_filter_gt(self):
        '''This test case ensures greater than operation is correctly parsed.'''

        filter_expr = "gt(value, 0.19)"

        self._test_parse_binary_filter(filter_expr, AppSettingMock.value, 0.19, ModelFilter.GT)

    def test_parse_filter_ge(self):
        '''This test case ensures greater or equal than operation is correctly parsed.'''

        filter_expr = "ge(value, 0.19)"

        self._test_parse_binary_filter(filter_expr, AppSettingMock.value, 0.19, ModelFilter.GE)

    def test_parse_filter_lt(self):
        '''This test case ensures less than operation is correctly parsed.'''

        filter_expr = "lt(value, 0.19)"

        self._test_parse_binary_filter(filter_expr, AppSettingMock.value, 0.19, ModelFilter.LT)

    def test_parse_filter_le(self):
        '''This test case ensures less or equal than operation is correctly parsed.'''

        filter_expr = "le(value, 0.19)"

        self._test_parse_binary_filter(filter_expr, AppSettingMock.value, 0.19, ModelFilter.LE)

    def test_parse_filter_in(self):
        '''This test case ensures in operation is correctly parsed.'''

        filter_expr = "in(value, [0.19, 0.20, 0.21])"

        self._test_parse_binary_filter(filter_expr, AppSettingMock.value,
                                       [0.19, 0.20, 0.21],
                                       ModelFilter.IN)

    def test_parse_filter_compoundor(self):
        '''This test case ensures compound or operations is correctly parsed.'''

        filter_expr = "or(eq(name, \"vat\"), eq(value, \"en_US\"))"

        result = self._query_parser.parse_filter(filter_expr, AppSettingMock)

        self.assertIsInstance(result, ModelFilterOr)

        result_filters = result.model_filters

        self.assertEqual(len(result_filters), 2)

        self.assertIsInstance(result_filters[0], ModelFilter)
        self.assertEqual(result_filters[0].column, AppSettingMock.name)
        self.assertEqual(result_filters[0].ref_value, "vat")
        self.assertEqual(result_filters[0].operation, ModelFilter.EQ)

        self.assertIsInstance(result_filters[1], ModelFilter)
        self.assertEqual(result_filters[1].column, AppSettingMock.value)
        self.assertEqual(result_filters[1].ref_value, "en_US")
        self.assertEqual(result_filters[1].operation, ModelFilter.EQ)

    def test_parse_filter_compoundand(self):
        '''This test case ensures compound or operations is correctly parsed.'''

        filter_expr = "and(eq(name, \"vat\"), eq(value, \"en_US\"))"

        result = self._query_parser.parse_filter(filter_expr, AppSettingMock)

        self.assertIsInstance(result, ModelFilterAnd)

        result_filters = result.model_filters

        self.assertEqual(len(result_filters), 2)

        self.assertIsInstance(result_filters[0], ModelFilter)
        self.assertEqual(result_filters[0].column, AppSettingMock.name)
        self.assertEqual(result_filters[0].ref_value, "vat")
        self.assertEqual(result_filters[0].operation, ModelFilter.EQ)

        self.assertIsInstance(result_filters[1], ModelFilter)
        self.assertEqual(result_filters[1].column, AppSettingMock.value)
        self.assertEqual(result_filters[1].ref_value, "en_US")
        self.assertEqual(result_filters[1].operation, ModelFilter.EQ)

    def test_parse_filter_compoundand_with_or(self):
        '''This test case ensures compound filters can receive other compound filters as argument.'''

        filter_expr = "and(or(eq(name, \"vat\"), eq(name, \"locale\")), eq(name, \"vat\"))"

        result = self._query_parser.parse_filter(filter_expr, AppSettingMock)

        self.assertIsInstance(result, ModelFilterAnd)

        result_filters = result.model_filters

        self.assertEqual(len(result_filters), 2)

        result_or = result_filters[0]
        result_eq = result_filters[1]

        self.assertIsInstance(result_or, ModelFilterOr)

        self.assertIsInstance(result_eq, ModelFilter)
        self.assertEqual(result_eq.column, AppSettingMock.name)
        self.assertEqual(result_eq.ref_value, "vat")
        self.assertEqual(result_eq.operation, ModelFilter.EQ)

    def test_parse_filter_compound_notenoughargs(self):
        '''This test case ensures an exception is raised when not enough arguments are passed to **or** filter.'''

        filters = ["or()", "or(,)", "or     (      )"]

        for filter_expr in filters:
            with self.assertRaises(QueryParserOperationInvalidError) as ctx:
                self._query_parser.parse_filter(filter_expr, Mock())

        self.assertTrue(str(ctx.exception).find("or ") > -1)

    def test_parse_filter_compound_invalidarg(self):
        '''This test case ensures an exception is raised if an invalid argument is passed to a compound filter.'''

        filter_expr = "or(eq(), eq(a,b))"

        with self.assertRaises(QueryParserOperationInvalidError) as ctx:
            self._query_parser.parse_filter(filter_expr, AppSettingMock)

        self.assertTrue(str(ctx.exception).find("eq") > -1)

    def test_parse_sort_empty(self):
        '''This test case ensures an empty list is returned for empty sort expressions.'''

        sort_expr = []

        self.assertEqual(self._query_parser.parse_sort(sort_expr, Mock()), [])

    def _test_parse_sort(self, sort_expr, expected_col, expected_dir):
        '''This method provides a template for testing simple sort filters.'''

        results = self._query_parser.parse_sort(sort_expr, AppSettingMock)

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertIsInstance(result, ModelSort)

        self.assertEqual(result.column, expected_col)
        self.assertEqual(result.sort_dir, expected_dir)

    def test_parse_sort_asc(self):
        '''This test case ensures sort ascending is parsed correctly.'''

        sort_expr = ["asc(name)"]

        self._test_parse_sort(sort_expr, AppSettingMock.name, ModelSort.ASC)

    def test_parse_sort_desc(self):
        '''This test case ensures sort descending is parsed correctly.'''

        sort_expr = ["desc(name)"]

        self._test_parse_sort(sort_expr, AppSettingMock.name, ModelSort.DESC)

    def test_parse_sort_invalidarg(self):
        '''This test case ensures invalid argument passed into sort expressions fail.'''

        sort_expr = ["asc(not_found)"]

        with self.assertRaises(FantasticoRoaError) as ctx:
            self._query_parser.parse_sort(sort_expr, AppSettingMock)

        self.assertTrue(str(ctx.exception).find(" not_found ") > -1)

class AppSettingMock(BASEMODEL):
    '''This is a very simple setting of an application.'''

    __tablename__ = "app_settings_mock"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(80), unique=True, nullable=False)
    value = Column("value", Text, nullable=False)

    def __init__(self, name, value):
        self.name = name
        self.value = value
