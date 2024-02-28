# configure_group.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    TimeoutException,
)
from configure_devices import ConfigureDevice
from web_elements import ConfigureGroupElements, MainMenuElements
import time


class ConfigureGroup(ConfigureDevice):
    def __init__(self):
        self.group_elements = ConfigureGroupElements()

    def navigate_to_configure_groups(self):
        try:
            # Navigate to the 'Configure Groups' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(By.XPATH, MainMenuElements().configure_groups)
            time.sleep(1)  # Wait for the 'CONFIGURE - Group' page to load

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")
            return False

    def configure_group(self, group_name, domain):
        try:
            print("Group setting")
            self.navigate_to_configure_groups()

            # Click the button to add a new group or find an existing one
            if not self.find_exist_group(group_name):
                self.click_element(
                    By.CSS_SELECTOR, self.group_elements.group_add_button
                )
                # Wait for the time to move to the group creation page.
                time.sleep(1)
                # Since there is no existing Group with the same name, a Group is created with that name.
                self.input_text(
                    By.CSS_SELECTOR, self.group_elements.group_name, group_name
                )
            else:
                print("A group with the same name exists.")

            # Set group domain
            group_domain_selector = (
                f"{self.group_elements.group_domain}[value='1']"
                if domain == "live"
                else f"{self.group_elements.group_domain}[value='2']"
            )
            self.click_element(By.CSS_SELECTOR, group_domain_selector)

            # Set group live trigger
            if domain == "live":
                # If necessary, set by adding parameter to configure_group function.
                # Default : Evergreen 1
                trigger_css_selector = self.group_elements.group_live_trigger_evergreen1
                self.click_element(By.CSS_SELECTOR, trigger_css_selector)

            # Save group settings
            self.click_element(By.CSS_SELECTOR, self.group_elements.group_save_button)
            # Wait for a moment before continuing
            print("Group setting complete")
            time.sleep(1)
            return True

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")
            return False

    def find_exist_group(self, group_name):
        try:
            group_table = self.find_web_element(
                By.XPATH, self.group_elements.group_table
            )

            for tr in group_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[1].get_attribute(
                    "innerText"
                )
                if column_value == group_name:
                    tr.find_elements(By.TAG_NAME, "td")[1].click()
                    return True  # Group found and clicked
            return False  # Group not found

        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False
