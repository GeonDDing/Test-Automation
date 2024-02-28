from time import sleep
import requests
import allure
import pytest
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api_operation import ApiOperation


def attach_response_step(step_name, response, status_name, result_name):
    with allure.step(step_name):
        if isinstance(response, tuple) and len(response) >= 2:
            status_code = (
                str(response[0])
                if isinstance(response[0], (int, float))
                else response[0]
            )
            allure.attach(
                f"Response Status Code: {status_code}",
                name=status_name,
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                f"{json.dumps(response[1], indent=4)}",
                name=result_name,
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            allure.attach(
                f"Invalid response format: {response}",
                name=status_name,
                attachment_type=allure.attachment_type.TEXT,
            )


def perform_api_operations(api_operation, operation_name):
    # POST
    response_post = api_operation.post_api_operation()
    for i, response in enumerate(response_post):
        attach_response_step(
            f"POST {operation_name}",
            response,
            f"POST Response Status Code {i+1}",
            f"POST Response Result {i+1}",
        )


@allure.title("Source API")
def test_sources(devid=2, chidx=0):
    # Source API 호출 전 채널 시작
    channel_start = {"operation": "transcode", "action": "start"}
    channel_stop = {"operation": "transcode", "action": "stop"}
    control_response = requests.put(
        f"{ApiOperation('controls').api_url}?id={devid}&chidx={chidx}",
        headers=ApiOperation("controls").headers,
        data=json.dumps(channel_start),
    )
    if control_response.status_code == 200:
        print("Channel started successfully")
        sleep(10)
        api_operation = ApiOperation("sources")
        perform_api_operations(api_operation, "Sources")
        requests.put(
            f"{ApiOperation('controls').api_url}?id={devid}&chidx={chidx}",
            headers=ApiOperation("controls").headers,
            data=json.dumps(channel_stop),
        )