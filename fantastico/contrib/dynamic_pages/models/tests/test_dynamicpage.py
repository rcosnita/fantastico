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
.. py:module:: fantastico.contrib.dynamic_pages.models.test_dynamicpage
'''
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.contrib.dynamic_pages.models.pages import DynamicPage

class DynamicPageTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for DynamicPage model class.'''

    def test_dynamicpage_init_ok_defaults(self):
        '''This test case ensures all page meta information are initialized correctly with default values.'''

        model = DynamicPage()

        self.assertIsNone(model.id)
        self.assertIsNone(model.name)
        self.assertIsNone(model.url)
        self.assertIsNone(model.template)
        self.assertIsNone(model.keywords)
        self.assertIsNone(model.description)
        self.assertIsNone(model.title)
        self.assertEqual("en", model.language)

    def test_dynamicpage_init_ok(self):
        '''This test case ensures all page meta information are initialized correctly with given values.'''

        name = "/en/home"
        url = "/en/home"
        template = "/frontend/views/master.html"
        keywords = "keyword 1, ..."
        description = "description"
        title = "Home page"
        language = "en-US"

        model = DynamicPage(name, url, template, keywords, description, title, language)

        self.assertIsNone(model.id)
        self.assertEqual(name, model.name)
        self.assertEqual(url, model.url)
        self.assertEqual(template, model.template)
        self.assertEqual(keywords, model.keywords)
        self.assertEqual(description, model.description)
        self.assertEqual(title, model.title)
        self.assertEqual(language, model.language)
