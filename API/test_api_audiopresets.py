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


@allure.title("Audiopreset API")
def test_audiopresets():
    api_operation = ApiOperation("audiopresets")
    perform_api_operations(api_operation, "Audiopreset")
