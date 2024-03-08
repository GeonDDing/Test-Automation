from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from webdriver_method import WebDriverMethod
from web_elements import MonitorDeviceElements, MainMenuElements
from login import Login


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
            self.error_log(f"{e}")
            return False

    def channel_start(self, channel_name):
        self.find_channel_index(channel_name)
        channel_start_element = self.monitor_device_elements.monitor_device_channel_start.format(self.chindex)
        channel_stop_element = self.monitor_device_elements.monitor_device_channel_stop.format(self.chindex)
        # Move to monitor device page
        try:
            self.click_element(By.XPATH, self.monitor_device_elements.monitor_device_page)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, channel_start_element)))
            self.click_element(By.CSS_SELECTOR, channel_start_element)
            self.step_log(f"#00{int(self.chindex)+1} {channel_name} 시작")
            return True
        except TimeoutException:
            try:
                self.step_log(f"#00{int(self.chindex)+1} {channel_name} 재시작")
                self.click_element(By.CSS_SELECTOR, channel_stop_element)
                self.accept_alert()
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, channel_start_element))
                    )
                    self.click_element(By.CSS_SELECTOR, channel_start_element)
                    return True
                except TimeoutException:
                    return False
            except (NoSuchElementException, ElementNotInteractableException) as e:
                self.error_log(f"{e}")
                return False


if __name__ == "__main__":
    test = MonitorDevice()
    login = Login()
    login.login("admin", "admin")
    test.find_channel_index("UDP Testing Channel")
    test.channel_start()
