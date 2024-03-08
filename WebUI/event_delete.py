# configure_device.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import MainMenuElements
import time


class ConfigureDevice(WebDriverMethod):
    # def __init__(self):
    # self.event_elements
    def navigate_to_event(self):
        try:
            # Navigate to the 'EVENTS' page
            self.click_element(By.XPATH, MainMenuElements().events)
            time.sleep(1)  # Wait for the 'EVENTS' page to load
        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(e)

    def event_delete_all(self):
        # Navigate to the 'EVENTS' page
        self.navigate_to_event()
        try:
            self.info_log("Delete event")
            time.sleep(1)
        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(e)
