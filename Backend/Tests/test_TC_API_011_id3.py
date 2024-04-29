import allure
import pytest
import requests
import json
import time

from Backend.api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("ID3")
class TestID3API:

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

    @pytest.mark.parametrize(
        "first_uri_resource, second_uri_resoure, devid_value, chindex_value",
        [("devid", "chindex", "2", "0")],
    )
    @allure.title("API: ID3")
    def test_id3s(self, first_uri_resource, second_uri_resoure, devid_value, chindex_value):
        # id3 API 호출 전 채널 시작
        channel_start = {"operation": "transcode", "action": "start"}
        channel_stop = {"operation": "transcode", "action": "stop"}
        control_response = requests.put(
            f"{ApiOperation('controls').api_url}?id=2&chidx=0",
            headers=ApiOperation("controls").headers,
            data=json.dumps(channel_start),
        )

        if control_response.status_code == 200:
            print("Channel started successfully")
            time.sleep(10)
            api_operation = ApiOperation("id3s")
            generated_id = None

            # POST
            with allure.step("POST ID3"):
                response_post = api_operation.post_api_operation()

                for i, response in enumerate(response_post):
                    self.attach_response_result(
                        response,
                        f"POST Response Status Code {i+1}",
                        f"POST Response Result {i+1}",
                    )

            # GET after POST request
            with allure.step("GET ID3"):
                response_get = api_operation.get_api_operation(
                    generated_id,
                    first_uri_resource,
                    devid_value,
                    second_uri_resoure,
                    chindex_value,
                )
                self.attach_response_result(
                    response_get,
                    "GET Response Status Code",
                    "GET Response Result",
                )

            # PUT
            with allure.step("PUT ID3"):
                response_put = api_operation.put_api_operation()
                for i, response in enumerate(response_put):
                    self.attach_response_result(
                        response,
                        f"PUT Response Status Code {i+1}",
                        f"PUT Response Result {i+1}",
                    )

            # GET after PUT request
            with allure.step("GET ID3"):
                response_get = api_operation.get_api_operation(
                    generated_id,
                    first_uri_resource,
                    devid_value,
                    second_uri_resoure,
                    chindex_value,
                )
                self.attach_response_result(
                    response_get,
                    "GET Response Status Code",
                    "GET Response Result",
                )

            # DELETE
            with allure.step("DELETE ID3"):
                response_delete = api_operation.delete_api_operation(
                    None,
                    first_uri_resource,
                    devid_value,
                    second_uri_resoure,
                    chindex_value,
                    "key",
                    "key0",
                )
                self.attach_response_result(
                    response_delete,
                    "DELETE Response Status Code",
                    "DELETE Response Result",
                )
            requests.put(
                f"{ApiOperation('controls').api_url}?id=2&chidx=0",
                headers=ApiOperation("controls").headers,
                data=json.dumps(channel_stop),
            )
