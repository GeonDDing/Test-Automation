# configure_device.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import ConfigureDeviceElements, MainMenuElements
import time


class ConfigureDevice(WebDriverMethod):
    def __init__(self):
        self.device_elements = ConfigureDeviceElements()

    def navigate_to_configure_devices(self):
        try:
            # Navigate to the 'Configure devices' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(By.XPATH, MainMenuElements().configure_devices)
            time.sleep(1)  # Wait for the 'CONFIGURE - Device' page to load

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(e)
            return False

    def configure_device(self, device_name, ip_address, group_name, role_name):
        try:
            self.navigate_to_configure_devices()
            # Click the button to add a new device or find an existing one
            if not self.find_exist_device(device_name):
                self.step_log(f"Device 설정")
                self.click_element(By.CSS_SELECTOR, self.device_elements.device_add_button)
                # Wait for the time to move to the device creation page.
                time.sleep(1)
                # Since there is no existing device with the same name, a device is created with that name.
                self.input_text(By.CSS_SELECTOR, self.device_elements.device_name, device_name)
            else:
                self.step_log(f"Device 수정")

            # IP Address
            self.input_text(By.CSS_SELECTOR, self.device_elements.device_ip_address, ip_address)
            # Select Group
            self.select_element(
                By.CSS_SELECTOR,
                self.device_elements.device_include_group,
                "text",
                group_name,
            )
            # Select Role
            self.select_element(
                By.CSS_SELECTOR,
                self.device_elements.device_include_role,
                "text",
                role_name,
            )
            self.option_log(f"Role : {role_name}")
            self.option_log(f"Group : {group_name}")
            # Save Device settings
            self.click_element(By.CSS_SELECTOR, self.device_elements.device_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(e)
            return False, e

    def find_exist_device(self, device_name):
        try:
            device_table = self.find_web_element(By.XPATH, self.device_elements.device_table)

            for tr in device_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")

                if column_value == device_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True  # Device found and clicked

            return False  # Device not found

        except NoSuchElementException as e:
            self.error_log(e)
            # Handle the error as needed, for example, return False or raise the exception again
            return False
