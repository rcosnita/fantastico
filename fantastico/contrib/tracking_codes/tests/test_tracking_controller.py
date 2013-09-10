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
.. py:module:: fantastico.contrib.tracking_codes.tracking_controller.test_tracking_controller
'''

from fantastico.contrib.tracking_codes.models.codes import TrackingCode
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from webob.response import Response
import json

class TrackingControllerTest(FantasticoUnitTestsCase):
    '''This class provides the test cases for checking correct behavior of tracking controller.'''

    def init(self):
        '''This method is invoked automatically in order to set common dependencies.'''

        from fantastico.contrib.tracking_codes.tracking_controller import TrackingController

        self.check_original_methods(TrackingController)

    def test_list_codes_ok(self):
        '''This test case ensures tracking codes are retrieved correctly.'''

        fake_codes = [TrackingCode("Google", "<script>test</script>"),
                      TrackingCode("Mint", "<script>test mint</script>")]
        fake_codes[0].id = 1
        fake_codes[1].id = 2

        expected_codes = [{"id": 1, "provider": "Google", "script": "<script>test</script>"},
                          {"id": 2, "provider": "Mint", "script": "<script>test mint</script>"}]

        self._test_list_codes_scenario_ok(fake_codes, expected_codes)

    def test_list_codes_undefined_ok(self):
        '''This test case ensures listing of tracking codes still work if no code is defined in database.'''

        fake_codes = []
        expected_codes = []

        self._test_list_codes_scenario_ok(fake_codes, expected_codes)

    def test_list_codes_ui_ok(self):
        '''This test case ensures tracking codes ui controller work as expected.'''

        from fantastico.contrib.tracking_codes.tracking_controller import TrackingController

        expected_tpl = "<script>test code</script>"

        settings_facade = Mock()
        request = Mock()

        controller = TrackingController(settings_facade)

        def load_template(tpl_name, model_data=None, get_template=None):
            '''This method mocks load_template method from controller.'''

            self.assertIsNone(model_data)
            self.assertIsNone(get_template)
            self.assertEqual("/list_tracking_codes.html", tpl_name)

            return expected_tpl

        controller.load_template = load_template

        response = controller.list_codes_ui(request)

        self.assertIsNotNone(controller)
        self.assertIsInstance(response, Response)

        self.assertEqual("text/html; charset=UTF-8", response.headers["Content-Type"])
        self.assertIsNotNone(response.body)
        self.assertEqual(expected_tpl, response.body.decode())

    def _test_list_codes_scenario_ok(self, fake_codes, expected_codes):
        '''This method provides a template for executing list codes success scenario.'''

        from fantastico.contrib.tracking_codes.tracking_controller import TrackingController

        request = Mock()
        model = Mock()
        settings_facade = Mock()

        def get_records_paged(start_record, end_record):
            self.assertEqual(0, start_record)
            self.assertEqual(TrackingController.MAX_RECORDS, end_record)

            return fake_codes

        model.get_records_paged = get_records_paged

        controller = TrackingController(settings_facade)

        request.models = Mock()
        request.models.TrackingCode = model

        codes_response = controller.list_codes(request)

        self.assertIsInstance(codes_response, Response)
        self.assertIsNotNone(codes_response.body)
        self.assertEqual("application/json; charset=UTF-8", codes_response.headers["Content-Type"])

        codes = json.loads(codes_response.body.decode())
        self.assertEqual(expected_codes, codes)
