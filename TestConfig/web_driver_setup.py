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
        # webdriver_options = self.config.items("WebDriverOptions")
        self.options = Options()

        # for option_key, option_value in webdriver_options:
        #     # Config.ini 퍼알 에 있는 옵션에서 '_' 를 '-' 로 변환
        #     option_key = option_key.replace("_", "-")
        #     option_argument = f"--{option_key}={option_value}"
        #     self.options.add_argument(option_argument)
        self.options.add_argument("disable-gpu")
        self.options.add_argument("no_sandbox")
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])

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
    driver = webdriver.Chrome(options=WebDriverInit().options)
    if platform.system() == "Darwin":
        driver.set_window_position(540, 0)
        driver.set_window_size(1280, 1920)
    elif platform.system() == "Windows":
        driver.set_window_position(1400, 0)
        driver.set_window_size(1280, 1920)
    else:
        driver.set_window_size(1280, 2160)

    def find_element(self, by, locator):
        return self.driver.find_element(by, locator)

    def click(self, by, locator):
        self.find_element(by, locator).click()

    def input_box(self, by, locator, contents):
        element = self.find_element(by, locator)
        time.sleep(0.5)
        # MAC OS 환경
        if platform.system() == "Darwin":
            element.send_keys(Keys.COMMAND + "A")
        # Windows 또는 Linux 환경
        else:
            element.send_keys(Keys.CONTROL + "a")
        time.sleep(0.5)
        element.send_keys(Keys.DELETE)
        time.sleep(0.5)
        element.send_keys(contents)

    def input_box_no_clear(self, by, locator, contents):
        element = self.find_element(by, locator)
        element.click()
        time.sleep(0.5)
        element.send_keys(contents)

    def drop_down(self, by, locator, select_type, select_value):
        # drop_down = Select(self.driver.find_element(by, locator))
        drop_down = Select(self.driver.find_element(by, locator))
        time.sleep(1)
        if select_type == "value":
            drop_down.select_by_value(select_value)
        elif select_type == "text":
            drop_down.select_by_visible_text(select_value)
        elif select_type == "get_value":
            drop_down.first_selected_option.text

    def is_element_displayed(self, by, locator):
        return self.find_element(by, locator).value_of_css_property("display")

    def is_checked(self, by, locator):
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((by, locator))).is_selected()

    def is_displayed(self, by, locator):
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((by, locator))).is_displayed()

    def wait_element(self, by, locator):
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((by, locator)))
            return True
        except Exception as e:
            self.warning_log("Element does not appear. %s" % repr(e))
            return False

    def presence_click(self, by, locator):
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((by, locator))).click()
            return True
        except:
            return False

    def clickable_click(self, by, locator):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((by, locator))).click()
            return True
        except:
            return False

    def accept_alert(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = Alert(self.driver)
            alert.accept()
            return True
        except:
            return False

    def page_implicitly_wait(self):
        self.driver.implicitly_wait(10)

    def quit_driver(self):
        self.driver.quit()

    def close_driver(self):
        self.driver.close()
