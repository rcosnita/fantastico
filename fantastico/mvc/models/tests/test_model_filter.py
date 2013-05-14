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
.. py:module:fantastico.mvc.models.tests.test_model_filter
'''
from fantastico.exceptions import FantasticoNotSupportedError
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer

class ModelFilterTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for ensuring model filter class works correctly.'''
    
    def test_model_filter_noquery(self):
        '''This test case ensures no exception occurs if the underlining query is None.'''
        
        model = Mock()
        
        model_filter = ModelFilter(model.id, 1, "gt")
        self.assertIsNone(model_filter.build(None))
    
    def test_model_filter_operation_notsupported(self):
        '''This test case ensures an exception is raised when the requested operation is not supported.'''
        
        model = Mock()
        
        with self.assertRaises(FantasticoNotSupportedError):
            ModelFilter(model.id, 1, "xx")
    
    def test_model_filter_ok(self):
        '''This test case ensures model filter can correctly enrich a given query with the right filters for
        all supported operations.'''

        expected_result = Mock()
        
        model = Mock()
        model.id = Column("id", Integer)
        model.id.like = Mock(return_value=expected_result)
        model.id.in_ = Mock(return_value=expected_result)

        query = Mock()
        query.filter = lambda *args, **kwargs: expected_result
        
        for operation in ModelFilter.get_supported_operations():
            ref_value = 1
            
            if operation == ModelFilter.IN:
                ref_value = [ref_value]
            
            model_filter = ModelFilter(model.id, ref_value, operation)
            new_query = model_filter.build(query)
            
            self.assertEqual(model.id, model_filter.column)
            self.assertEqual(operation, model_filter.operation)
            self.assertEqual(expected_result, new_query)
    
    def test_model_filter_in_notsupported(self):
        '''This test case ensures in filter raises an exception if ref_value is not a list.'''
        
        model = Mock()
        model.id = Column("id", Integer)
        
        model_filter = ModelFilter(model.id, "invalid list", ModelFilter.IN)
        
        query = Mock()
        
        with self.assertRaises(FantasticoNotSupportedError):
            model_filter.build(query)