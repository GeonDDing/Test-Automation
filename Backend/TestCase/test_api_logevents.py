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
    # GET
    response_get = api_operation.get_api_operation(None, *args)
    attach_response_step(
        f"GET {operation_name}",
        response_get,
        "GET Response Status Code",
        "GET Response Result",
    )


@allure.title("Logevents API")
def test_logevents():
    api_operation = ApiOperation("logevents")
    perform_api_operations(api_operation, "logevents", "severity", "3")


if __name__ == "__main__":
    test_logevents()
