import allure
import json
import sys
import pytest
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from api_operation import ApiOperation


def attach_response_step(step_name, response, status_name, result_name):
    with allure.step(step_name):
        if str(response[0]) == "200":
            allure.attach(
                f"Response Status Code: {response[0]}, 테스트 성공",
                name=status_name,
                attachment_type=None,
            )
            allure.attach(
                f"{json.dumps(response[1], indent=4)}",
                name=result_name,
                attachment_type=None,
            )
        else:
            allure.attach(
                f"Response Status Code: {response[0]}, 테스트 실패",
                name=status_name,
                attachment_type=None,
            )
            assert str(response[0]) == "200", "테스트 실패"


def perform_api_operations(api_operation, operation_name, generated_id=None):
    # GET
    response_get = api_operation.get_api_operation()
    attach_response_step(
        f"GET {operation_name}",
        response_get,
        "GET Response Status Code",
        "GET Response Result",
    )

    # POST
    response_post = api_operation.post_api_operation()
    for i, response in enumerate(response_post):
        attach_response_step(
            f"POST {operation_name}",
            response,
            f"POST Response Status Code {i+1}",
            f"POST Response Result {i+1}",
        )

        if generated_id == None and "id" in response[1]:
            generated_id = response[1]["id"]

    # PUT
    response_put = api_operation.put_api_operation(generated_id)
    for i, response in enumerate(response_put):
        attach_response_step(
            f"PUT {operation_name}",
            response,
            f"PUT Response Status Code {i+1}",
            f"PUT Response Result {i+1}",
        )

    # DELETE
    response_delete = api_operation.delete_api_operation(generated_id)
    attach_response_step(
        f"DELETE {operation_name}",
        response_delete,
        "DELETE Response Status Code",
        "DELETE Response Result",
    )


# @pytest.mark.skip(reason="이 테스트는 스킵됩니다.")
@allure.title("Device API")
def test_devices():
    api_operation = ApiOperation("devices")
    perform_api_operations(api_operation, "Device")
