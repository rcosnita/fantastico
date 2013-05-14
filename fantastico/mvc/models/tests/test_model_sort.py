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
.. py:module:: fantastico.mvc.models.tests.test_model_sort
'''
from fantastico.exceptions import FantasticoNotSupportedError
from fantastico.mvc.models.model_sort import ModelSort
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer

class ModelSortTest(FantasticoUnitTestsCase):
    '''This class provides the test cases for model sort filter.'''
    
    def init(self):
        self._id_col = Column("id", Integer)
    
    def test_modelsort_dir_notsupported(self):
        '''This test case ensures an exception is raised if model sort given direction is not supported.'''
        
        with self.assertRaises(FantasticoNotSupportedError):
            ModelSort(self._id_col, "xxx")
    
    def test_modelsort_col_notsupported(self):
        '''This test case ensures an exception is raised if the given column type is not supported.'''
        
        with self.assertRaises(FantasticoNotSupportedError):
            ModelSort(Mock(), ModelSort.ASC)
    
    def test_modelsort_ok(self):
        '''This test case ensures modelsort filter is correctly built.'''
        
        expected_result = Mock()
        
        query = Mock()
        query.order_by = Mock(return_value=expected_result)
        
        for sort_dir in ModelSort.get_supported_sort_dirs(self):
            model_sort = ModelSort(self._id_col, sort_dir)
            new_query = model_sort.build(query)

            self.assertEqual(self._id_col, model_sort.column)
            self.assertEqual(sort_dir, model_sort.sort_dir)            
            self.assertEqual(expected_result, new_query)