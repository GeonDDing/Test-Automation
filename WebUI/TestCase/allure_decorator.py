import allure


class AllureStepDecorator:
    def __init__(self, step_name, success_message, failure_message):
        self.step_name = step_name
        self.success_message = success_message
        self.failure_message = failure_message

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with allure.step(self.step_name):
                result = func(*args, **kwargs)
                status_message = self.success_message if result else self.failure_message
                allure.attach(
                    status_message,
                    name=self.step_name,
                    attachment_type=allure.attachment_type.TEXT,
                )
                assert result, self.failure_message

        return wrapper


def allure_step_decorator(step_name, success_message, failure_message):
    return AllureStepDecorator(step_name, success_message, failure_message)
