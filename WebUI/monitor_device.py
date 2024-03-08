from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from webdriver_method import WebDriverMethod
from web_elements import MonitorDeviceElements, MainMenuElements
from stats_receiver import StatsReceiver
from login import Login
import time


class MonitorDevice(WebDriverMethod):
    def __init__(self, chindex=0):
        super().__init__()
        self.monitor_device_elements = MonitorDeviceElements()
        self.click_element(By.XPATH, MainMenuElements().monitor)
        self.chindex = chindex

    def find_channel_index(self, channel_name):
        try:
            monitor_table = self.find_web_element(By.XPATH, self.monitor_device_elements.monitor_table)

            for idx, tr in enumerate(monitor_table.find_elements(By.XPATH, ".//tbody/tr")):
                if tr.find_elements(By.TAG_NAME, "td")[3].get_attribute("innerText") == channel_name:
                    self.chindex = idx
                    break

        except NoSuchElementException as e:
            self.error_log(e)
            return False

    def channel_start(self, channel_name):
        stats_instance = StatsReceiver()
        self.find_channel_index(channel_name)
        channel_start_element = self.monitor_device_elements.monitor_device_channel_start.format(self.chindex)
        channel_stop_element = self.monitor_device_elements.monitor_device_channel_stop.format(self.chindex)

        try:
            self.click_element(By.XPATH, self.monitor_device_elements.monitor_device_page)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, channel_start_element)))
            self.click_element(By.CSS_SELECTOR, channel_start_element)
            self.step_log(f"#00{int(self.chindex)+1} {channel_name} 시작")
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, channel_stop_element))
                )
                stats_instance.exec_multiprocessing(self.chindex)
                self.click_element(By.CSS_SELECTOR, channel_stop_element)
                self.accept_alert()

            except TimeoutException as e:
                self.error_log(e)
                return False

        except TimeoutException:
            self.step_log(f"#00{int(self.chindex)+1} {channel_name} 재시작")
            self.click_element(By.CSS_SELECTOR, channel_stop_element)
            self.accept_alert()

            try:
                WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, channel_start_element))
                )
                self.click_element(By.CSS_SELECTOR, channel_start_element)
                try:
                    WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, channel_stop_element))
                    )
                    stats_instance.exec_multiprocessing(self.chindex)
                    self.click_element(By.CSS_SELECTOR, channel_stop_element)
                    self.accept_alert()

                except TimeoutException as e:
                    self.error_log(e)
                    return False

            except TimeoutException as e:
                self.error_log(e)
                return False

        return True
