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
from fantastico.exceptions import FantasticoIncompatibleClassError, \
    FantasticoDbError, FantasticoDbNotFoundError
from fantastico.mvc import BASEMODEL
from fantastico.mvc.model_facade import ModelFacade
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
        self._session.commit = lambda: None
        
        model_id = self._facade.create(model)
        
        self.assertEqual(1, len(model_id))
        self.assertEqual(1, model_id[0])
        self.assertEqual(1, model.id)
        
    def test_create_exception_unhandled(self):
        '''This test case makes sure a model creation exception is wrapped correctly into a concrete fantastico exception.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe") 
        
        self._session.add = Mock(side_effect=Exception("Unhandled exception"))
        
        self.assertRaises(FantasticoDbError, self._facade.create, *[model])
        
    def test_update_ok(self):
        '''This test case ensures a model can be updated correctly using model facade.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter_by = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[model])

        
        def merge(model):
            model.first_name = "John Changed"
        
        self._session.merge = merge
        self._session.commit = lambda: None
        
        self._facade.update(model)
        
        self.assertEqual("John Changed", model.first_name)
        
    def test_update_exception_unhandled(self):
        '''This test case ensures a model update gracefully handles all unhandled exceptions.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter_by = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[model])

        self._session.merge = Mock(side_effect=Exception("Unhandled exception"))
        self._session.commit = lambda: None
        
        self.assertRaises(FantasticoDbError, self._facade.update, *[model])
        
    def test_update_exception_notfound(self):
        '''This test case ensures a model update exception is raised when the given model does not exist.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter_by = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[])
        
        self.assertRaises(FantasticoDbNotFoundError, self._facade.update, *[model])
    
    def test_find_by_pk_ok(self):
        '''This test case ensures find_by_pk method retrieves a model instance when a record is found by id.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter_by = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[model])

        response = self._facade.find_by_pk({PersonModelTest.id: 1})
        
        self.assertEqual(model, response)
        
    def test_find_by_pk_notfound(self):
        '''This test case ensures find_by_pk method raises an exception when a matching record is not found.'''
        
        model = PersonModelTest(first_name="John", last_name="Doe")
        model.id = 1
        
        self._session.query = Mock(return_value=self._session)
        self._session.filter_by = Mock(return_value=self._session)
        self._session.all = Mock(return_value=[])

        with self.assertRaises(FantasticoDbNotFoundError):
            self._facade.find_by_pk({PersonModelTest.id: 1})