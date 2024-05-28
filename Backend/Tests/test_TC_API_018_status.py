import allure
import requests
import time
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

    @pytest.mark.parametrize(
        "first_uri_resource, groupid, devid, chidx",
        [("ip", "10.1.1.11", "27", "0")],
    )
    @allure.title("API: Status")
    def test_status(self, first_uri_resource, groupid, devid, chidx):
        generated_id = None
        failure_flags = {"get_failed": False}
        channel_start = {"operation": "transcode", "action": "start"}
        channel_stop = {"operation": "transcode", "action": "stop"}
        control_response = requests.put(
            f"{ApiOperation('controls').api_url}?id={devid}&chidx={chidx}",
            headers=ApiOperation("controls").headers,
            data=json.dumps(channel_start),
        )
        if control_response.status_code == 200:

            time.sleep(10)
            api_operation = ApiOperation("status")

            # GET
            with allure.step("GET Status"):
                try:
                    response_get = api_operation.get_api_operation(generated_id, first_uri_resource, groupid)
                    self.attach_response_result(
                        response_get,
                        "GET Response Status Code",
                        "GET Response Result",
                    )
                except AssertionError:
                    failure_flags["get_failed"] = True

            control_response = requests.put(
                f"{ApiOperation('controls').api_url}?id={devid}&chidx={chidx}",
                headers=ApiOperation("controls").headers,
                data=json.dumps(channel_stop),
            )

        # Check failure flags and fail the test if any step failed
        for step, failed in failure_flags.items():
            if failed:
                pytest.fail(f"{step.replace('_', ' ').capitalize()}")
