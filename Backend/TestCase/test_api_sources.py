import requests
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
@allure.sub_suite("Source")
class TestSourceAPI:
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

    # fmt: off
    @pytest.mark.parametrize("devid_vlaue, chidx_value",[("2", "0")],)
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
