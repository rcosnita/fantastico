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
.. py:module:: fantastico.contrib.tracking_codes.models.codes
'''
from fantastico.mvc import BASEMODEL
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text

class TrackingCode(BASEMODEL):
    '''This class provides the model for tracking codes. It maps **tracking_codes** table to an object. In order to use this model
    please read :doc:`/features/mvc`.'''

    __tablename__ = "tracking_codes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    provider = Column("provider", String(50), unique=True, nullable=False)
    script = Column("script", Text, nullable=False)

    def __init__(self, provider, script):
        self.provider = provider
        self.script = script
