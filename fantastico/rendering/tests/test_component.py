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
.. py:module:: fantastico.rendering.tests.test_component
'''
from fantastico.exceptions import FantasticoInsufficientArgumentsError, FantasticoTemplateNotFoundError, FantasticoUrlInvokerError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from jinja2.exceptions import TemplateSyntaxError, TemplateNotFound
from mock import Mock
from webob.request import Request
import json

class ComponentUnitTests(FantasticoUnitTestsCase):
    '''This class provides all test cases required to check correct behavior of component extension.'''

    old_nodes_block = None

    @classmethod
    def setup_once(cls):
        '''This method is used to mock some of Jinja2 dependencies in order to make the code testable.'''

        from jinja2 import nodes

        cls.old_nodes_block = nodes.CallBlock
        nodes.CallBlock = CallBlockMock

    @classmethod
    def cleanup_once(cls):
        '''This method is used to restore mocked jinja 2 dependencies.'''

    def init(self):
        '''This method is invoked automatically and sets the default values for internal attributes.'''

        self._parse_index = -1 # because first call is not important: tag name.

    def test_component_named_parameters_ok(self):
        '''This test case ensures all named parameters are correctly resolved and delegated to render method.

        .. code-block:: html

            <!-- Component tag covered by this test. -->
            {% component template="/show_blog_formatted.html",url="/blog/articles/1",runtime="server" %}Simple tag body{% endcomponent %}
        '''

        expected_template = "/show_blog_formatted.html"
        expected_url = "/blog/articles/1"
        expected_runtime = "server"
        expected_lineno = 1
        expected_body = "Simple tag body"

        self._test_scenario_component_parse(expected_template, expected_url, expected_runtime, expected_body,
                                            expected_template, expected_url, expected_runtime, expected_body,
                                            expected_lineno)

    def test_component_missing_runtime_ok(self):
        '''This test case ensures runtime parameter can be ommitted.

        .. code-block:: html

            <!-- Component tag covered by this test. -->
            {% component template="/show_blog_formatted.html",url="/blog/articles/1" %}Simple tag body{% endcomponent %}
        '''

        expected_template = "/show_blog_formatted.html"
        expected_url = "/blog/articles/1"
        expected_runtime = "server"
        expected_lineno = 1
        expected_body = "Simple tag body"

        self._test_scenario_component_parse(expected_template, expected_url, None, expected_body,
                                            expected_template, expected_url, expected_runtime, expected_body,
                                            expected_lineno)

    def test_component_no_template_argument(self):
        '''This test case ensures componet works as expected even if template is not given.

        .. code-block:: html

            <!-- component tag covered -->
            {% component url="/blog/ui/articles/1" %}{% endcomponent %}
        '''

        mock_template = ""

        expected_template = "/raw_dump.html"
        expected_url = "/blog/articles/1"
        expected_runtime = "server"
        expected_lineno = 1
        expected_body = "Simple tag body"

        self._test_scenario_component_parse(mock_template, expected_url, None, expected_body,
                                            expected_template, expected_url, expected_runtime, expected_body,
                                            expected_lineno)

    def test_component_no_arguments(self):
        '''This test case ensures a concrete exception is raised if no arguments are provided to component.

        .. code-block:: html

            <!-- component tags covered -->
            {% component %}{% endcomponent %}
            {% component template="xxxx" %}{% endcomponent %}
        '''

        with self.assertRaises(FantasticoInsufficientArgumentsError):
            self._test_scenario_component_parse(None, None, None, None,
                                                None, None, None, None,
                                                1)

    def _test_scenario_component_parse(self, mock_template, mock_url, mock_runtime, mock_body,
                                       expected_template, expected_url, expected_runtime, expected_body,
                                       expected_lineno):
        '''This method provides the skeleton required for component parse test cases.'''

        from fantastico.rendering.component import Component

        environment, parser = self._mock_parser_parse(mock_template, mock_url, mock_runtime,
                                                      expected_lineno, expected_body)

        component = Component(environment)

        block = component.parse(parser)
        template_kwarg = block.call_block.kwargs[0]
        url_kwarg = block.call_block.kwargs[1]
        runtime_kwarg = block.call_block.kwargs[2]

        self.assertEqual("template", template_kwarg.key)
        self.assertEqual(expected_template, template_kwarg.value.value)

        self.assertEqual("url", url_kwarg.key)
        self.assertEqual(expected_url, url_kwarg.value.value)

        self.assertEqual("runtime", runtime_kwarg.key)
        self.assertEqual(expected_runtime, runtime_kwarg.value.value)

        self.assertEqual(expected_lineno, block.call_block.lineno)

    def test_render_with_template(self):
        '''This test case ensures a template rendering is triggered with url response data when template argument is given.'''

        from fantastico.rendering.component import Component

        expected_url = "/simple/url"
        expected_template = "/test.html"
        expected_result = "works"
        expected_environment = {"HTTP_CUSTOM_HEADER": "Simple header",
                                "HTTP_CONTENT_TYPE": "application/json"}
        environment, url_invoker_cls = self._mock_render_dependencies(expected_template, expected_url, expected_environment,
                                                                      expected_result)

        component = Component(environment, url_invoker_cls)

        result = component.render(expected_template, expected_url)

        self.assertEqual(expected_result, result)
        self.assertEqual("application/json", expected_environment["HTTP_CONTENT_TYPE"])

    def test_render_without_template(self):
        '''This test case ensure component reusage without template work as expected by delegating rendering
        process to template /raw_dump.html.'''

        from fantastico.rendering.component import Component

        expected_url = "/simple/url"
        expected_template = "/raw_dump.html"
        expected_result = "works"
        expected_environment = {"HTTP_CUSTOM_HEADER": "Simple header",
                                "HTTP_CONTENT_TYPE": "application/json"}

        environment, url_invoker_cls = self._mock_render_dependencies(expected_template, expected_url, expected_environment,
                                                                      expected_result, json_output=False)

        component = Component(environment, url_invoker_cls)

        result = component.render(url=expected_url)

        self.assertEqual(expected_result, result)
        self.assertEqual("application/json", expected_environment["HTTP_CONTENT_TYPE"])

    def test_render_notfound_template(self):
        '''This test case covers the scenario where the requested template passed to component tag is not found.'''

        from fantastico.rendering.component import Component

        expected_url = "/simple/url"
        expected_template = "/template.html"
        expected_result = "works"
        expected_environment = {"HTTP_CUSTOM_HEADER": "Simple header",
                                "HTTP_CONTENT_TYPE": "application/json"}

        environment, url_invoker_cls = self._mock_render_dependencies(expected_template, expected_url, expected_environment,
                                                                      expected_result)

        environment.get_template = Mock(side_effect=TemplateNotFound("template does not exist."))

        component = Component(environment, url_invoker_cls)

        with self.assertRaises(FantasticoTemplateNotFoundError) as ctx:
            component.render(expected_template, expected_url)

        self.assertTrue(str(ctx.exception).find(expected_template) > -1)

    def test_render_urlinvoker_error(self):
        '''This test case ensures a concrete fantastico exception is thrown during rendering if an exception occurs
        within url invoker.'''

        from fantastico.rendering.component import Component

        expected_url = "/simple/url"
        expected_template = "/template.html"
        expected_result = "works"
        expected_environment = {"HTTP_CUSTOM_HEADER": "Simple header",
                                "HTTP_CONTENT_TYPE": "application/json"}

        url_invoker = Mock()
        url_invoker.invoke_url = Mock(side_effect=FantasticoUrlInvokerError("Unexpected invoker exception"))

        environment = self._mock_render_dependencies(expected_template, expected_url, expected_environment,
                                                                      expected_result)[0]

        url_invoker_cls = Mock(return_value=url_invoker)
        component = Component(environment, url_invoker_cls)

        with self.assertRaises(FantasticoUrlInvokerError) as ctx:
            component.render(expected_template, expected_url)

        self.assertTrue(str(ctx.exception).find("Unexpected invoker exception") > -1)

    def _mock_parser_parse(self, mock_template, mock_url, mock_runtime, mock_lineno, mock_body):
        '''This method is used for mocking the parser object so that it returns the given values. Useful for generating
        multiple test scenarios for parse.

        :returns: A tuple of (environment, parser)'''

        from jinja2 import nodes

        environment = Mock()
        environment.volatile = None

        def fake_parse_expression():
            '''This method mocks parse expression and returns expected named parameters.'''

            syntax_ex = TemplateSyntaxError("unexpected end of tag", lineno=mock_lineno)

            self._parse_index += 1

            if self._parse_index == 1:
                if mock_template is None:
                    raise syntax_ex

                if not mock_template:
                    return

                return nodes.Name(*["template", environment])

            if self._parse_index == 2:
                if mock_template is None:
                    raise syntax_ex

                if not mock_template:
                    return

                return nodes.Const(mock_template)

            if self._parse_index == 3:
                if not mock_url:
                    raise syntax_ex

                return nodes.Name(*["url", environment])

            if self._parse_index == 4:
                return nodes.Const(mock_url)

            if self._parse_index == 5:
                if not mock_runtime:
                    raise syntax_ex

                return nodes.Name(*["runtime", environment])

            if self._parse_index == 6:
                return nodes.Const(mock_runtime)

        parser = Mock()
        parser.stream = parser
        parser.current = parser
        parser.lineno = mock_lineno
        parser.parse_expression = fake_parse_expression
        parser.parse_statements = Mock(return_value=mock_body)

        return (environment, parser)

    def _mock_render_dependencies(self, expected_template, expected_url, expected_environment, expected_output,
                                  json_output=True):
        '''This method mocks all rendering dependencies and retrieves desired values.'''

        url_invoker = Mock()

        def invoke_url(url, headers):
            self.assertEqual(expected_url, url)
            self.assertEqual("Simple header", headers["Custom-Header"])

            if json_output:
                return [json.dumps({"message": expected_output}).encode()]

            return [expected_output.encode()]

        url_invoker.invoke_url = invoke_url

        url_invoker_cls = Mock(return_value=url_invoker)

        environment = Mock()
        environment.fantastico_request = Mock(return_value=environment)
        environment.fantastico_request.environ = environment
        environment.fantastico_request.headers = Request(expected_environment).headers
        environment.fantastico_request.cookies = {}

        def get_template(template):
            self.assertEqual(expected_template, template)

            return environment

        environment.get_template = get_template

        def render(model):
            if json_output:
                self.assertEqual(model, {"model": {"message": expected_output}})
            else:
                self.assertEqual(model, {"model": expected_output})

            return expected_output

        environment.render = render

        return (environment, url_invoker_cls)

class CallBlockMock(object):
    '''This class provides a mock object which actually replaces nodes.CallBlock jinja implementation.'''

    def __init__(self, call_block, arguments, defaults, body):
        '''This constructor simply accept all ordered and named arguments given.'''

        self.lineno = None
        self.call_block = call_block
        self.arguments = arguments
        self.defaults = defaults
        self.body = body

    def set_lineno(self, lineno):
        '''This method stores the line number.'''

        self.lineno = lineno

        return self
