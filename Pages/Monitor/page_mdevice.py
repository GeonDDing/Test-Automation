from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import MonitorDeviceElements, MainMenuElements
import xml.etree.ElementTree as elementTree
import time
import requests


class MonitorDevice(WebDriverSetup):
    def __init__(self, chindex=0):
        self.monitor_device_elements = MonitorDeviceElements()
        self.chindex = chindex
        self.url = self.base_url_parser()
        self.channel_start_btn = self.monitor_device_elements.monitor_device_channel_start.format(self.chindex)
        self.channel_stop_btn = self.monitor_device_elements.monitor_device_channel_stop.format(self.chindex)

    def find_channel_index(self, channel_name):
        try:
            monitor_table = self.find_element(By.XPATH, self.monitor_device_elements.monitor_table)
            for idx, tr in enumerate(monitor_table.find_elements(By.XPATH, ".//tbody/tr")):
                if tr.find_elements(By.TAG_NAME, "td")[3].get_attribute("innerText") == channel_name:
                    self.chindex = idx
                    break

        except Exception as e:
            self.error_log(f"Not found exist monitoring channel| {repr(e)}")
            return False

    def channel_start(self, channel_name):
        channel_start_time = time.time()

        self.click(By.XPATH, MainMenuElements().monitor)
        time.sleep(1)
        self.find_channel_index(channel_name)
        self.click(By.XPATH, self.monitor_device_elements.monitor_table)
        try:
            starting_status = self.find_element(
                By.CSS_SELECTOR, self.monitor_device_elements.channel_starting_content_block
            ).value_of_css_property("display")
            stoping_status = self.find_element(
                By.CSS_SELECTOR, self.monitor_device_elements.channel_stoping_content_block
            ).value_of_css_property("display")
            if starting_status == "block" or stoping_status == "block":
                self.warning_log("The channel is ending so please wait for a moment.")
                time.sleep(30)
            self.step_log(f"#00{int(self.chindex+1)} {channel_name} Channel Starting")
            self.clickable_click(By.CSS_SELECTOR, self.channel_start_btn)
            time.sleep(10)
        except Exception as e:
            self.warning_log(f"#00{int(self.chindex+1)} {channel_name} Channel Start Failure | {e}")
            return False, None
        else:
            while True:
                stop_status = self.find_element(
                    By.CSS_SELECTOR, self.monitor_device_elements.channel_stop_content_block
                ).value_of_css_property("display")
                if stop_status == "block":
                    self.step_log(f"#00{int(self.chindex+1)} {channel_name} Channel Start success")
                    return True, self.chindex
                else:
                    if time.time() - channel_start_time > 70:
                        self.warning_log(f"#00{int(self.chindex+1)} Timeout, {channel_name} Channel Start Failure")
                        return False, None
                time.sleep(2)

    def channel_stop(self, chindex, channel_name):
        try:
            self.step_log(f"#00{int(chindex+1)} {channel_name} Channel Stoping")
            self.click(By.CSS_SELECTOR, self.channel_stop_btn)

            self.accept_alert()
        except Exception as e:
            self.warning_log(f"#00{int(chindex+1)} {channel_name} Channel Stop Failure | {e}")
            return False
        else:
            while True:
                if self.find_element(By.CSS_SELECTOR, "#ChannelBoxStopped0").value_of_css_property("display"):
                    self.step_log(f"#00{int(chindex+1)} {channel_name} Channel Stop success")
                    return True
                else:
                    self.warning_log(f"#00{int(chindex+1)} Timeout, {channel_name} Channel Stop Failure")
                    return False

    # def channel_stop(self, chindex, channel_name):
    #     try:
    #         self.clickable_click(By.CSS_SELECTOR, self.channel_stop_btn)
    #         self.step_log(f"#00{int(chindex+1)} {channel_name} Channel Stoping")
    #         self.click(By.CSS_SELECTOR, self.channel_stop_btn)
    #         self.accept_alert()
    #         while True:
    #             try:
    #                 channel_response = requests.get(f"{self.url}:900{chindex}/stats")
    #                 if channel_response.status_code == 200:
    #                     self.warning_log(f"#00{int(chindex+1)} {channel_name} Channel Stop Failure")
    #                     return False
    #             except requests.exceptions.ConnectionError as e:
    #                 return True
    #             else:
    #                 pass
    #             time.sleep(2)
    #     except Exception as e:
    #         self.error_log(f"The channel failed to stop because an error occurred | {repr(e)}")
    #         return False

    def channel_stop_all(self):
        try:
            self.click(By.XPATH, MainMenuElements().monitor)
            time.sleep(1)
            self.click(By.XPATH, self.monitor_device_elements.monitor_table)
            self.step_log("Stoping all channels")
            self.clickable_click(By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_stop_all)
            self.accept_alert()
            try:
                self.clickable_click(By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_start_all)
                return True
            except:
                return False

        except:
            return False
