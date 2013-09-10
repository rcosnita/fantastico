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
.. py:module:: fantastico.contrib.dynamic_pages.tests.test_pages_router
'''
from fantastico.contrib.dynamic_pages.models.pages import DynamicPage, DynamicPageModel
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class PagesRouterTests(FantasticoUnitTestsCase):
    '''This class provides the test cases required to ensure dynamic pages are served correctly.'''

    def init(self):
        '''This method is invoked automatically in order to set common dependencies.'''

        from fantastico.contrib.dynamic_pages.pages_router import PagesRouter

        self.check_original_methods(PagesRouter)

    def _mock_page_get_records_paged(self, expected_url, expected_items):
        '''This method mocks get_records_paged from DynamicPage model facade.'''

        def get_records_paged(start_record, end_record, model_filter):
            self.assertEqual(start_record, 0)
            self.assertEqual(end_record, 1)
            self.assertEqual(model_filter.column, DynamicPage.url)
            self.assertEqual(model_filter.ref_value, expected_url)
            self.assertEqual(model_filter.operation, ModelFilter.EQ)

            return expected_items

        return get_records_paged

    def _mock_pagemodel_get_records_paged(self, page_model):
        '''This method returns a mock for get_records_paged belonging to DynamicPageModel facade.'''
        from fantastico.contrib.dynamic_pages.pages_router import PagesRouter

        def get_records_paged(start_record, end_record, model_filter):
            self.assertEqual(0, start_record)
            self.assertEqual(PagesRouter.MAX_PAGE_ATTRS, end_record)
            self.assertEqual(DynamicPageModel.page_id, model_filter.column)
            self.assertEqual(1, model_filter.ref_value)
            self.assertEqual(ModelFilter.EQ, model_filter.operation)

            return [page_model]

        return get_records_paged

    def _mock_load_template(self, page, page_model, expected_result):
        '''This method return a compatible load_template mock which can be injected into PagesRouter.'''

        def load_template(tpl_name, tpl_model):
            self.assertEqual(page.template, tpl_name)

            tpl_model = tpl_model.get("page")
            self.assertIsNotNone(tpl_model)
            self.assertEqual(page.title, tpl_model["title"])
            self.assertEqual(page.description, tpl_model["description"])
            self.assertEqual(page.keywords, tpl_model["keywords"])
            self.assertEqual(page.language, tpl_model["language"])

            if page_model:
                self.assertEqual({"value": page_model.value}, tpl_model[page_model.name])

            return expected_result

        return load_template

    def test_serve_dynamicpage_notfound(self):
        '''This test case covers the case when an inexistent dynamic page is requested.'''

        from fantastico.contrib.dynamic_pages.pages_router import PagesRouter

        expected_url = "/page/not/found"
        page_facade = Mock()
        request = Mock()

        page_facade.get_records_paged = self._mock_page_get_records_paged(expected_url, [])
        request.models = Mock()
        request.models.DynamicPage = page_facade

        router = PagesRouter(Mock())

        response = router.serve_dynamic_page(request, expected_url[1:], os_provider=Mock())

        self.assertEqual(404, response.status_code)
        self.assertEqual("text/html", response.content_type)

    def _test_serve_dynamicpage_scenario(self, page, page_model, expected_url, expected_result):
        '''This method provides a test scenario for serve dynamic page method.'''

        from fantastico.contrib.dynamic_pages.pages_router import PagesRouter

        page_facade = Mock()
        page_attr_facade = Mock()

        request = Mock()

        page_facade.get_records_paged = self._mock_page_get_records_paged(expected_url, [page])
        request.models = Mock()
        request.models.DynamicPage = page_facade
        request.models.DynamicPageModel = page_attr_facade

        page_attr_facade.get_records_paged = self._mock_pagemodel_get_records_paged(page_model)

        router = PagesRouter(Mock())

        router.load_template = self._mock_load_template(page, page_model, expected_result)

        response = router.serve_dynamic_page(request, expected_url[1:], os_provider=Mock())

        self.assertEqual(200, response.status_code)
        self.assertEqual("text/html", response.content_type)
        self.assertEqual(expected_result, response.body.decode())


    def test_serve_dynamicpage_ok(self):
        '''This test case covers the case when dynamic page exists and have a model binded.'''

        expected_url = "/page/about"
        expected_result = "simple test rendered template"
        page = DynamicPage(template="/comp/template",
                           language="ro-RO",
                           keywords="keyword 1, keyword 2",
                           description="simple description",
                           title="simple title")
        page.id = 1

        page_model = DynamicPageModel(page_id=1, name="simple_attr", value="simple test")

        self._test_serve_dynamicpage_scenario(page, page_model, expected_url, expected_result)

    def test_serve_dynamicpage_nomodel_ok(self):
        '''This test case covers the case when dynamic page exists but does not have a model binded.'''

        expected_url = "/page/about"
        expected_result = "simple test rendered template"
        page = DynamicPage(template="/comp/template",
                           language="ro-RO",
                           keywords="keyword 1, keyword 2",
                           description="simple description",
                           title="simple title")
        page.id = 1

        self._test_serve_dynamicpage_scenario(page, None, expected_url, expected_result)
