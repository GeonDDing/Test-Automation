from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
)
from webdriver_method import WebDriverMethod
from web_elements import MonitorDeviceElements, MainMenuElements
import time


class MonitorDevice(WebDriverMethod):
    def __init__(self, chindex=0):
        self.monitor_device_elements = MonitorDeviceElements()
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
        self.click_element(By.XPATH, MainMenuElements().monitor)
        self.find_channel_index(channel_name)
        self.channel_start_element = self.monitor_device_elements.monitor_device_channel_start.format(self.chindex)
        self.channel_stop_element = self.monitor_device_elements.monitor_device_channel_stop.format(self.chindex)
        try:
            self.click_element(By.XPATH, self.monitor_device_elements.monitor_device_page)

            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_start_element))
            )
            self.click_element(By.CSS_SELECTOR, self.channel_start_element)
            self.step_log(f"#00{int(self.chindex+1)} {channel_name} Channel Starting")
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_stop_element))
                )
                return True, self.chindex

            except:
                # Action when startup fails after clicking the channel start button.
                self.info_log(f"#00{int(self.chindex+1)} {channel_name} Channel Start Failure")
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_start_element))
                    )
                    self.click_element(By.CSS_SELECTOR, self.channel_start_element)
                    self.info_log(f"#00{int(self.chindex+1)} {channel_name} Channel Restarting")
                    try:
                        WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_stop_element))
                        )
                        return True, self.chindex

                    except (TimeoutException, ElementNotInteractableException, AttributeError) as e:
                        self.error_log(e)
                        return False, None

                except (TimeoutException, ElementNotInteractableException, AttributeError) as e:
                    self.error_log(e)
                    return False, None

        except:
            self.info_log(f"#00{int(self.chindex+1)} {channel_name} Channel Restarting")
            self.click_element(By.CSS_SELECTOR, self.channel_stop_element)
            self.accept_alert()

            try:
                WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_start_element))
                )
                self.click_element(By.CSS_SELECTOR, self.channel_start_element)
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.channel_stop_element))
                    )
                    return True, self.chindex

                except (TimeoutException, ElementNotInteractableException, AttributeError) as e:
                    self.error_log(e)
                    return False, None

            except (TimeoutException, ElementNotInteractableException, AttributeError) as e:
                self.error_log(e)
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
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_start_all))
                )
                return True

            except (TimeoutException, ElementNotInteractableException, AttributeError) as e:
                self.error_log(e)
                return False

        except (TimeoutException, ElementNotInteractableException, AttributeError) as e:
            self.error_log(e)
            return False

    def channel_stop_all(self):
        try:
            self.click_element(By.XPATH, MainMenuElements().monitor)
            time.sleep(1)
            self.click_element(By.XPATH, self.monitor_device_elements.monitor_device_page)
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
