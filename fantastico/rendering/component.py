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

.. py:module:: fantastico.rendering.component
'''
from fantastico.exceptions import FantasticoInsufficientArgumentsError, FantasticoTemplateNotFoundError
from fantastico.rendering.url_invoker import FantasticoUrlInternalInvoker
from jinja2 import nodes
from jinja2.exceptions import TemplateSyntaxError, TemplateNotFound
from jinja2.ext import Extension
from jinja2.nodes import Const
from webob.request import Request
import json
from fantastico.utils import instantiator

class Component(Extension):
    '''In fantastico, components are defined as a collection of classes and scripts grouped together as described in
    :doc:`/features/component_model`. Each fantastico component provides one or more public routes that can be accessed from
    a browser or from other components. This class provides the mechanism for internal component referencing.

    In order to gain a better understanding about internal / in process component referencing we assume **Blog** component
    provides the following public routes:

        * **/blog/articles/<article_id>** - Retrieves information about an article.
        * **/blog/ui/articles/<article_id>** - Displays an article within a html container.

    The first url is a simple json endpoint while the second url is a simple html dynamic page. When we want to reuse a
    datasource or an dynamic html page in fantastico is extremely easy to achieve. Lets first see possible responses from the
    above mentioned endpoints:

    .. code-block:: javascript

        /* /blog/articles/<article_id> response */
        {"id": 1,
         "title": "Simple blog article",
         "content": "This is a simple and easy to read blog article."}

    .. code-block:: html

        <!-- /blog/ui/articles/<article_id> response-->

        <div class="blog-article">
            <p class="title">Simple blog article</p>

            <p class="content">This is a simple and easy to read blog article.</p>
        </div>

    A very common scenario is to create multiple views for a given endpoint.

    .. code-block:: html

        <!-- web service server side reusage -->
        {% component url="/blog/articles/1", template="/show_blog_formatted.html", runtime="server" %}{% endcomponent %}

    .. code-block:: html

        <!-- show_blog_formatted.html -->
        <p class="blog-title">{{model.title}}</p>
        <p class="blog-content">{{model.content}}</p>

    As you can see, json response is plugged into a given template name. It is mandatory that the given template exists on the
    component root path.

    Also a very common scenario is to include an endpoint that renders partial html into a page:

    .. code-block:: html

        <!-- html server side reusage -->
        {% component url="/blog/ui/articles/1",runtime="server" %}{% endcomponent %}

    Runtime attribute is used for telling Fantastico if the rendering needs to take place on server side or on client. Currently,
    only server side rendering is supported which actually means a page will be completed rendered on server and then the markup
    is sent to the browser.

    In order to reduce required attributes for component tag, runtime attribute is optional with server as default value.
    '''

    COMP_ARG_TEMPLATE = "template"
    COMP_TEMPLATE_DEFAULT = "/raw_dump.html"

    COMP_ARG_URL = "url"
    COMP_ARG_RUNTIME = "runtime"
    COMP_RUNTIME_DEFAULT = "server"

    tags = set(["component"])

    def __init__(self, environment, url_invoker_cls=FantasticoUrlInternalInvoker):
        super(Component, self).__init__(environment)

        self._url_invoker_cls = url_invoker_cls
        self._comp_search_path = instantiator.get_class_abslocation(Component)

    def parse(self, parser):
        '''This method is used to parse the component extension from template, identify named parameters and render it.

        :param parser: The Jinja 2 expression parser.
        :type parser: Jinja 2 parser.
        :returns: A callblock able to render the component.
        :raises FantasticoInsufficientArgumentsError: when no / not enough arguments are provided to component.
        '''

        lineno = parser.stream.current.lineno

        parameters = []

        parser.parse_expression()

        while True:
            parser.stream.skip_if("comma")
            parser.stream.skip_if("assign")

            try:
                expression = parser.parse_expression()
            except TemplateSyntaxError:
                # occurs when some parameters are missing.
                break

            if expression:
                parameters.append(expression)

            if len(parameters) == 6:
                break

        named_params, missing_params = self._get_named_params(parameters)

        self._validate_missing_parameters(missing_params)

        method = self.call_method("render", kwargs=named_params, lineno=lineno)

        body = parser.parse_statements(['name:endcomponent'], drop_needle=True)

        return nodes.CallBlock(method,
                               [],
                               [],
                               body).set_lineno(lineno)

    def render(self, template=COMP_TEMPLATE_DEFAULT, url=None, runtime="server", caller=lambda: ""):
        '''This method is used to render the specified url using the given parameters.

        :param template: The template we want to render into the result of the url.
        :type template: string
        :param url: The url we want to invoke.
        :type url: string
        :param runtime: The runtime we execute the rendering into. Only **server** is supported for now.
        :type runtime: string
        :param caller: The caller macro that can retrieve the body of the tag when invoked.
        :type caller: macro
        :returns: The rendered component result.
        :raises fantastico.exceptions.FantasticoTemplateNotFoundError: Whenever we try to render a template which does not exist.
        :raises fantastico.exceptions.FantasticoUrlInvokerError: Whenever an exception occurs invoking a url within the container.
        '''

        # [rcosnita] do something with the inner body of the tag. Coming in a future version.
        caller()

        if runtime != "server":
            return

        remove_comp_filepath = False

        if template == Component.COMP_TEMPLATE_DEFAULT:
            self.environment.loader.searchpath.append("%s/views" % self._comp_search_path)

            remove_comp_filepath = True

        curr_request = self.environment.fantastico_request
        request = Request.blank(url)

        request.headers = curr_request.headers
        request.cookies = curr_request.cookies

        url_invoker = self._url_invoker_cls(curr_request.context.wsgi_app, request.environ)
        response = url_invoker.invoke_url(url, request.headers)[0]

        try:
            json_response = None

            try:
                json_response = json.loads(response.decode())
            except ValueError as ex:
                json_response = response.decode()

            return self.environment.get_template(template).render({"model": json_response})
        except TemplateNotFound as ex:
            raise FantasticoTemplateNotFoundError("Template %s does not exist." % template, ex)
        finally:
            if remove_comp_filepath:
                self.environment.loader.searchpath.pop()

    def _get_named_params(self, expressions):
        '''This method transform a list of expressions into a dictionary. It is mandatory that the given list has even number
        of expressions otherwise an exception is raised.

        :param expressions: A list of jinja2 expressions.
        :type expressions: list
        :returns: A tuple (list of kwargs nodes, dict of missing_arguments).'''

        named_params = []
        missing_params = {Component.COMP_ARG_TEMPLATE: True,
                          Component.COMP_ARG_URL: True,
                          Component.COMP_ARG_RUNTIME: True}

        last_lineno = -1
        expr_iterator = iter(expressions)

        for expr_name in expr_iterator:
            expr_value = next(expr_iterator)

            missing_params[expr_name.name] = False

            last_lineno = expr_value.lineno
            named_params.append(nodes.Keyword(expr_name.name, expr_value, lineno=last_lineno))

        if missing_params[Component.COMP_ARG_TEMPLATE]:
            named_params.insert(0, nodes.Keyword(Component.COMP_ARG_TEMPLATE,
                                                 Const(Component.COMP_TEMPLATE_DEFAULT), lineno=last_lineno))

        if missing_params[Component.COMP_ARG_RUNTIME]:
            named_params.append(nodes.Keyword(Component.COMP_ARG_RUNTIME, Const(Component.COMP_RUNTIME_DEFAULT),
                                              lineno=last_lineno))

        return named_params, missing_params

    def _validate_missing_parameters(self, missing_parameters):
        '''This method validates the dictionary containing all parameters of component marked with False if they are found and
        True if they miss.'''

        if missing_parameters["url"]:
            raise FantasticoInsufficientArgumentsError("Mandatory url parameter missing.")
