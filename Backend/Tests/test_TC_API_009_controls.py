import allure
import pytest
import json
import time

from Backend.api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Control")
class TestControlAPI:

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

    @pytest.mark.parametrize("devid_value, uri_resource, chidx_value", [("27", "chidx", "0")])
    @allure.title("API: Control")
    def test_controls(self, devid_value, uri_resource, chidx_value):
        api_operation = ApiOperation("controls")
        failure_flags = {"get_failed": False, "put_failed": False}

        # GET
        with allure.step("GET Control"):
            try:
                response_get = api_operation.get_api_operation()
                self.attach_response_result(
                    response_get,
                    "GET Response Status Code",
                    "GET Response Result",
                )
            except AssertionError:
                failure_flags["get_failed"] = True

        # PUT
        with allure.step("PUT Control"):
            try:
                response_put = api_operation.put_api_operation(devid_value, uri_resource, chidx_value)
                for i, response in enumerate(response_put):
                    with allure.step(f"PUT Control {i+1}"):
                        self.attach_response_result(
                            response,
                            f"PUT Response Status Code {i+1}",
                            f"PUT Response Result {i+1}",
                        )
            except AssertionError:
                failure_flags["put_failed"] = True

        # Check failure flags and fail the test if any step failed
        for step, failed in failure_flags.items():
            if failed:
                pytest.fail(f"{step.replace('_', ' ').capitalize()}")
