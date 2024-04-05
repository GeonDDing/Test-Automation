import allure
import json
from api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("Group")
class TestGroupAPI:
    @staticmethod
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

    @allure.title("API: Group")
    def test_groups(self):
        api_operation = ApiOperation("groups")
        generated_id = None

        # GET
        with allure.step("GET Group"):
            response_get = api_operation.get_api_operation()
            self.attach_response_result(
                response_get,
                "GET Response Status Code",
                "GET Response Result",
            )

        # POST
        with allure.step("POST Group"):
            response_post = api_operation.post_api_operation()

            for i, response in enumerate(response_post):
                self.attach_response_result(
                    response,
                    f"POST Response Status Code {i+1}",
                    f"POST Response Result {i+1}",
                )

                if generated_id == None and "id" in response[1]:
                    generated_id = response[1]["id"]

        # PUT
        with allure.step("PUT Group"):
            response_put = api_operation.put_api_operation(generated_id)

            for i, response in enumerate(response_put):
                self.attach_response_result(
                    response,
                    f"PUT Response Status Code {i+1}",
                    f"PUT Response Result {i+1}",
                )

        # DELETE
        with allure.step("DELETE Group"):
            response_delete = api_operation.delete_api_operation(generated_id)
            self.attach_response_result(
                response_delete,
                "DELETE Response Status Code",
                "DELETE Response Result",
            )
