# configure_role.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    TimeoutException,
)
from configure_devices import ConfigureDevice
from web_elements import ConfigureRoleElements, MainMenuElements
import time


class ConfigureRole(ConfigureDevice):
    def __init__(self):
        self.role_elements = ConfigureRoleElements()

    def navigate_to_configure_roles(self):
        try:
            # Navigate to the 'Configure Roles' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(By.XPATH, MainMenuElements().configure_roles)
            time.sleep(1)  # Wait for the 'CONFIGURE - Role' page to load

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")
            return False

    def configure_role(self, role_name, *channel_name):
        try:
            print("Role setting")
            self.navigate_to_configure_roles()

            # Click the button to add a new role or find an existing one
            if not self.find_exist_role(role_name):
                self.click_element(By.CSS_SELECTOR, self.role_elements.role_add_button)
                # Wait for the time to move to the group creation page.
                time.sleep(1)
                # Since there is no existing Role with the same name, a Role is created with that name.
                self.input_text(
                    By.CSS_SELECTOR, self.role_elements.role_name, role_name
                )
                if channel_name:
                    for index, channel_value in enumerate(channel_name):
                        self.select_element(
                            By.XPATH,
                            self.role_elements.add_channel_list,
                            "text",
                            channel_value,
                        )
            else:
                print("A role with the same name exists.")
                if channel_name:
                    for index, channel_value in enumerate(channel_name):
                        selected_channel_list = f"//*[@id='channel{index}']"
                        self.select_element(
                            By.XPATH, selected_channel_list, "text", channel_value
                        )

            self.click_element(By.CSS_SELECTOR, self.role_elements.role_save_button)
            print("Role setting complete")
            time.sleep(1)
            return True

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")
            return False

    def find_exist_role(self, role_name):
        try:
            role_table = self.find_web_element(By.XPATH, self.role_elements.role_table)
            for tr in role_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute(
                    "innerText"
                )
                if column_value == role_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True  # Role found and clicked
            return False  # Role not found

        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False
