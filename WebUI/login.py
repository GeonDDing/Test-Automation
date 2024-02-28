# login.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    TimeoutException,
)
from webdriver_method import WebDriverMethod
from web_elements import LoginElements
import logging


class Login(WebDriverMethod):
    def login(self, username, password):
        # Open Page
        self.driver.get(self.url)
        try:
            # Input username
            self.input_text(By.CSS_SELECTOR, LoginElements.login, username)
            # Input password
            self.input_text(By.CSS_SELECTOR, LoginElements.password, password)
            # Click login button
            self.click_element(By.CSS_SELECTOR, LoginElements.login_button)
            if self.driver.current_url == "http://10.1.0.145/hms/index.php":
                logging.info("Login 성공")
                print("로그인 정보")
                print(f"  ㆍID : {username}")
                print(f"  ㆍPW : {password}")
                return True, None
            else:
                logging.error("Login 실패")
                print("로그인 실패")
                return False, "Login Failed"

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")
            logging.error((f"Error: {e}"))
            return False, e


class Logout(WebDriverMethod):
    def logout(self):
        pass


if __name__ == "__main__":
    test = Login()
    print(test.login("admin", "admin1"))
