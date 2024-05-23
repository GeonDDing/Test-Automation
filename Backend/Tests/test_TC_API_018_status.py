import allure
import pytest
import json
from Backend.api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Status")
class TestStatusAPI:

    def attach_response_result(self, response, status_name, result_name):
        status_code = response[0]
        status_message = "API Test Successful" if status_code == 200 else "API Test Failed"
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
        assert status_code == 200, "API Test Failed"

    @pytest.mark.parametrize("uri_resource, groupid_value", [("ip", "10.1.1.11")])
    @allure.title("API: Status")
    def test_status(self, uri_resource, groupid_value):
        api_operation = ApiOperation("status")
        generated_id = None

        # GET
        with allure.step("GET Status"):
            response_get = api_operation.get_api_operation(generated_id, uri_resource, groupid_value)
            self.attach_response_result(
                response_get,
                "GET Response Status Code",
                "GET Response Result",
            )
