import allure
import pytest
import json
from Backend.api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("IOStream")
class TestSystemAPI:

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

    @pytest.mark.parametrize("first_uri_resource, devid, second_uri_resource, ip", [("id", "27", "ip", "10.1.1.11")])
    @allure.title("API: IOStream")
    def test_status(self, first_uri_resource, devid, second_uri_resource, ip):
        api_operation = ApiOperation("iostreams")
        failure_flags = {"gett_failed": False}

        # GET
        with allure.step("GET IOStream"):
            try:
                response_get = api_operation.get_api_operation(None, first_uri_resource, devid, second_uri_resource, ip)
                self.attach_response_result(
                    response_get,
                    "GET Response Status Code",
                    "GET Response Result",
                )
            except AssertionError:
                failure_flags["get_failed"] = True

        # Check failure flags and fail the test if any step failed
        for step, failed in failure_flags.items():
            if failed:
                pytest.fail(f"{step.replace('_', ' ').capitalize()}")
