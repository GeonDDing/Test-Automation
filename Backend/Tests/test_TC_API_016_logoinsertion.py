import allure
import requests
import json
import time
import pytest
from Backend.api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Logo Insertion")
class TestLogoInsertionAPI:

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
        "first_uri_resource, devid, second_uri_resource, chidx, channelid", [("devid", "27", "chidx", "0", "16")]
    )
    @allure.title("API: Logo Insertion")
    def test_logoinsertion(self, first_uri_resource, devid, second_uri_resource, chidx, channelid):
        failure_flags = {
            "put_failed": False,
            "delete_failed": False,
        }
        additional_uri = f"={channelid}&devid={devid}&chidx={chidx}"
        channel_start = {"operation": "transcode", "action": "start"}
        channel_stop = {"operation": "transcode", "action": "stop"}
        control_response = requests.put(
            f"{ApiOperation('controls').api_url}?id={devid}&chidx=0",
            headers=ApiOperation("controls").headers,
            data=json.dumps(channel_start),
        )

        if control_response.status_code == 200:
            print("Channel started successfully")
            time.sleep(20)
            api_operation = ApiOperation("logoinsertion")

            # PUT
            with allure.step("PUT Logo Insertion"):
                try:
                    response_put = api_operation.put_api_operation(
                        channelid, first_uri_resource, devid, second_uri_resource, chidx
                    )
                    for response in response_put:
                        self.attach_response_result(
                            response,
                            "PUT Response Status Code",
                            "PUT Response Result",
                        )
                except AssertionError:
                    failure_flags["put_failed"] = True

            # DELETE
            with allure.step("DELETE Logo Insertion"):
                try:
                    response_delete = api_operation.delete_api_operation(additional_uri)
                    self.attach_response_result(
                        response_delete,
                        "DELETE Response Status Code",
                        "DELETE Response Result",
                    )
                except AssertionError:
                    failure_flags["delete_failed"] = True

            control_response = requests.put(
                f"{ApiOperation('controls').api_url}?id={devid}&chidx={chidx}",
                headers=ApiOperation("controls").headers,
                data=json.dumps(channel_stop),
            )

        # Check failure flags and fail the test if any step failed
        for step, failed in failure_flags.items():
            if failed:
                pytest.fail(f"{step.replace('_', ' ').capitalize()}")
