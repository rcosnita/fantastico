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

from fantastico.roa.query_parser_exceptions import QueryParserOperationInvalidError
from fantastico.roa.query_parser_operations import QueryParserOperationBinaryEq, QueryParserOperationBinaryGe, \
    QueryParserOperationBinaryGt, QueryParserOperationBinaryLe, QueryParserOperationBinaryLt, QueryParserOperationBinaryLike, \
    QueryParserOperationBinaryIn, QueryParserOperationSortAsc, QueryParserOperationSortDesc, QueryParserOperationOr, \
    QueryParserOperationAnd, QueryParserOperationCompound
import re

class QueryParser(object):
    '''This class provides ROA query parser functionality. It provides methods for transforming filter and sorting expressions
    (:doc:`/features/roa/rest_standard`) into mvc filters (:doc:`/features/mvc`).'''

    _lang_symbols = {"(": "(",
                    ")": ")",
                    ",": ","}

    _MAX_TOKEN_LENGTH = 4
    _lang_rules = {}

    _T_END = "$"

    TERM = 0
    RULE = 1
    regex_text = "[a-zA-Z\\. \"0-9\\[\\]]{1,}"

    def __init__(self):
        self._stack = [(self.TERM, self._T_END)]
        self._model = None

        self._lang_rules = {
                self.regex_text: {
                                ",": [(self.RULE, self.regex_text), (self.TERM, ")")],
                                self.regex_text: [(self.TERM, self.regex_text)]
                              },
                ",": {
                        ",": [(self.TERM, ",")]
                      },
                ")": {
                        ")": [(self.TERM, ")")]
                      },
                "(": {}
             }

        self._lang_grammar = {self.regex_text: {
                                            self.regex_text: (self.regex_text, self.regex_text, self._add_argument)
                                        },
                       ",": {
                                ",": (",", ",", self._nop)
                             },
                       ")": {
                                 ")": (")", ")", self._exec_operator)
                             },
                       "(": {}
                     }

        self._last_operator = []
        self._discovered_tokens = []
        self._compound_arguments = []

        self._register_all_operations()

    def _register_all_operations(self):
        '''This method register all supported operations of this parser.'''

        self._register_operation(QueryParserOperationBinaryEq(self))
        self._register_operation(QueryParserOperationBinaryGt(self))
        self._register_operation(QueryParserOperationBinaryGe(self))
        self._register_operation(QueryParserOperationBinaryLt(self))
        self._register_operation(QueryParserOperationBinaryLe(self))
        self._register_operation(QueryParserOperationBinaryLike(self))
        self._register_operation(QueryParserOperationBinaryIn(self))

        self._register_operation(QueryParserOperationOr(self))
        self._register_operation(QueryParserOperationAnd(self))

        self._register_operation(QueryParserOperationSortAsc(self))
        self._register_operation(QueryParserOperationSortDesc(self))

    def _register_operation(self, operator):
        '''This method registers a given operations into the list of supported operations. Grammar rules are enriched based
        on the given operator.'''

        token = operator.get_token()

        self._lang_grammar[token] = operator.get_grammar_table(self._new_operator)
        self._lang_grammar["("][token] = ("(", token, self._nop)
        self._lang_symbols[operator.get_token()] = token
        self._lang_rules[token] = operator.get_grammar_rules()
        self._lang_rules["("][token] = [(self.RULE, token)]

    def _nop(self):
        '''This method is used as default values when a table grammar entry does not require any concrete action.'''

        pass

    def _exec_operator(self):
        '''This method executes the current operator against the given the model.

        :rtype: :py:class`fantastico.mvc.models.model_filter.ModelFilterAbstract`'''

        curr_operation = self._last_operator.pop()

        if isinstance(curr_operation, QueryParserOperationCompound):
            if len(self._compound_arguments) != 2:
                raise QueryParserOperationInvalidError("Operation %s accepts 2 parameters. %s given." % \
                                                       (curr_operation.get_token(), len(self._compound_arguments)))

            curr_operation.add_argument(self._compound_arguments.pop())
            curr_operation.add_argument(self._compound_arguments.pop())

            self._compound_arguments.insert(0, curr_operation.get_filter(self._model))
        else:
            self._compound_arguments.insert(0, curr_operation.get_filter(self._model))

        return self._compound_arguments[-1]

    def _add_argument(self):
        '''This method adds a new argument to the current operation.'''

        self._last_operator[-1].add_argument(self._discovered_tokens.pop().strip())

    def _new_operator(self, operator_cls):
        '''This method adds a new operator on the stack of operations.'''

        self._last_operator.append(operator_cls(self))

    def _parse_lexic(self, filter_expr):
        '''This method identify the lexic of the given filter expression. As a result a set of supported symbols are returned.'''

        tokens = []

        curr_token = []
        idx = 0

        while idx < len(filter_expr):
            char = filter_expr[idx]

            if char == ' ' and "\"" not in curr_token:
                idx += 1
                continue

            token = None

            if "[" not in curr_token and "\"" not in curr_token:
                token = self._lang_symbols.get(char)

            if not token:
                curr_token.append(char)

                token = self._lang_symbols.get("".join(curr_token))

                if token:
                    curr_token = []
                    tokens.append(token)
            else:
                if curr_token:
                    tokens.append("".join(curr_token))
                    curr_token = []

                tokens.append(token)

            if len(curr_token) > self._MAX_TOKEN_LENGTH:
                next_delim = None

                if "[" not in curr_token:
                    next_delim = filter_expr.find(",", idx)

                    if next_delim > -1 and filter_expr[next_delim - 1] == ")":
                        next_delim = next_delim - 1

                    if next_delim == -1:
                        next_delim = filter_expr.find(")", idx)

                    if filter_expr[next_delim - 1] == ")":
                        next_delim -= 1
                else:
                    next_delim = filter_expr.find("]", idx) + 1

                curr_token.extend(filter_expr[idx + 1:next_delim])
                token = "".join(curr_token)
                tokens.append(token)

                curr_token = []

                idx = next_delim

                continue

            idx += 1

        tokens.append(self._T_END)

        return tokens

    def _parse_syntax(self, tokens):
        '''This method does a syntax parsing on the given tokens. Tokens simply describe the sentence being analysed. In order
        to obtain tokens a lexic analysis must be executed.

        :param tokens: A list of tokens describing the sentence being analysed.
        :type tokens: list
        :returns: Left most derivation of the sentence.
        :rtype: list
        '''

        position = 0

        ll_derivation = []

        while len(self._stack) > 0:
            s_type, s_token = self._stack.pop()
            token = tokens[position]

            if s_type == self.TERM:
                position = self._handle_term_token(s_token, token, position)
                continue

            self._handle_rule_token(tokens, ll_derivation, s_token, token, position)

        return ll_derivation

    def _handle_term_token(self, s_token, token, curr_pos):
        '''This method handles the given tuple of s_token and token when the given s_token is terminal.'''

        if token == s_token:
            curr_pos += 1

            return curr_pos

        if len(self._discovered_tokens) == 0:
            raise QueryParserOperationInvalidError("Invalid operation in expression.")

        raise QueryParserOperationInvalidError("Operator %s received bad input token %s" % \
                                               (self._discovered_tokens[-1], token))

    def _handle_rule_token(self, all_tokens, ll_derivation, s_token, token, curr_pos):
        '''This method handles the given tuple of s_token and token when the given s_token is a grammar rule.'''

        if not self._lang_symbols.get(token) and s_token == self.regex_text and re.match(s_token, token):
            self._discovered_tokens.insert(0, token)

            token = self.regex_text
            all_tokens[curr_pos] = self.regex_text

        if self._lang_symbols.get(token) and s_token == self.regex_text:
            s_token = "("

        rule = self._lang_grammar[s_token].get(token)

        if not rule:
            return

        ll_derivation.append(rule)

        for curr_rule in reversed(self._lang_rules[rule[0]][rule[1]]):
            self._stack.append(curr_rule)

    def parse_filter(self, filter_expr, model):
        '''This method transform the given filter expression into mvc filters.

        :param filter_expr: The filter string expression we want to convert to query objects.
        :type filter_exprt: string
        :param model: The model used to describe the resource on which the requests are done.
        :returns: The newly created mvc query object.
        :rtype: :py:class:`fantastico.mvc.models.model_filter.ModelFilterAbstract`'''

        if not filter_expr or len(filter_expr.strip()) == 0:
            return

        self._model = model
        tokens = self._parse_lexic(filter_expr)

        self._stack.append((self.RULE, tokens[0]))
        ll_derivation = self._parse_syntax(tokens[1:])

        model_filter = None

        for ll_rule in ll_derivation:
            model_filter = ll_rule[2]()

        return model_filter

    def parse_sort(self, sort_expr, model):
        '''This method transform the given sort expression into mvc sort filter.

        :param filter_expr: The filter string expression we want to convert to query objects.
        :type filter_exprt: string
        :param model: The model used to describe the resource on which the requests are done.
        :returns: The newly created mvc query object.
        :rtype: :py:class:`fantastico.mvc.models.model_sort.ModelSort`
        '''

        results = []

        for expr in sort_expr:
            results.append(self.parse_filter(expr, model))

        return results
