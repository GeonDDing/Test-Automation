import pytest
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
            assert (
                status_code == "200"
            ), f"Expected status code 200 but received {status_code}"
        else:
            allure.attach(
                f"Invalid response format: {response}",
                name=status_name,
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail("Invalid response format")


def perform_api_operations(api_operation, operation_name, *args):
    # PUT
    response_put = api_operation.put_api_operation(*args)
    for i, response in enumerate(response_put):
        attach_response_step(
            f"PUT {operation_name}",
            response,
            f"PUT Response Status Code {i+1}",
            f"PUT Response Result {i+1}",
        )


# @pytest.mark.skip(reason="이 테스트는 스킵됩니다.")
@allure.title("Contorl API")
def test_controls():
    api_operation = ApiOperation("controls")
    perform_api_operations(api_operation, "Control", 2, "chidx", 0)
