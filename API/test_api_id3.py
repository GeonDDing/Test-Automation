from time import sleep
import requests
import allure
import json
import sys

sys.path.append("./API")
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

    # GET after POST request
    response_get = api_operation.get_api_operation(None, "devid", "1", "chindex", "1")
    attach_response_step(
        f"GET {operation_name}",
        response_get,
        "GET Response Status Code",
        "GET Response Result",
    )

    # PUT
    response_put = api_operation.put_api_operation()
    for i, response in enumerate(response_put):
        attach_response_step(
            f"PUT {operation_name}",
            response,
            f"PUT Response Status Code {i+1}",
            f"PUT Response Result {i+1}",
        )

    # GET after PUT request
    response_get = api_operation.get_api_operation(None, "devid", "1", "chindex", "1")
    attach_response_step(
        f"GET {operation_name}",
        response_get,
        "GET Response Status Code",
        "GET Response Result",
    )

    # DELETE
    response_delete = api_operation.delete_api_operation(
        None, "devid", "1", "chindex", "1", "key", "key0"
    )
    attach_response_step(
        f"DELETE {operation_name}",
        response_delete,
        "DELETE Response Status Code",
        "DELETE Response Result",
    )


@allure.title("ID3 API")
def test_id3s():
    # id3 API 호출 전 채널 시작
    channel_start = {"operation": "transcode", "action": "start"}
    channel_stop = {"operation": "transcode", "action": "stop"}
    control_response = requests.put(
        f"{ApiOperation('controls').api_url}?id=1&chidx=1",
        headers=ApiOperation("controls").headers,
        data=json.dumps(channel_start),
    )
    if control_response.status_code == 200:
        print("Channel started successfully")
        sleep(10)
    api_operation = ApiOperation("id3s")
    perform_api_operations(api_operation, "id3")
    requests.put(
        f"{ApiOperation('controls').api_url}?id=1&chidx=1",
        headers=ApiOperation("controls").headers,
        data=json.dumps(channel_stop),
    )
