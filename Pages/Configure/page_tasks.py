# configure_device.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ConfigureTaskElements, MainMenuElements
import time


class ConfigureTask(WebDriverSetup):
    def __init__(self):
        self.task_elements = ConfigureTaskElements()

    def access_configure_tasks(self):
        try:
            self.click(By.XPATH, MainMenuElements().configure)
            self.click(By.XPATH, MainMenuElements().configure_tasks)
            time.sleep(1)
        except Exception as e:
            self.error_log(repr(e))
            return False

    def configure_task(self, task_name, taks_options=None):
        try:
            self.step_log("Task Creation")
            self.access_configure_tasks()

            if not self.find_exist_task(task_name):
                self.click(By.CSS_SELECTOR, self.task_elements.task_add_button)
                self.input_box(By.CSS_SELECTOR, self.task_elements.task_name, task_name)
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
                    self.select_box(By.CSS_SELECTOR, element_selector, "text", value)
                elif "Recurring weekly" == key:
                    self.click(By.CSS_SELECTOR, element_selector)
                else:
                    self.input_box(By.CSS_SELECTOR, element_selector, value)

            self.click(By.CSS_SELECTOR, self.task_elements.task_save_button)
            return True
        except Exception as e:
            self.error_log(e)
            return False

    def find_exist_task(self, task_name):
        try:
            task_table = self.find_element(By.XPATH, self.task_elements.task_table)

            for tr in task_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[1].get_attribute("innerText")
                if column_value == task_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True
            return False
        except Exception as e:
            self.error_log(e)
            return False
