# configure_device.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import ConfigureTaskElements, MainMenuElements
import time


class ConfigureTask(WebDriverMethod):
    def __init__(self):
        self.task_elements = ConfigureTaskElements()

    def navigate_to_configure_tasks(self):
        try:
            # Navigate to the 'Configure devices' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(By.XPATH, MainMenuElements().configure_tasks)
            time.sleep(1)  # Wait for the 'CONFIGURE Tasks' page to load

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def configure_task(self, task_name, taks_options=None):
        try:
            self.step_log("Task Creation")
            self.navigate_to_configure_tasks()

            # Click the button to add a new task or find an existing one
            if not self.find_exist_task(task_name):
                self.click_element(By.CSS_SELECTOR, self.task_elements.task_add_button)
                # Wait for the time to move to the task creation page.
                time.sleep(1)
                # Since there is no existing Task with the same name, a Task is created with that name.
                self.input_text(By.CSS_SELECTOR, self.task_elements.task_name, task_name)
            else:
                self.step_log("Task Modification")

            select_relevant_keys = {
                "Group",
                "Channel",
                "Task",
                "Replacement Image",
                "Replacement Playlist",
                "Recurring daily",
                "State",
            }

            for key, value in taks_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.task_elements,
                    (
                        f"task_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"task_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in select_relevant_keys):
                    self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                elif "Recurring weekly" == key:
                    self.click_element(By.CSS_SELECTOR, element_selector)
                else:
                    self.input_text(By.CSS_SELECTOR, element_selector, value)

            # Save task settings
            self.click_element(By.CSS_SELECTOR, self.task_elements.task_save_button)
            # Wait for a moment before continuing
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def find_exist_task(self, task_name):
        try:
            task_table = self.find_web_element(By.XPATH, self.task_elements.task_table)

            for tr in task_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[1].get_attribute("innerText")
                if column_value == task_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True  # Task found and clicked

            return False  # Task not found

        except NoSuchElementException as e:
            self.error_log(e)
            # Handle the error as needed, for example, return False or raise the exception again
            return False
