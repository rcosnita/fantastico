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
.. py:module::
'''
from abc import ABCMeta, abstractmethod # pylint: disable=W0611
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.mvc.models.model_filter_compound import ModelFilterOr, ModelFilterAnd
from fantastico.mvc.models.model_sort import ModelSort
from fantastico.roa.query_parser_exceptions import QueryParserOperationInvalidError
import json
import re

class QueryParserOperation(object, metaclass=ABCMeta):
    '''This class defines the contract for a query parser operation.'''

    def __init__(self, operation, argument, parser):
        self._operation = operation
        self._argument = argument
        self._parser = parser

    @abstractmethod
    def build_filter(self, model):
        '''This method builds the model filter (:doc:`fantastico.mvc.models.model_filter.ModelFilter`).'''

    @abstractmethod
    def validate(self, model):
        '''This method validates the given operation and argument in order to ensure a filter can be built.

        :raises fantastico.roa.query_parser_exceptions.QueryParserOperationInvalidError:
            Whenever the current operation attributes are invalid.'''

    def get_filter(self, model):
        '''This method validates the current operation and build the filter.'''

        self.validate(model)

        return self.build_filter(model)

class QueryParserOperationSort(QueryParserOperation, metaclass=ABCMeta):
    '''This class provides base support for sort operations: asc / desc.'''

    def __init__(self, operation, argument, parser, sort_dir=None):
        super(QueryParserOperationSort, self).__init__(operation, argument, parser)

        self._sort_dir = sort_dir

    def validate(self, model):
        '''This method validates sorting argument passed to this operation.'''

        self._argument = self._argument.strip()

        try:
            self._argument = getattr(model, self._argument)
        except AttributeError:
            raise QueryParserOperationInvalidError("Resource attribute %s does not exist." % self._argument)

    def build_filter(self, model):
        '''This method builds the sorting model.'''

        return ModelSort(self._argument, self._sort_dir)

class QueryParserOperationSortAsc(QueryParserOperationSort):
    '''This class provides asc sort operation.'''

    def __init__(self, operation, argument, parser):
        super(QueryParserOperationSortAsc, self).__init__(operation, argument, parser, sort_dir=ModelSort.ASC)

class QueryParserOperationSortDesc(QueryParserOperationSort):
    '''This class provides desc sort operation.'''

    def __init__(self, operation, argument, parser):
        super(QueryParserOperationSortDesc, self).__init__(operation, argument, parser, sort_dir=ModelSort.DESC)


class QueryParserOperationBinary(QueryParserOperation):
    '''This class provides the validation / build logic for binary operations.'''

    def __init__(self, operation, argument, parser):
        super(QueryParserOperationBinary, self).__init__(operation, argument, parser)

        self._column = None
        self._value = None

    def build_filter(self, model):
        '''This method builds an equality filter.'''

        self._value = json.loads(self._value)

        return ModelFilter(column=self._column, ref_value=self._value, operation=self._operation)

    def validate(self, model):
        '''This method ensures that three arguments were passed.'''

        first_comma = self._argument.find(",")

        if first_comma == -1:
            raise QueryParserOperationInvalidError("Binary operation %s requires two arguments." % self._operation)

        arguments = [self._argument[:first_comma], self._argument[first_comma + 1:]]

        if not arguments[0].strip():
            raise QueryParserOperationInvalidError("Binary operation %s first argument is empty." % self._operation)

        if not arguments[1].strip():
            raise QueryParserOperationInvalidError("Binary operation %s second argument is empty." % self._operation)

        column_name = arguments[0].strip()

        try:
            self._column = getattr(model, column_name)
        except AttributeError:
            raise QueryParserOperationInvalidError("Resource model does not contain %s attribute." % column_name)

        self._value = arguments[1].strip()

class QueryParserOperationCompound(QueryParserOperation, metaclass=ABCMeta):
    '''This class provides the parser for compound filter or. It will recursively parse each argument and in the end will return
    a compatible :py:class:`fantastico.mvc.model_filter_compound.ModelFilterCompound`. Each concrete class must specify the
    compound filter type to use.'''

    def __init__(self, operation, argument, parser, compound_filter_cls=None):
        super(QueryParserOperationCompound, self).__init__(operation, argument, parser)

        self._compound_filter_cls = compound_filter_cls

    def build_filter(self, model):
        '''This method builds the compound filter based on the parsed arguments of this operation.'''

        return self._compound_filter_cls(*self._argument)

    def validate(self, model):
        '''This method validates all arguments passed to this compound filter.'''

        filters = []

        filters_or = re.findall(r"or\(.*?\)\)", self._argument)

        for filter_expr in filters_or:
            self._argument = self._argument.replace(filter_expr, "", 1)

        filters_and = re.findall(r"and\(.*?\)\)", self._argument)

        for filter_expr in filters_and:
            self._argument = self._argument.replace(filter_expr, "", 1)

        filters.extend(filters_or)
        filters.extend(filters_and)

        filters_binary = re.findall(r"[a-z]{1,}\(.*?\)", self._argument)

        filters.extend(filters_binary)

        if len(filters) < 2:
            raise QueryParserOperationInvalidError("%s operation takes at least two arguments." % self._operation)

        self._argument = [self._parser.parse_filter(filter_expr, model) for filter_expr in filters]

class QueryParserOperationOr(QueryParserOperationCompound):
    '''This class provides a query parser for **or** compound filtering.'''

    def __init__(self, operation, argument, parser):
        super(QueryParserOperationOr, self).__init__(operation, argument, parser, compound_filter_cls=ModelFilterOr)

class QueryParserOperationAnd(QueryParserOperationCompound):
    '''This class provides a query parser for **and** compound filtering.'''

    def __init__(self, operation, argument, parser):
        super(QueryParserOperationAnd, self).__init__(operation, argument, parser, compound_filter_cls=ModelFilterAnd)
