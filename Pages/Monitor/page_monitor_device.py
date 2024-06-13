from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import MonitorDeviceElements, MainMenuElements
import xml.etree.ElementTree as elementTree
import time
import requests


class MonitorDevice(WebDriverSetup):
    def __init__(self, chindex=int()):
        self.monitor_device_elements = MonitorDeviceElements()
        self.chindex = chindex
        self.url = self.base_url_parser()

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
        self.channel_start_btn = self.monitor_device_elements.monitor_device_channel_start.format(self.chindex)
        self.click(By.XPATH, self.monitor_device_elements.monitor_table)
        time.sleep(3)
        # 채널 상태 변화 체크를 위한 Locator
        start_content = (By.CSS_SELECTOR, self.monitor_device_elements.channel_start_content_block.format(self.chindex))
        stop_content = (By.CSS_SELECTOR, self.monitor_device_elements.channel_stop_content_block.format(self.chindex))
        starting_content = (
            By.CSS_SELECTOR,
            self.monitor_device_elements.channel_starting_content_block.format(self.chindex),
        )
        stoping_content = (
            By.CSS_SELECTOR,
            self.monitor_device_elements.channel_stoping_content_block.format(self.chindex),
        )
        try:
            if (
                self.is_element_displayed(*starting_content) == "block"
                or self.is_element_displayed(*stoping_content) == "block"
            ):
                self.warning_log("The channel is stoping... so please wait for a moment.")
                time.sleep(30)
            self.step_log(f"#00{int(self.chindex+1)} {channel_name} Channel Starting")
            self.clickable_click(By.CSS_SELECTOR, self.channel_start_btn)
            time.sleep(10)
        except Exception as e:
            self.warning_log(f"#00{int(self.chindex+1)} {channel_name} Channel Start Failure | {e}")
            return False, None
        else:
            try:
                while True:
                    if self.is_element_displayed(*stop_content) == "block":
                        self.step_log(f"#00{int(self.chindex+1)} {channel_name} Channel Start Success")
                        return True, self.chindex
                    else:
                        if time.time() - channel_start_time > 70:
                            self.error_log(f"#00{int(self.chindex+1)} Timeout, {channel_name} Channel Start Failure")
                            return False, None
                        else:
                            if self.is_element_displayed(*start_content):
                                self.click(By.CSS_SELECTOR, self.channel_start_btn)
                                time.sleep(10)
                                if self.is_element_displayed(*stop_content) == "block":
                                    self.step_log(
                                        f"#00{int(self.chindex+1)} {channel_name} Channel Start Retry Success"
                                    )
                                    return True, self.chindex
                                else:
                                    self.error_log(
                                        f"#00{int(self.chindex+1)} Timeout, {channel_name} Channel Start Retry Failure"
                                    )
                                    return False, None
            except Exception as e:
                self.error_log(f"#00{int(self.chindex+1)} {channel_name} Channel Start Failure | {e}")
                time.sleep(2)

    def channel_stop(self, chindex, channel_name):
        self.channel_stop_btn = self.monitor_device_elements.monitor_device_channel_stop.format(chindex)
        try:
            self.step_log(f"#00{int(chindex+1)} {channel_name} Channel Stoping")
            self.click(By.CSS_SELECTOR, self.channel_stop_btn)
            self.accept_alert()
            channel_stop_time = time.time()
        except Exception as e:
            self.error_log(f"#00{int(chindex+1)} {channel_name} Channel Stop Failure | {e}")
            return False
        else:
            while True:
                start_content = (
                    By.CSS_SELECTOR,
                    self.monitor_device_elements.channel_start_content_block.format(chindex),
                )
                if time.time() - channel_stop_time > 30:
                    if self.is_element_displayed(*start_content) == "block":
                        self.step_log(f"#00{int(chindex+1)} {channel_name} Channel Stop Success")
                        return True
                    else:
                        self.error_log(f"#00{int(chindex+1)} Timeout, {channel_name} Channel Stop Failure")
                        return False
                else:
                    if self.is_element_displayed(*start_content) == "block":
                        self.step_log(f"#00{int(chindex+1)} {channel_name} Channel Stop Success")
                        return True

    def channel_stop_all(self):
        try:
            self.click(By.XPATH, MainMenuElements().monitor)
            time.sleep(1)
            self.click(By.XPATH, self.monitor_device_elements.monitor_table)
            self.step_log("Stoping all channels")
            self.clickable_click(By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_stop_all)
            if self.accept_alert():
                if self.is_displayed(By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_start_all):
                    self.info_log("Stop All : True")
                    return True
                else:
                    self.info_log("Stop All : False")
                    return False
            else:
                if self.is_displayed(By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_start_all):
                    self.info_log("Stop All : True")
                    return True
                else:
                    self.info_log("Stop All : False")
                    return False
        except:
            return False
