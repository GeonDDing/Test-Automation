# configure_group.py
from selenium.webdriver.common.by import By
from Pages.Configure.page_devices import ConfigureDevice
from TestConfig.web_locator import ConfigureGroupElements, MainMenuElements
import time


class ConfigureGroup(ConfigureDevice):
    def __init__(self):
        self.group_elements = ConfigureGroupElements()

    def access_configure_groups(self):
        try:
            self.click(By.XPATH, MainMenuElements().configure)
            self.click(By.XPATH, MainMenuElements().configure_groups)
            time.sleep(1)
        except Exception as e:
            self.error_log(f"An error occurred while accessing the group configuration page. | {repr(e)}")
            return False

    def configure_group(self, group_name, domain):
        try:
            self.access_configure_groups()

            if not self.find_exist_group(group_name):
                self.step_log(f"Group Creation")
                self.click(By.CSS_SELECTOR, self.group_elements.group_add_button)

                self.input_box(By.CSS_SELECTOR, self.group_elements.group_name, group_name)
            else:
                self.step_log(f"Group Modification")

            group_domain_selector = (
                f"{self.group_elements.group_domain}[value='1']"
                if domain == "Live"
                else f"{self.group_elements.group_domain}[value='2']"
            )
            self.click(By.CSS_SELECTOR, group_domain_selector)

            if domain == "Live":
                # Default : Evergreen 1
                trigger_css_selector = self.group_elements.group_live_trigger_evergreen1
                self.click(By.CSS_SELECTOR, trigger_css_selector)
                self.option_log(f"Domain : {domain}")
            self.click(By.CSS_SELECTOR, self.group_elements.group_save_button)
            return True
        except Exception as e:
            self.error_log(f"Group setting error| {repr(e)}")
            return False

    def find_exist_group(self, group_name):
        try:
            group_table = self.find_element(By.XPATH, self.group_elements.group_table)
            for tr in group_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[1].get_attribute("innerText")
                if column_value == group_name:
                    tr.find_elements(By.TAG_NAME, "td")[1].click()
                    return True
            return False
        except Exception as e:
            self.error_log(f"Not found exist group| {repr(e)}")
            return False
