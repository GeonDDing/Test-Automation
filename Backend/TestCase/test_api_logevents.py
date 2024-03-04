import allure
import pytest
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Log Evnet")
class TestLogEventAPI:
    @staticmethod
    def attach_response_result(response, status_name, result_name):
        status_code = response[0]
        status_message = "테스트 성공" if status_code == 200 else "테스트 실패"
        allure.attach(
            f"Response Status Code: {status_code}, {status_message}",
            name=status_name,
            attachment_type=None,
        )
        allure.attach(
            json.dumps(response[1], indent=4),
            name=result_name,
            attachment_type=None,
        )
        assert status_code == 200, "테스트 실패"

    @pytest.mark.parametrize("uri_resource, severity_value", [("severity", "3")])
    @allure.title("API: Log Evnet")
    def test_logevents(self, uri_resource, severity_value):
        api_operation = ApiOperation("logevents")
        generated_id = None

        # GET
        with allure.step("GET Log Event"):
            response_get = api_operation.get_api_operation(
                generated_id, uri_resource, severity_value
            )
            self.attach_response_result(
                response_get,
                "GET Response Status Code",
                "GET Response Result",
            )
