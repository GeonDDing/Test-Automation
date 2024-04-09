from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_method import WebDriverMethod
from web_elements import MonitorDeviceElements, MainMenuElements
import time
import requests


class MonitorDevice(WebDriverMethod):
    def __init__(self, chindex=0):
        self.monitor_device_elements = MonitorDeviceElements()
        self.chindex = chindex
        self.url = self.base_url_parser()

    def find_channel_index(self, channel_name):
        try:
            monitor_table = self.find_web_element(By.XPATH, self.monitor_device_elements.monitor_table)
            for idx, tr in enumerate(monitor_table.find_elements(By.XPATH, ".//tbody/tr")):
                if tr.find_elements(By.TAG_NAME, "td")[3].get_attribute("innerText") == channel_name:
                    self.chindex = idx
                    break

        except NoSuchElementException as e:
            self.error_log(f"Not found exist monitoring channel {e}")
            return False

    def channel_start(self, channel_name):
        is_channel_start = bool()
        self.click_element(By.XPATH, MainMenuElements().monitor)
        time.sleep(0.5)
        self.find_channel_index(channel_name)
        time.sleep(0.5)
        self.click_element(By.XPATH, self.monitor_device_elements.monitor_table)
        self.channel_start_element = self.monitor_device_elements.monitor_device_channel_start.format(self.chindex)
        self.channel_stop_element = self.monitor_device_elements.monitor_device_channel_stop.format(self.chindex)
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_start_element))
            )
            self.click_element(By.CSS_SELECTOR, self.channel_start_element)
            self.step_log(f"#00{int(self.chindex+1)} {channel_name} Channel Starting")
            channel_start_time = time.time()
            while True:
                try:
                    channel_status = requests.get(f"{self.url}:900{self.chindex}/stats")
                    if channel_status.status_code == 200:
                        is_channel_start = True
                        break
                except requests.exceptions.ConnectionError as e:
                    if time.time() - channel_start_time > 70:
                        self.warning_log(f"#00{int(self.chindex+1)} {channel_name} Channel Start Failure")
                        is_channel_start = False, None
                        break
                time.sleep(2)
            if not is_channel_start:
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_start_element))
                    )
                    self.click_element(By.CSS_SELECTOR, self.channel_start_element)
                    self.info_log(f"#00{int(self.chindex+1)} {channel_name} Channel Restarting")
                    channel_restart_time = time.time()
                    while True:
                        try:
                            channel_status = requests.get(f"{self.url}:900{self.chindex}/stats")
                            if channel_status.status_code == 200:
                                break
                        except requests.exceptions.ConnectionError as e:
                            if time.time() - channel_restart_time > 70:
                                self.warning_log(f"#00{int(self.chindex+1)} {channel_name} Channel Start Failure")
                                return False, None
                        time.sleep(2)
                except Exception as e:
                    self.error_log(f"The channel failed to restart because an error occurred. {e}")
                    return False, None
            return True, self.chindex
        except Exception as e:
            self.error_log(f"The channel failed to start because an error occurred. {e}")
            return False, None

    def channel_stop(self, chindex, channel_name):
        self.channel_start_element = self.monitor_device_elements.monitor_device_channel_start.format(chindex)
        self.channel_stop_element = self.monitor_device_elements.monitor_device_channel_stop.format(chindex)
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_stop_element))
            )
            self.step_log(f"#00{int(chindex+1)} {channel_name} Channel Stoping")
            self.click_element(By.CSS_SELECTOR, self.channel_stop_element)
            self.accept_alert()
            channel_stop_time = time.time()
            while True:
                try:
                    channel_status = requests.get(f"{self.url}:900{chindex}/stats")
                    if channel_status.status_code == 200:
                        if time.time() - channel_stop_time > 70:
                            self.warning_log(f"#00{int(chindex+1)} {channel_name} Channel Stop Failure")
                            return False
                except requests.exceptions.ConnectionError as e:
                    return True
                time.sleep(2)

        except Exception as e:
            self.error_log(f"The channel failed to stop because an error occurred. {e}")
            return False

    def channel_stop_all(self):
        try:
            self.click_element(By.XPATH, MainMenuElements().monitor)
            time.sleep(1)
            self.click_element(By.XPATH, self.monitor_device_elements.monitor_table)
            WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_stop_all))
            )
            self.step_log("Stoping all channels")
            self.click_element(By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_stop_all)
            self.accept_alert()
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_start_all))
                )
                return True
            except:
                return False
        except:
            return False
