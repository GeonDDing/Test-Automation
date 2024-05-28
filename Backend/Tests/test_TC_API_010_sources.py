import requests
import allure
import pytest
import json
import time

from Backend.api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Source")
class TestSourceAPI:

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

    # fmt: off
    @pytest.mark.parametrize("first_uri_resource, devid, second_uri_resource, chindex",[("devid", "27", "chindex", "0")],)
    @allure.title("API: Source")
    # fmt: on
    def test_sources(self, first_uri_resource, devid, second_uri_resource, chindex):
        # Source API 호출 전 채널 시작
        channel_start = {"operation": "transcode", "action": "start"}
        channel_stop = {"operation": "transcode", "action": "stop"}
        control_response = requests.put(
            f"{ApiOperation('controls').api_url}?id={devid}&chindex={chindex}",
            headers=ApiOperation("controls").headers,
            data=json.dumps(channel_start),
        )
        failure_flags = {
            "get_failed": False,
            "post_failed": False,
            "delete_failed": False,
        }

        if control_response.status_code == 200:
            print("Channel started successfully")
            time.sleep(20)
            api_operation = ApiOperation("sources")

            # GET
            with allure.step("GET Source"):
                try:
                    response_get = api_operation.get_api_operation(
                        None, first_uri_resource, devid, second_uri_resource, chindex
                    )
                    self.attach_response_result(
                        response_get,
                        "GET Response Status Code",
                        "GET Response Result",
                    )
                except AssertionError:
                    failure_flags["get_failed"] = True

            # POST
            with allure.step("POST Source"):
                try:
                    response_post = api_operation.post_api_operation(
                        first_uri_resource, devid, second_uri_resource, chindex
                    )
                    for i, response in enumerate(response_post):
                        self.attach_response_result(
                            response,
                            f"POST Response Status Code {i+1}",
                            f"POST Response Result {i+1}",
                        )
                except AssertionError:
                    failure_flags["post_failed"] = True

            # DELETE
            with allure.step("DELETE Source"):
                try:
                    response_delete = api_operation.delete_api_operation(
                        None, first_uri_resource, devid, second_uri_resource, chindex
                    )
                    self.attach_response_result(
                        response_delete,
                        "DELETE Response Status Code",
                        "DELETE Response Result",
                    )
                except AssertionError:
                    failure_flags["delete_failed"] = True

            requests.put(
                f"{ApiOperation('controls').api_url}?id={devid}&chidx={chindex}",
                headers=ApiOperation("controls").headers,
                data=json.dumps(channel_stop),
            )

        # Check failure flags and fail the test if any step failed
        for step, failed in failure_flags.items():
            if failed:
                pytest.fail(f"{step.replace('_', ' ').capitalize()}")
