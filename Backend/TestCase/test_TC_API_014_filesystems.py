import allure
import pytest
import json
from api_operation import ApiOperation


@allure.parent_suite("Backend Test Automation")
@allure.suite("API")
@allure.sub_suite("File System")
class TestFileSystemAPI:
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

    @pytest.mark.parametrize("uri_resource, ip_address", [("ip", "10.1.0.145")])
    @allure.title("API:  File System")
    def test_devices(self, uri_resource, ip_address):
        api_operation = ApiOperation("filesystems")
        generated_id = None
        # uri_resource = "ip"
        # ip_address = "10.1.0.145"

        # GET
        with allure.step("GET File System"):
            response_get = api_operation.get_api_operation(generated_id, uri_resource, ip_address)
            self.attach_response_result(
                response_get,
                "GET Response Status Code",
                "GET Response Result",
            )

        # DELETE
        # with allure.step("DELETE File System"):
        #     response_delete = api_operation.delete_api_operation(generated_id)
        #     self.attach_response_result(
        #         response_delete,
        #         "DELETE Response Status Code",
        #         "DELETE Response Result",
        #     )
