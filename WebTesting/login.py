# login.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException
from webdriver_method import WebDriverMethod
from web_elements import LoginElements
import time


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

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")


class Logout(WebDriverMethod):
    def logout(self):
        pass


if __name__ == '__main__':
    test = Login()
    test.login('admin', 'admin')
