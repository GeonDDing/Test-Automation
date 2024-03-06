# # configure_channels.py
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import (
#     NoSuchElementException,
#     ElementNotVisibleException,
#     TimeoutException,
# )
# from webdriver_method import WebDriverMethod
# from web_elements import MonitorDeviceElements, MainMenuElements
# from login import Login
# import time


# class MonitorDevice(WebDriverMethod):
#     def __init__(self, chindex=0):
#         self.monitor_device_elements = MonitorDeviceElements()
#         self.chindex = chindex

#     def find_channel_index(self, channel_name):
#         try:
#             idx = 0
#             if self.wait_element(By.XPATH, self.monitor_device_elements.monitor_table):
#                 monitor_table = self.find_web_element(
#                     By.XPATH, self.monitor_device_elements.monitor_table
#                 )
#             for tr in monitor_table.find_elements(By.XPATH, ".//tbody/tr"):
#                 column_value = tr.find_elements(By.TAG_NAME, "td")[3].get_attribute(
#                     "innerText"
#                 )
#                 if column_value == channel_name:
#                     self.chindex = idx
#                     # print(f"{self.chindex} : {column_value}")
#                     break
#                 idx += 1

#         except NoSuchElementException as e:
#             print(f"Element not found: {e}")
#             return False

#     def channel_start(self):
#         # Add channel index in channel start and stop button
#         channel_start_element = (
#             self.monitor_device_elements.monitor_device_channel_start.format(
#                 self.chindex
#             )
#         )
#         channel_stop_element = (
#             self.monitor_device_elements.monitor_device_channel_stop.format(
#                 self.chindex
#             )
#         )
#         self.click_element(
#             By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_page
#         )
#         try:
#             # Wait until the button is clickable
#             WebDriverWait(self.driver, 5).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, channel_start_element))
#             )
#             print("Channel 시작")
#             self.click_element(By.CSS_SELECTOR, channel_start_element)
#             try:
#                 WebDriverWait(self.driver, 30).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, channel_stop_element))
#                 )
#                 return True

#             except:
#                 return False

#         except TimeoutException:
#             print("Channel 재시작")
#             self.click_element(By.CSS_SELECTOR, channel_stop_element)
#             # Click OK in the message window confirming channel termination. (Alert)
#             self.accept_alert()
#             # Wait for channel termination
#             try:
#                 # Wait until the button is clickable
#                 WebDriverWait(self.driver, 30).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, channel_start_element))
#                 )
#                 # Restart the channel when it terminatie.
#                 self.click_element(By.CSS_SELECTOR, channel_start_element)
#                 try:
#                     WebDriverWait(self.driver, 30).until(
#                         EC.element_to_be_clickable(
#                             (By.CSS_SELECTOR, channel_stop_element)
#                         )
#                     )
#                     return True

#                 except:
#                     return False
#             except TimeoutException:
#                 print("Channel 시작 실패")
#                 return False


# if __name__ == "__main__":
#     test = MonitorDevice()
#     login = Login()
#     login.login("admin", "admin")
#     test.find_channel_index("UDP Testing Channel")
#     test.channel_start()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from webdriver_method import WebDriverMethod
from web_elements import MonitorDeviceElements
from login import Login


class MonitorDevice(WebDriverMethod):
    def __init__(self, chindex=0):
        super().__init__()
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
            print(f"Element not found: {e}")
            return False

    def channel_start(self, channel_name):
        self.find_channel_index(channel_name)
        channel_start_element = self.monitor_device_elements.monitor_device_channel_start.format(self.chindex)
        channel_stop_element = self.monitor_device_elements.monitor_device_channel_stop.format(self.chindex)
        # Move to monitor device page
        try:
            self.click_element(By.CSS_SELECTOR, self.monitor_device_elements.monitor_device_page)
            self.click_element(By.CSS_SELECTOR, channel_start_element)
            print("Channel 시작")
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, channel_stop_element)))
            return True
        except TimeoutException:
            try:
                print("Channel 정지")
                self.click_element(By.CSS_SELECTOR, channel_stop_element)
                self.accept_alert()
                try:
                    print("Channel 제시작")
                    self.click_element(By.CSS_SELECTOR, channel_start_element)
                    WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, channel_stop_element))
                    )
                    return True
                except TimeoutException:
                    return False
            except (NoSuchElementException, ElementNotInteractableException) as e:
                print(f"Error: {e}")
                return False


if __name__ == "__main__":
    test = MonitorDevice()
    login = Login()
    login.login("admin", "admin")
    test.find_channel_index("UDP Testing Channel")
    test.channel_start()
