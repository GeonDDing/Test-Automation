# configure_role.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.Configure.page_devices import ConfigureDevice
from Pages.Monitor.page_monitor_device import MonitorDevice
from TestConfig.web_locator import ConfigureRoleElements, MainMenuElements
import time

from Pages.Login.page_login import Login


class ConfigureRole(ConfigureDevice):
    def __init__(self):
        self.role_elements = ConfigureRoleElements()

    def access_configure_roles(self):
        try:
            self.click(By.XPATH, MainMenuElements().configure)
            self.click(By.XPATH, MainMenuElements().configure_roles)
            time.sleep(1)

        except Exception as e:
            self.error_log(f"An error occurred while accessing the role configuration page. | {repr(e)}")
            return False

    def configure_role(self, role_name, *channel_name):
        if MonitorDevice().channel_stop_all():
            self.access_configure_roles()
        else:
            MonitorDevice().channel_stop_all()
            self.access_configure_roles()
        try:
            if not self.find_exist_role(role_name):
                self.step_log(f"Role Creation")
                self.click(By.CSS_SELECTOR, self.role_elements.role_add_button)
                self.input_box(By.CSS_SELECTOR, self.role_elements.role_name, role_name)
                if channel_name:
                    for index, channel_value in enumerate(channel_name):
                        self.select_box(
                            By.XPATH,
                            self.role_elements.add_channel_list,
                            "text",
                            channel_value,
                        )
                        self.option_log(f"Channel : {channel_name[index]}")
            else:
                self.step_log(f"Role Modification")
                while True:
                    try:
                        self.click(By.CSS_SELECTOR, self.role_elements.role_remove_button)
                    except Exception as e:
                        self.info_log(f"Channel remove complete")
                        break
                if channel_name:
                    for index, channel_value in enumerate(channel_name):
                        self.select_box(By.XPATH, self.role_elements.add_channel_list, "text", channel_value)
                        self.option_log(f"Channel : {channel_name[index]}")

            self.click(By.CSS_SELECTOR, self.role_elements.role_save_button)
            return True
        except Exception as e:
            self.error_log(f"Role setting error| {repr(e)}")
            return False

    def find_exist_role(self, role_name):
        try:
            role_table = self.find_element(By.XPATH, self.role_elements.role_table)
            for tr in role_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                if column_value == role_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True
            return False
        except Exception as e:
            self.error_log(f"Not found exist role| {repr(e)}")
            return False
