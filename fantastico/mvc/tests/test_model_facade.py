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
from fantastico.exceptions import FantasticoIncompatibleClassError
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

        self._facade = ModelFacade(Mock(), Mock())

        self.assertRaises(FantasticoIncompatibleClassError, self._facade.new_model, *[])