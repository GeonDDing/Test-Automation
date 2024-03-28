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
        print(services_options)
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
                    if any(keyword in key for keyword in input_options_key):
                        if key in ["Host", "Port", "Community"]:
                            if self.wait_element(
                                By.XPATH, self.networking_elements.networking_services_snmp_configure_button
                            ):
                                print(services_element)
                                # services_element = self.get_networking_elements("Services SNMP", key)
                                self.click_element(
                                    By.XPATH,
                                    self.networking_elements.networking_services_snmp_configure_button,
                                )
                            if self.wait_element(By.CSS_SELECTOR, services_element):
                                self.select_element(By.CSS_SELECTOR, services_element, "text", value)
                            self.click_element(
                                By.CSS_SELECTOR,
                                self.networking_elements.networking_services_snmp_apply_button,
                            )
                        # elif key == "SMB path":
                        #     if not self.find_web_element(By.CSS_SELECTOR, services_element).get_attribute("value"):
                        #         self.input_text(By.CSS_SELECTOR, services_element, value)
                        #         self.click_element(
                        #             By.CSS_SELECTOR,
                        #             self.networking_elements.networking_services_smb_mount_button,
                        #         )
                        # else:
                        #     self.input_text(By.CSS_SELECTOR, services_element, value)
                    else:
                        self.click_element(By.CSS_SELECTOR, services_element)
        except Exception as e:
            print(e)

    def get_networking_elements(self, netconfig, key):
        elements = getattr(
            self.networking_elements,
            f"networking_{netconfig.lower()}_{key.replace(' ', '_').replace('-', '_').lower()}",
            None,
        )
        return elements
