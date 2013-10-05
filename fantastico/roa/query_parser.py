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
.. py:module:: fantastico.roa.query_parser
'''

from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.roa.query_parser_operations import QueryParserOperationBinary, QueryParserOperationOr
from fantastico.roa.roa_exceptions import FantasticoRoaError

class QueryParser(object):
    '''This class provides ROA query parser functionality. It provides methods for transforming filter and sorting expressions
    (:doc:`/features/roa/rest_standard`) into mvc filters (:doc:`/features/mvc`).'''

    REGISTERED_OPERATIONS = {ModelFilter.EQ: QueryParserOperationBinary,
                             ModelFilter.LIKE: QueryParserOperationBinary,
                             ModelFilter.GT: QueryParserOperationBinary,
                             ModelFilter.GE: QueryParserOperationBinary,
                             ModelFilter.LT: QueryParserOperationBinary,
                             ModelFilter.LE: QueryParserOperationBinary,
                             ModelFilter.IN: QueryParserOperationBinary,
                             "or": QueryParserOperationOr}

    def _get_operation_parser(self, operation, argument):
        '''This method obtains an instance of an operation parser (if possible).'''

        operation_parser = QueryParser.REGISTERED_OPERATIONS.get(operation)

        if not operation_parser:
            raise FantasticoRoaError("Operation %s is not supported." % operation)

        return operation_parser(operation, argument, self)

    def parse_filter(self, filter_expr, model):
        '''This method transform the given filter expression into mvc filters.

        :param filter_expr: The filter string expression we want to convert to query objects.
        :type filter_exprt: string
        :param model: The model used to describe the resource on which the requests are done.
        :returns: The newly created mvc query object.
        :rtype: :py:class:`fantastico.mvc.models.model_filter.ModelFilterAbstract`'''

        if not filter_expr or len(filter_expr.strip()) == 0:
            return

        operation_separator = filter_expr.find("(")
        operation = filter_expr[:operation_separator]
        argument = filter_expr[operation_separator + 1:-1]

        operation = self._get_operation_parser(operation.strip(), argument.strip())

        return operation.get_filter(model)
