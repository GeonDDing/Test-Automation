# configure_device.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import MainMenuElements
import time


class ConfigureDevice(WebDriverMethod):
    def access_event(self):
        # Navigate to the 'Configure devices' page
        self.click_element(By.XPATH, MainMenuElements().events)
        time.sleep(1)  # Wait for the 'CONFIGURE - device' page to load

    def event_delete_all(self):
        # Navigate to the 'Configure devices' page
        self.access_event()
        try:
            self.info_log("Delete event")

            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
