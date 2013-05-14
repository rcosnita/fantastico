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
.. py:module:: fantastico.mvc.tests.test_model_facade
'''
from fantastico.exceptions import FantasticoIncompatibleClassError, FantasticoDbError, FantasticoDbNotFoundError
from fantastico.mvc import BASEMODEL
from fantastico.mvc.model_facade import ModelFacade
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.mvc.models.model_sort import ModelSort
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

class PersonModelTest(BASEMODEL):
    '''This is just a simple base model used in unit tests.'''
    
    __tablename__ = "persons"
    
    id = Column("id", Integer, autoincrement=True, primary_key=True)
    first_name = Column("first_name", String(50))
    last_name = Column("last_name", String(50))
    
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class ModelFacadeTests(FantasticoUnitTestsCase):
    '''This class provides test suite for generating a model facade for BaseModel classes.'''
    
    def init(self):
        self._session = Mock()
        self._facade = ModelFacade(PersonModelTest, self._session)
        self._rollbacked = False
        self._model_filter = None
        self._model_sort = None
        
    def test_new_model_ok(self):
        '''This test case ensures a model facade can obtain an instance of a given class.'''
        
        for model in [self._facade.new_model("John", **{"last_name": "Doe"}),
                      self._facade.new_model("John", last_name="Doe")]:
            self.assertEqual(PersonModelTest, self._facade.model_cls)
            self.assertIsInstance(model, BASEMODEL)
            self.assertEqual("John", model.first_name)
            self.assertEqual("Doe", model.last_name)
            
    def test_new_model_incompatible(self):
        '''This test case makes sure a model facade instance raises an exception if given model class does not
        extend **BASEMODEL**.'''

        with self.assertRaises(FantasticoIncompatibleClassError):
            ModelFacade(Mock(), Mock())
        
    def test_create_ok(self):
        '''This test case makes sure a model can be correctly saved using a facade.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        
        def add(model):
            model.id = 1
            
            return self._session
        
        self._session.add = add
        
        model_id = self._facade.create(model)
        
        self.assertFalse(self._rollbacked)
        self.assertEqual(1, len(model_id))
        self.assertEqual(1, model_id[0])
        self.assertEqual(1, model.id)
        
    def test_create_exception_unhandled(self):
        '''This test case makes sure a model creation exception is wrapped correctly into a concrete fantastico exception.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe") 
        
        self._session.add = Mock(side_effect=Exception("Unhandled exception"))
        
        def rollback():
            self._rollbacked = True
            
        self._session.rollback = rollback
        
        self.assertRaises(FantasticoDbError, self._facade.create, *[model])
        self.assertTrue(self._rollbacked)
        
    def test_update_ok(self):
        '''This test case ensures a model can be updated correctly using model facade.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[model])

        
        def merge(model):
            model.first_name = "John Changed"
        
        self._session.merge = merge
        
        self._facade.update(model)
        
        self.assertFalse(self._rollbacked)
        self.assertEqual("John Changed", model.first_name)
        
    def test_update_exception_unhandled(self):
        '''This test case ensures a model update gracefully handles all unhandled exceptions.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[model])

        self._session.merge = Mock(side_effect=Exception("Unhandled exception"))
        
        def rollback():
            self._rollbacked = True
            
        self._session.rollback = rollback        
        
        self.assertRaises(FantasticoDbError, self._facade.update, *[model])
        self.assertTrue(self._rollbacked)
        
    def test_update_exception_notfound(self):
        '''This test case ensures a model update exception is raised when the given model does not exist.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[])
        
        def rollback():
            self._rollbacked = True
            
        self._session.rollback = rollback
        
        self.assertRaises(FantasticoDbNotFoundError, self._facade.update, *[model])
        self.assertTrue(self._rollbacked)
    
    def test_find_by_pk_ok(self):
        '''This test case ensures find_by_pk method retrieves a model instance when a record is found by id.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[model])

        response = self._facade.find_by_pk({PersonModelTest.id: 1})
        
        self.assertFalse(self._rollbacked)
        self.assertEqual(model, response)
        
    def test_find_by_pk_notfound(self):
        '''This test case ensures find_by_pk method raises an exception when a matching record is not found.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[])

        def rollback():
            self._rollbacked = True
            
        self._session.rollback = rollback

        with self.assertRaises(FantasticoDbNotFoundError):
            self._facade.find_by_pk({PersonModelTest.id: 1})

        self.assertTrue(self._rollbacked)
                    
    def test_delete_ok(self):
        '''This test case ensures a model can be deleted successfully if no exception occurs.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._facade.delete(model)
        
        self.assertFalse(self._rollbacked)

    def test_delete_exception_unhandled(self):
        '''This test case ensures unhandled exceptions are gracefully handled by delete method.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.delete = Mock(side_effect=Exception("Unhandled exception"))
        
        def rollback():
            self._rollbacked = True
            
        self._session.rollback = rollback

        
        with self.assertRaises(FantasticoDbError):
            self._facade.delete(model)
        
        self.assertTrue(self._rollbacked)
        
    def test_get_paged_records_ok(self):
        '''This test case ensures records can be retrieved correctly from a facade.'''
        
        expected_model = Mock()
        
        self._model_filter = ModelFilter(PersonModelTest.id, 1, ModelFilter.GT)
        self._model_sort = ModelSort(PersonModelTest.first_name)
        
        def query_mock(cls_obj):
            self.assertEqual(PersonModelTest, cls_obj)
            
            return self._session
        
        def filter_mock(expr):
            self.assertEqual(self._model_filter.get_expression(), expr)
            
            return self._session
        
        def sort_mock(expr):
            self.assertEqual(self._model_sort.get_expression(), expr)
            
            return self._session
        
        def offset_mock(offset):
            self.assertEqual(0, offset)
            
            return self._session
        
        def limit_mock(limit_count):
            self.assertEqual(4, limit_count)
            
            return self._session
        
        self._session.query = query_mock
        self._session.filter = filter_mock
        self._session.order_by = sort_mock
        self._session.offset = offset_mock
        self._session.limit = limit_mock
        self._session.all = Mock(return_value=[expected_model, expected_model, expected_model])
                
        records = self._facade.get_records_paged(start_record=0, end_record=4, 
                                                 sort_expr=self._model_sort,
                                                 filter_expr=self._model_filter)
        
        self.assertIsNotNone(records)
        self.assertEqual(3, len(records))
        
        for model in records:
            self.assertEqual(expected_model, model)
    
    def test_get_records_paged_default(self):
        '''This test case ensure records are retrieved when no filter / sort_expr are specified.'''

        def query_mock(cls_obj):
            self.assertEqual(PersonModelTest, cls_obj)
            
            return self._session
        
        def offset_mock(offset):
            self.assertEqual(0, offset)
            
            return self._session
        
        def limit_mock(limit_count):
            self.assertEqual(4, limit_count)
            
            return self._session
        
        self._session.query = query_mock
        self._session.offset = offset_mock
        self._session.limit = limit_mock
        self._session.all = Mock(return_value=[])
        
        records = self._facade.get_records_paged(start_record=0, end_record=4)
        
        self.assertIsNotNone(records)
        self.assertEqual(0, len(records))
    
    def test_get_records_paged_unhandled_exception(self):
        '''This test case ensures that any unhandled exception from filters / sql alchemy is gracefully handled.'''
        
        self._model_filter = ModelFilter(PersonModelTest.id, 1, ModelFilter.GT)
        self._model_filter.build = Mock(side_effect=Exception("Unhandled exception"))
        
        def rollback():
            self._rollbacked = True
            
        self._session.rollback = rollback
        
        with self.assertRaises(FantasticoDbError):
            self._facade.get_records_paged(start_record=0, end_record=4, filter_expr=self._model_filter)

        self.assertTrue(self._rollbacked)
        
    def test_count_records_default_ok(self):
        '''This test case ensures count method works correctly.'''

        def query_mock(cls_obj):
            self.assertEqual(PersonModelTest, cls_obj)
            
            return self._session
        
        self._session.query = query_mock
        self._session.count = Mock(return_value=20)
        
        records_count = self._facade.count_records()
        
        self.assertEqual(20, records_count)
    
    def test_count_records_filtered_ok(self):
        '''This test case ensures count method works correctly when a filter is given.'''
        
        self._model_filter = ModelFilter(PersonModelTest.id, 1, ModelFilter.GT)
        
        def query_mock(cls_obj):
            self.assertEqual(PersonModelTest, cls_obj)
            
            return self._session
        
        def filter_mock(expr):
            self.assertEqual(self._model_filter.get_expression(), expr)
            
            return self._session
        
        self._session.query = query_mock
        self._session.filter = filter_mock
        self._session.count = Mock(return_value=20)
        
        records_count = self._facade.count_records(self._model_filter)
        
        self.assertEqual(20, records_count)

    def test_count_records_unhandled_exception(self):
        '''This test case ensures count method gracefully handles unexpected exceptions.'''
        
        self._model_filter = ModelFilter(PersonModelTest.id, 1, ModelFilter.GT)
        self._model_filter.build = Mock(side_effect=Exception("Unhandled exception"))
        
        def rollback():
            self._rollbacked = True
            
        self._session.rollback = rollback
        
        with self.assertRaises(FantasticoDbError):
            self._facade.count_records(self._model_filter)

        self.assertTrue(self._rollbacked)        