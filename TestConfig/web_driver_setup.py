# webdriver_method.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

from TestConfig.web_log import WebLog
import time, platform, os, configparser


class WebDriverInit:
    def __init__(self):
        self.base_url_parser()
        webdriver_options = self.config.items("WebDriverOptions")
        self.options = Options()

        for option_key, option_value in webdriver_options:
            # Config.ini 퍼알 에 있는 옵션에서 '_' 를 '-' 로 변환
            option_key = option_key.replace("_", "-")
            option_argument = f"--{option_key}={option_value}"
            self.options.add_argument(option_argument)

        self.url = self.config.get("Webpage", "url")

    def base_url_parser(self):
        try:
            current_directory = os.path.dirname(os.path.realpath(__file__))  # 현재 경로
            config_path = os.path.join(current_directory, "config.ini")  # 현재 경로에서 config.ini 파일 찾음
            self.config = configparser.ConfigParser()  # config.ini 파일 내용 파싱
            self.config.read(config_path)  # config.ini 파일 내용 파싱 후 읽기
            return self.config.get("Webpage", "url")
        except Exception as e:
            print(e)


class WebDriverSetup(WebDriverInit, WebLog):
    if platform.system() == "Darwin" and platform.system() == "Windows":
        driver = webdriver.Chrome(options=WebDriverInit().options)
        driver.set_window_position(540, 0)
        driver.set_window_size(1280, 1920)
    else:
        driver = webdriver.Chrome(options=WebDriverInit().options)
        driver.set_window_size(1280, 2160)

    def find_element(self, by, locator):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, locator)))
            return self.driver.find_element(by, locator)
        except Exception as e:
            return None

    def click(self, by, locator):
        self.find_element(by, locator).click()
        time.sleep(0.5)

    def input_box(self, by, locator, contents):
        # MAC OS 환경
        if platform.system() == "Darwin":
            element = self.find_element(by, locator)
            element.send_keys(Keys.COMMAND + "A")
            time.sleep(0.3)
            element.send_keys(Keys.DELETE)
            time.sleep(0.3)
            element.send_keys(contents)
        # Windows 또는 Linux 환경
        else:
            element = self.find_element(by, locator)
            element.send_keys(Keys.CONTROL + "A")
            time.sleep(0.3)
            element.send_keys(Keys.DELETE)
            time.sleep(0.3)
            element.send_keys(contents)

    def select_box(self, by, locator, select_type, select_value):
        # select_box = Select(self.driver.find_element(by, locator))
        select_box = Select(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, locator))))
        if select_type == "value":
            select_box.select_by_value(select_value)
        elif select_type == "text":
            select_box.select_by_visible_text(select_value)

    # def is_element_displayed(self, locator):

    def is_checked(self, by, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, locator))).is_selected()

    def is_displayed(self, by, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, locator))).is_displayed()

    def wait_element(self, by, locator):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, locator)))
            return True
        except Exception as e:
            self.warning_log("Element does not appear. %s" % repr(e))
            return False

    def clickable_click(self, by, locator):
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((by, locator))).click()

    def accept_alert(self):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = Alert(self.driver)
        alert.accept()

    def quit_driver(self):
        self.driver.quit()

    def close_driver(self):
        self.driver.close()
