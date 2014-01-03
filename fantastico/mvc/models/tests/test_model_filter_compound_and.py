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
.. py:module:fantastico.mvc.models.tests.test_model_filter_compound
'''
from fantastico.exceptions import FantasticoNotSupportedError, FantasticoError
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.mvc.models.model_filter_compound import ModelFilterAnd
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

class ModelFilterAndTests(FantasticoUnitTestsCase):
    '''This class provides test suite for compound *and* model filter.'''

    def init(self):
        self._model = Mock()
        self._model.id = Column("id", Integer)

    def test_modelfilterand_noargs(self):
        '''This test case ensures compound **and** filter can not be built without arguments.'''

        with self.assertRaises(FantasticoNotSupportedError):
            ModelFilterAnd()

    def test_modelfilterand_notenoughargs(self):
        '''This test case ensures compound **and** filter can not be built with a single argument.'''

        with self.assertRaises(FantasticoNotSupportedError):
            ModelFilterAnd(ModelFilter(self._model.id, 1, ModelFilter.EQ))

    def test_modelfilterand_wrongargtype(self):
        '''This test case ensures compound **and** filter works only with ModelFilter arguments.'''

        with self.assertRaises(FantasticoNotSupportedError):
            ModelFilterAnd(Mock(), Mock())

    def test_modelfilterand_ok(self):
        '''This test case ensures compound **and** filter correctly transform the filter into sql alchemy and_ statement.'''

        self._or_invoked = False

        model_filter = ModelFilterAnd(ModelFilter(self._model.id, 1, ModelFilter.EQ),
                                      ModelFilter(self._model.id, 1, ModelFilter.EQ),
                                      ModelFilter(self._model.id, 1, ModelFilter.EQ))

        query = Mock()

        def filter_fn(expr):
            self._or_invoked = True

            return Mock()

        query.filter = filter_fn

        query_new = model_filter.build(query)

        self.assertTrue(self._or_invoked)
        self.assertIsInstance(query_new, Mock)

    def test_modelfiterand_unhandled_exception(self):
        '''This test case ensures unhandled exceptions raised from ModelFilter are gracefully handled by ModelFilterAnd build.'''

        model_filter = ModelFilter(self._model.id, 1, ModelFilter.EQ)
        model_filter.get_expression = Mock(side_effect=Exception("Unhandled exception"))

        model_filter_and = ModelFilterAnd(model_filter, model_filter, model_filter)

        with self.assertRaises(FantasticoError):
            model_filter_and.build(Mock())

    def test_modelfilterand_eq_ok(self):
        '''This test case ensures two model filters and equality works as expected.'''

        id_col = Column("id", Integer)
        name_col = Column("name", String(100))

        filter1 = ModelFilterAnd(ModelFilter(id_col, 1, ModelFilter.EQ),
                                 ModelFilter(name_col, "john", ModelFilter.EQ))

        filter2 = ModelFilterAnd(ModelFilter(id_col, 1, ModelFilter.EQ),
                                 ModelFilter(name_col, "john", ModelFilter.EQ))

        self.assertEqual(filter1, filter2)
        self.assertEqual(hash(filter1), hash(filter2))

    def test_modelfilterand_eq_differenttype(self):
        '''This test case ensures compound model filter and can not be equal with a simple model filter.'''

        id_col = Column("id", Integer)
        name_col = Column("name", String(100))

        filter1 = ModelFilter(id_col, 1, ModelFilter.EQ)
        filter2 = ModelFilterAnd(filter1,
                                 ModelFilter(name_col, "john", ModelFilter.EQ))

        self.assertNotEqual(filter2, filter1)
        self.assertNotEqual(hash(filter2), hash(filter1))

    def test_modelfilterand_eq_different(self):
        '''This test case ensures compound model filter and is not always equal with another compound model filter and.'''

        id_col = Column("id", Integer)
        name_col = Column("name", String(100))

        filter1 = ModelFilterAnd(ModelFilter(id_col, 1, ModelFilter.EQ),
                                 ModelFilter(id_col, 1, ModelFilter.EQ))

        filter2 = ModelFilterAnd(ModelFilter(id_col, 1, ModelFilter.EQ),
                                 ModelFilter(name_col, "john", ModelFilter.EQ))

        self.assertNotEqual(filter1, filter2)
        self.assertNotEqual(hash(filter1), hash(filter2))
