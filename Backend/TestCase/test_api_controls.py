import pytest
import allure
import json
import sys
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
