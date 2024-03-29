# configure_group.py
from selenium.webdriver.common.by import By
from web_elements import SettingsNetworkingElements, MainMenuElements
from webdriver_method import WebDriverMethod
import time


class SettingsNetworking(WebDriverMethod):
    def __init__(self):
        self.networking_elements = SettingsNetworkingElements()
        self.access_settings_networking()

    def access_settings_networking(self):
        try:
            self.click_element(By.XPATH, MainMenuElements().settings)
            self.click_element(By.XPATH, MainMenuElements().settings_networking)
            time.sleep(1)
        except Exception as e:
            self.error_log(f"An error occurred while accessing the networking settings page  {e}")
            return False

    def networking_services(self, services_options):
        netconfig = "Services"
        input_options_key = [
            "SMB path",
            "SNMP Host",
            "SNMP Port",
            "SNMP Community",
        ]
        try:
            self.sub_step_log(f"Networking {netconfig} Settings")
            if self.wait_element(By.CSS_SELECTOR, self.networking_elements.networking_netconfig_selector):
                # Enter the service options.
                self.select_element(
                    By.CSS_SELECTOR,
                    self.networking_elements.networking_netconfig_selector,
                    "text",
                    netconfig,
                )
                self.click_element(
                    By.CSS_SELECTOR,
                    self.networking_elements.networking_configure_button,
                )
                for key, value in services_options.items():
                    self.option_log(f"{key} : {value}")
                    services_element = self.get_networking_elements(netconfig, key)
                    # Network Services 에는 Text 입력만 있음
                    # SNMP 는 추후에 사용하게되면 UI에서 값 세팅만 자동화 (MIB Browser 를 사용해야해서 자동화 불가)
                    if any(keyword in key for keyword in input_options_key):
                        if key == "SMB path":
                            if not self.find_web_element(By.CSS_SELECTOR, services_element).get_attribute("value"):
                                self.input_text(By.CSS_SELECTOR, services_element, value)
                                self.click_element(
                                    By.CSS_SELECTOR,
                                    self.networking_elements.networking_services_smb_mount_button,
                                )
            return True
        except Exception as e:
            self.error_log(f"Networking {netconfig} setting error {e}")

    def get_networking_elements(self, netconfig, key):
        elements = getattr(
            self.networking_elements,
            f"networking_{netconfig.lower()}_{key.replace(' ', '_').replace('-', '_').lower()}",
            None,
        )
        return elements
