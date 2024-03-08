# configure_group.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
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

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")
            return False

        finally:
            self.quit_driver()

    def configure_group(self, group_name, domain):
        try:
            self.navigate_to_configure_groups()
            # Click the button to add a new group or find an existing one
            if not self.find_exist_group(group_name):
                self.step_log(f"Group 설정")
                self.click_element(By.CSS_SELECTOR, self.group_elements.group_add_button)
                # Wait for the time to move to the group creation page.
                time.sleep(1)
                # Since there is no existing Group with the same name, a Group is created with that name.
                self.input_text(By.CSS_SELECTOR, self.group_elements.group_name, group_name)
            else:
                self.step_log(f"Group 수정")

            # Set group domain
            group_domain_selector = (
                f"{self.group_elements.group_domain}[value='1']"
                if domain == "Live"
                else f"{self.group_elements.group_domain}[value='2']"
            )
            self.click_element(By.CSS_SELECTOR, group_domain_selector)

            # Set group live trigger
            if domain == "Live":
                # If necessary, set by adding parameter to configure_group function.
                # Default : Evergreen 1
                trigger_css_selector = self.group_elements.group_live_trigger_evergreen1
                self.click_element(By.CSS_SELECTOR, trigger_css_selector)
                self.option_log(f"Domain : {domain}")
            # Save group settings
            self.click_element(By.CSS_SELECTOR, self.group_elements.group_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")
            return False

        finally:
            self.quit_driver()

    def find_exist_group(self, group_name):
        try:
            group_table = self.find_web_element(By.XPATH, self.group_elements.group_table)

            for tr in group_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[1].get_attribute("innerText")

                if column_value == group_name:
                    tr.find_elements(By.TAG_NAME, "td")[1].click()
                    return True  # Group found and clicked

            return False  # Group not found

        except NoSuchElementException as e:
            self.error_log(f"{e}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False

        finally:
            self.quit_driver()
