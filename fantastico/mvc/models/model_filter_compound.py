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
.. py:module:fantastico.mvc.models.model_filter_compound
'''
from fantastico.exceptions import FantasticoNotSupportedError, FantasticoError
from fantastico.mvc.models.model_filter import ModelFilter, ModelFilterAbstract
from sqlalchemy.sql.expression import and_, or_

class ModelFilterCompound(ModelFilterAbstract):
    '''This class provides the api for compounding ModelFilter objects into a specified sql alchemy operation.'''
    
    def __init__(self, operation, *args):
        if len(args) < 2:
            raise FantasticoNotSupportedError("Compound filter *and* takes at least 2 simple model filters.")
        
        for arg in args:
            if not isinstance(arg, ModelFilter):
                raise FantasticoNotSupportedError("ModelFilterAnd accept only arguments of type ModelFilter.")
        
        self._operation = operation
        self._model_filters = args

    def build(self, query):
        '''This method transform the current compound statement into an sql alchemy filter.'''
        
        try:
            query = query.filter(self.get_expression())
            
            return query
        except Exception as ex:
            raise FantasticoError(ex)
    
    def get_expression(self):
        '''This method transforms calculates sqlalchemy expression held by this filter.'''
        
        return self._operation(*[model_filter.get_expression() for model_filter in self._model_filters])
    
class ModelFilterAnd(ModelFilterCompound):
    '''This class provides a compound filter that allows **and** conditions against models. Below you can find a simple example:
    
        .. code-block:: python
        
            id_gt_filter = ModelFilter(PersonModel.id, 1, ModelFilter.GT)
            id_lt_filter = ModelFilter(PersonModel.id, 5, ModelFilter.LT)
            name_like_filter = ModelFilter(PersonModel.name, '%%john%%', ModelFilter.LIKE)
            
            complex_condition = ModelFilterAnd(id_gt_filter, id_lt_filter, name_like_filter)
    '''
    
    def __init__(self, *args):
        super(ModelFilterAnd, self).__init__(and_, *args)
        
class ModelFilterOr(ModelFilterCompound):
    '''This class provides a compound filter that allows **or** conditions against models. Below you can find a simple example:

        .. code-block:: python
        
            id_gt_filter = ModelFilter(PersonModel.id, 1, ModelFilter.GT)
            id_lt_filter = ModelFilter(PersonModel.id, 5, ModelFilter.LT)
            name_like_filter = ModelFilter(PersonModel.name, '%%john%%', ModelFilter.LIKE)
            
            complex_condition = ModelFilterOr(id_gt_filter, id_lt_filter, name_like_filter)
    '''
    
    def __init__(self, *args):
        super(ModelFilterOr, self).__init__(or_, *args)