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

    def attach_response_result(response, status_name, result_name):
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
    @pytest.mark.parametrize("devid_vlaue, chidx_value",[("3", "0")],)
    @allure.title("API: Source")
    # fmt: on
    def test_sources(self, devid_vlaue, chidx_value):
        # Source API 호출 전 채널 시작
        channel_start = {"operation": "transcode", "action": "start"}
        channel_stop = {"operation": "transcode", "action": "stop"}
        control_response = requests.put(
            f"{ApiOperation('controls').api_url}?id={devid_vlaue}&chidx={chidx_value}",
            headers=ApiOperation("controls").headers,
            data=json.dumps(channel_start),
        )
        if control_response.status_code == 200:
            print("Channel started successfully")
            time.sleep(10)
            api_operation = ApiOperation("sources")

            # POST
            with allure.step("POST Source"):
                response_post = api_operation.post_api_operation()
                for i, response in enumerate(response_post):
                    self.attach_response_result(
                        response,
                        f"POST Response Status Code {i+1}",
                        f"POST Response Result {i+1}",
                    )

            requests.put(
                f"{ApiOperation('controls').api_url}?id={devid_vlaue}&chidx={chidx_value}",
                headers=ApiOperation("controls").headers,
                data=json.dumps(channel_stop),
            )
