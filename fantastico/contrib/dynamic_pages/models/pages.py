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
.. py:module:: fantastico.contrib.dynamic_pages.models.pages
'''
from fantastico.mvc import BASEMODEL
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text

class DynamicPage(BASEMODEL):
    '''This model holds meta information about dynamic pages. Below you can find all meta information for a dynamic page:

        #. id (unique identifier for a dynamic page)
        #. name
        #. url
        #. template
        #. keywords
        #. description
        #. language

    In a template used for rendering dynamic pages, you can easily access page meta information:

    .. code-block:: html

        <p>Id: {{page.id}}</p>
        <p>Name: {{page.name}}</p>
        <p>Url: {{page.url}}</p>
        <p>Template: {{page.template}}</p>
        <p>Keywords: {{page.keywords}}</p>
        <p>Description: {{page.description}}</p>
        <p>Language: {{page.language}}</p>

    Usually it does not make sense to display dynamic page unique identifier but you can do it if necessary.
    '''

    __tablename__ = "pages"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(100))
    url = Column("url", String(100))
    template = Column("template", String(100))
    keywords = Column("keywords", String(200))
    description = Column("description", String(300))
    title = Column("title", String(100))
    language = Column("language", String(5), default="en")

    def __init__(self, name=None, url=None, template=None, keywords=None, description=None,
                 title=None, language="en"):
        self.name = name
        self.url = url
        self.template = template
        self.keywords = keywords
        self.description = description
        self.title = title
        self.language = language

class DynamicPageModel(BASEMODEL):
    '''This class defines how page models looks like. A page model defines the actual content for en existing page.'''

    __tablename__ = "page_models"

    entry_id = Column("entry_id", Integer, primary_key=True, autoincrement=True)
    page_id = Column("page_id", Integer)
    name = Column("name", String(100))
    value = Column("value", Text)

    def __init__(self, page_id=None, name=None, value=None):
        self.page_id = page_id
        self.name = name
        self.value = value
