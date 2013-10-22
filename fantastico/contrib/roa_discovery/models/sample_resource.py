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
.. py:module:: fantastico.contrib.roa_discovery.models.sample_resource
'''
from fantastico.mvc import BASEMODEL
from fantastico.roa.resource_decorator import Resource
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, Float

@Resource(name="Sample Resource", url="/sample-resources")
class SampleResource(BASEMODEL):
    '''This is a very simple non intrusive resource used to showcase discoverability and ROA api generator.'''

    __tablename__ = "sample_resources"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(100), nullable=False)
    description = Column("description", Text)
    total = Column("total", Float, nullable=False)
    vat = Column("vat", Float, nullable=False)

    def __init__(self, name=None, description=None, total=None, vat=None):
        self.name = name
        self.description = description
        self.total = total
        self.vat = vat