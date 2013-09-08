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
.. py:module:: fantastico.contrib.tracking_codes.tracking_controller
'''

import json
from webob.response import Response

from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import ControllerProvider, Controller

@ControllerProvider()
class TrackingController(BaseController):
    '''.. image:: /images/components/tracking_codes/erd.png

    This class provides the tracking operations supported by **TrackingCodes** component.
    '''

    MAX_RECORDS = 50

    @Controller(url="^/tracking-codes/codes(/)?$",
                models={"TrackingCode": "fantastico.contrib.tracking_codes.models.codes.TrackingCode"})
    def list_codes(self, request):
        '''This method provides tracking codes listing logic. It list all available tracking codes from database.

        :param request: The current http request being processed. Read :doc:`/features/request_response` for more information.
        :type request: :py:class:`webob.request.Request`
        :returns: JSON list of available tracking codes. Can be empty if no tracking codes are defined.
        '''

        codes_facade = request.models.TrackingCode

        codes = codes_facade.get_records_paged(start_record=0, end_record=TrackingController.MAX_RECORDS)
        codes = [{"id": code.id,
                  "provider": code.provider,
                  "script": code.script} for code in codes]

        response = Response(json.dumps(codes), content_type="application/json")

        return response

    @Controller(url="^/tracking-codes/ui/codes(/)?$") #pylint: disable=W0613
    def list_codes_ui(self, request):
        '''This method renders all available tracking codes.'''

        return Response(self.load_template("/list_tracking_codes.html"))
