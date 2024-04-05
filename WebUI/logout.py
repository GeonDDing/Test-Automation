# login.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import LogoutElements
import time


class Logout(WebDriverMethod):
    def logout(self):
        try:
            self.step_log(f"Web Logout")
            self.click_element(By.CSS_SELECTOR, LogoutElements.logout_button)
            time.sleep(2)
            if self.driver.current_url == f"{self.url}/hms/login.php":
                return True
            else:
                return False

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            if self.driver.current_url == f"{self.url}/hms/login.php":
                return True
            else:
                self.error_log(f"Logout failed error {e}")
                return False
