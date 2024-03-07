# webdriver_method.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
from webdriver_init import WebDriverInit
from web_log import WebLog
import time
import platform


class WebDriverMethod(WebDriverInit, WebLog):
    driver = webdriver.Chrome(options=WebDriverInit().options)
    driver.set_window_size(1280, 1920)

    def find_web_element(self, by, locator):
        try:
            return self.driver.find_element(by, locator)
        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.web_log(f"[ERROR] {e}")
            return None

    def click_element(self, by, locator):
        self.find_web_element(by, locator).click()
        time.sleep(1)

    def input_text(self, by, locator, contents):
        if platform.system() == "Darwin":
            element = self.find_web_element(by, locator)
            element.send_keys(Keys.COMMAND + "A")
            time.sleep(0.3)
            element.send_keys(Keys.DELETE)
            time.sleep(0.3)
            element.send_keys(contents)
        else:
            element = self.find_web_element(by, locator)
            element.send_keys(Keys.CONTROL + "A")
            time.sleep(0.3)
            element.send_keys(Keys.DELETE)
            time.sleep(0.3)
            element.send_keys(contents)

    def select_element(self, by, locator, select_type, select_value):
        select_box = Select(self.driver.find_element(by, locator))
        if select_type == "value":
            select_box.select_by_value(select_value)
        elif select_type == "text":
            select_box.select_by_visible_text(select_value)
        time.sleep(0.3)

    def is_checked(self, by, locator):
        return self.find_web_element(by, locator).is_selected()

    def wait_element(self, by, locator):
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((by, locator)))
            return True
        except TimeoutException:
            self.web_log("Element does not appear.")
            return False

    def accept_alert(self):
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = Alert(self.driver)
        alert.accept()

    def quit_driver(self):
        self.driver.quit()
