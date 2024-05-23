import allure
import requests
import time
import json
import pytest
from Backend.api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Scrolling Text")
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
        "first_uri_resource, devid, second_uri_resource, chidx, channelid", [("devid", "16", "chidx", "0", "16")]
    )
    @allure.title("API: Scrolling Text")
    def test_scrollingtext(self, first_uri_resource, devid, second_uri_resource, chidx, channelid):
        channel_start = {"operation": "transcode", "action": "start"}
        channel_stop = {"operation": "transcode", "action": "stop"}
        control_response = requests.put(
            f"{ApiOperation('controls').api_url}?id={devid}&chidx={chidx}",
            headers=ApiOperation("controls").headers,
            data=json.dumps(channel_start),
        )

        if control_response.status_code == 200:
            print("Channel started successfully")
            time.sleep(10)
            api_operation = ApiOperation("scrollingtext")

            # PUT
            with allure.step("PUT Scrolling Text"):
                response_put = api_operation.put_api_operation(
                    channelid, first_uri_resource, devid, second_uri_resource, chidx
                )
                for i, response in enumerate(response_put):
                    self.attach_response_result(
                        response,
                        f"PUT Response Status Code {i+1}",
                        f"PUT Response Result {i+1}",
                    )
                time.sleep(60)

            control_response = requests.put(
                f"{ApiOperation('controls').api_url}?id={devid}&chidx={chidx}",
                headers=ApiOperation("controls").headers,
                data=json.dumps(channel_stop),
            )
