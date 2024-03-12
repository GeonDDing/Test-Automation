# webdriver_init.py
import os
import configparser
from selenium.webdriver.chrome.options import Options


class WebDriverInit:
    def __init__(self):
        try:
            current_directory = os.path.dirname(os.path.realpath(__file__))  # 현재 경로만 추출
            config_path = os.path.join(current_directory, "config.ini")  # 현재 경로에서 config.ini 찾음
            self.config = configparser.ConfigParser()  # config.ini 파싱
            self.config.read(config_path)  # config.ini 파싱 후 일기

        except Exception as e:
            print(e)

        webdriver_options = self.config.items("WebDriverOptions")
        self.options = Options()

        for option_key, option_value in webdriver_options:
            # Replace underscores with dashes for compatibility
            option_key = option_key.replace("_", "-")
            option_argument = f"--{option_key}={option_value}"
            self.options.add_argument(option_argument)

        self.url = self.config.get("Webpage", "url")
