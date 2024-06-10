# configure_device.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ConfigureDeviceElements, MainMenuElements
import time


class ConfigureDevice(WebDriverSetup):
    def __init__(self):
        self.device_elements = ConfigureDeviceElements()

    def navigate_to_configure_devices(self):
        try:
            self.click(By.XPATH, MainMenuElements().configure)
            self.click(By.XPATH, MainMenuElements().configure_devices)
            time.sleep(1)
        except Exception as e:
            self.error_log(f"Error moving to device configuration page | {repr(e)}")
            return False

    def configure_device(self, device_name, ip_address, group_name, role_name):
        try:
            self.navigate_to_configure_devices()
            if not self.find_exist_device(device_name):
                self.step_log(f"Device Creation")
                self.click(By.CSS_SELECTOR, self.device_elements.device_add_button)
                self.input_box(By.CSS_SELECTOR, self.device_elements.device_name, device_name)
            else:
                self.step_log(f"Device Modification")
            # IP Address
            self.input_box(By.CSS_SELECTOR, self.device_elements.device_ip_address, ip_address)
            # Select Group
            self.drop_down(
                By.CSS_SELECTOR,
                self.device_elements.device_include_group,
                "text",
                group_name,
            )
            # Select Role
            self.drop_down(
                By.CSS_SELECTOR,
                self.device_elements.device_include_role,
                "text",
                role_name,
            )
            self.option_log(f"Role : {role_name}")
            self.option_log(f"Group : {group_name}")
            # Save Device settings
            self.click(By.CSS_SELECTOR, self.device_elements.device_save_button)
            return True
        except Exception as e:
            self.error_log(f"Deivce setting error | {repr(e)}")
            return False, e

    def find_exist_device(self, device_name):
        try:
            device_table = self.find_element(By.XPATH, self.device_elements.device_table)
            for tr in device_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                if column_value == device_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True
            return False
        except Exception as e:
            self.error_log(f"Not found exist device | {repr(e)}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False
