# login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import LoginElements
import time


class Login(WebDriverMethod):
    def login(self, username, password):
        # Open Page
        self.driver.get(self.url)
        try:
            print("\n")
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, LoginElements.login))
                )
                self.step_log(f"Web Login")
                # Input username
                self.option_log(f"ID : {username}")
                self.input_text(By.CSS_SELECTOR, LoginElements.login, username)
                # Input password
                self.option_log(f"PW : {password}")
                self.input_text(By.CSS_SELECTOR, LoginElements.password, password)
                # Click login button
                self.click_element(By.CSS_SELECTOR, LoginElements.login_button)

                if (
                    self.driver.current_url == "http://10.1.0.145/hms/index.php"
                    or self.driver.current_url == "http://10.1.0.145/hms/index.php"
                ):
                    return True
                else:
                    return False
            except Exception as e:
                if (
                    self.driver.current_url == "http://10.1.0.145/hms/"
                    or self.driver.current_url == "http://10.1.0.145/hms/index.php"
                ):
                    return True
                else:
                    self.error_log(f"Login failed error {e}")
                    return False
        except Exception as e:
            if (
                self.driver.current_url == "http://10.1.0.145/hms/"
                or self.driver.current_url == "http://10.1.0.145/hms/index.php"
            ):
                return True
            else:
                self.error_log(f"Login failed error {e}")
                return False


if __name__ == "__main__":
    test = Login()
    print(test.login("admin", "admin1"))
