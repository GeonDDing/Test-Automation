import allure
import json
import sys
sys.path.append('D:/Testing/API')
from api_operation import ApiOperation


def attach_response_step(step_name, response, status_name, result_name):
    with allure.step(step_name):
        if isinstance(response, tuple) and len(response) >= 2:
            status_code = str(response[0]) if isinstance(
                response[0], (int, float)) else response[0]
            allure.attach(f"Response Status Code: {status_code}",
                          name=status_name, attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"{json.dumps(response[1], indent=4)}",
                          name=result_name, attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(
                f"Invalid response format: {response}", name=status_name, attachment_type=allure.attachment_type.TEXT)


def perform_api_operations(api_operation, operation_name, *args):
    # GET
    response_get = api_operation.get_api_operation(None, *args)
    attach_response_step(f'GET {operation_name}', response_get,
                         "GET Response Status Code", "GET Response Result")


@allure.title("Logevents API")
def test_logevents():
    api_operation = ApiOperation('logevents')
    perform_api_operations(api_operation, 'logevents', 'severity', '3')


if __name__ == '__main__':
    test_logevents()