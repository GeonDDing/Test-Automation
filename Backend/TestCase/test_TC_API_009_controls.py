import allure
import pytest
import json
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Control")
class TestControlAPI:
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

    @pytest.mark.parametrize("devid_value, uri_resource, chidx_value", [("2", "chidx", "0")])
    @allure.title("API: Contorl")
    def test_controls(self, devid_value, uri_resource, chidx_value):
        api_operation = ApiOperation("controls")

        # PUT
        response_put = api_operation.put_api_operation(devid_value, uri_resource, chidx_value)

        for i, response in enumerate(response_put):
            with allure.step(f"PUT Control"):
                self.attach_response_result(
                    response,
                    f"PUT Response Status Code {i+1}",
                    f"PUT Response Result {i+1}",
                )
