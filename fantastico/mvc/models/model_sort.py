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
.. py:module:: fantastico.mvc.models.model_sort
'''
from fantastico.exceptions import FantasticoNotSupportedError
from fantastico.mvc.models.model_filter import ModelFilterAbstract
from sqlalchemy.schema import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute

class ModelSort(ModelFilterAbstract):
    '''This class provides a filter that knows how to sort rows from a query result set. It is extremely easy to use:
    
        .. code-block:: python
        
            id_sort_asc = ModelSort(PersonModel.id, ModelSort.ASC)
    '''

    ASC = "asc"
    DESC = "desc"
    
    _column = None
    _sort_dir = None
    
    @property
    def column(self):
        '''This property holds the column we are currently sorting.'''
        
        return self._column
    
    @property
    def sort_dir(self):
        '''This property holds the sort direction we are currently using.'''
        
        return self._sort_dir
    
    def __init__(self, column, sort_dir=None):
        sort_dir = sort_dir or ModelSort.ASC
        
        if not isinstance(column, Column) and not isinstance(column, InstrumentedAttribute):
            raise FantasticoNotSupportedError("ModelSort column must be of type Column.")
        
        if not self._is_sort_dir_supported(sort_dir):
            raise FantasticoNotSupportedError("ModelSort does not support %s sort direction." % sort_dir)
        
        self._column = column
        self._sort_dir = sort_dir
        self._cached_expr = None
    
    def _is_sort_dir_supported(self, sort_dir):
        '''This method detects if the specified sort dir is supported.'''
        
        return sort_dir in self.get_supported_sort_dirs()
    
    def get_supported_sort_dirs(self):
        '''This method returns all supported sort directions. Currently only ASC / DESC directions are supported.'''
    
        return [ModelSort.ASC, ModelSort.DESC]
    
    def build(self, query):
        '''This method appends sort_by clause to the given query.'''
        
        return query.order_by(self.get_expression())
    
    def get_expression(self):
        '''This method returns the sqlalchemy expression held by this filter.'''
        
        if self._cached_expr is not None:
            return self._cached_expr
        
        if self.sort_dir == ModelSort.ASC:
            self._cached_expr = self.column.asc()
        elif self.sort_dir == ModelSort.DESC:
            self._cached_expr = self.column.desc()
        
        return self._cached_expr