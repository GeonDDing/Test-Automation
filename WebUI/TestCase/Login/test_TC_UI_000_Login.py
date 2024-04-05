import allure
from login import Login

pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("Login")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Login")
class TestLogin:
    test_configuration_data = {
        "ID": "admin",
        "PW": "admin",
    }

    @staticmethod
    def attach_result(step_name, success_message, failure_message):
        def step_decorator(func):
            def step_wrapper(*args, **kwargs):
                with allure.step(step_name):
                    result = func(*args, **kwargs)
                    status_message = success_message if result else failure_message
                    allure.attach(
                        status_message,
                        name=step_name,
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    assert result, failure_message

            return step_wrapper

        return step_decorator

    @attach_result("Login", "Login Successful", "Login Failed")
    def login(self, **kwargs):
        with allure.step("Login"):
            login_instance = Login()
            return login_instance.login(kwargs["ID"], kwargs["PW"])

    @allure.sub_suite("Login")
    @allure.title("Login")
    def test_login(self):
        self.login(**self.test_configuration_data)


if __name__ == "__main__":
    TestLogin().test_login()
