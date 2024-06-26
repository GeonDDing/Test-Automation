import allure
import pytest
import json
from Backend.api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Output")
class TestOutputAPI:

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

    @allure.title("API: Output")
    def test_outputs(self):
        api_operation = ApiOperation("outputs")
        generated_id = None
        failure_flags = {
            "get_failed": False,
            "post_failed": False,
            "put_failed": False,
            "delete_failed": False,
        }

        # GET
        with allure.step("GET Output"):
            try:
                response_get = api_operation.get_api_operation()
                self.attach_response_result(
                    response_get,
                    "GET Response Status Code",
                    "GET Response Result",
                )
            except AssertionError:
                failure_flags["get_failed"] = True

        # POST
        with allure.step("POST Output"):
            try:
                response_post = api_operation.post_api_operation()
                for response in response_post:
                    self.attach_response_result(
                        response,
                        "POST Response Status Code",
                        "POST Response Result",
                    )
                    if generated_id is None and "id" in response[1]:
                        generated_id = response[1]["id"]
            except AssertionError:
                failure_flags["post_failed"] = True

        # PUT
        with allure.step("PUT Output"):
            try:
                response_put = api_operation.put_api_operation(generated_id)
                for response in response_put:
                    self.attach_response_result(
                        response,
                        "PUT Response Status Code",
                        "PUT Response Result",
                    )
            except AssertionError:
                failure_flags["put_failed"] = True

        # DELETE
        with allure.step("DELETE Output"):
            try:
                response_delete = api_operation.delete_api_operation(generated_id)
                self.attach_response_result(
                    response_delete,
                    "DELETE Response Status Code",
                    "DELETE Response Result",
                )
            except AssertionError:
                failure_flags["delete_failed"] = True

        # Check failure flags and fail the test if any step failed
        for step, failed in failure_flags.items():
            if failed:
                pytest.fail(f"{step.replace('_', ' ').capitalize()}")
