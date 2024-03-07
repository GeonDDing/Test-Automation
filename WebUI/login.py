# login.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import LoginElements


class Login(WebDriverMethod):
    def login(self, username, password):
        # Open Page
        self.driver.get(self.url)
        try:
            print("\n- Management Web 로그인")
            # Input username
            print(f"  ㆍID : {username}")
            self.input_text(By.CSS_SELECTOR, LoginElements.login, username)
            # Input password
            print(f"  ㆍPW : {password}")
            self.input_text(By.CSS_SELECTOR, LoginElements.password, password)
            # Click login button
            self.click_element(By.CSS_SELECTOR, LoginElements.login_button)

            if self.driver.current_url == "http://10.1.0.145/hms/index.php":
                return True
            else:
                return False

        except (NoSuchElementException, ElementNotVisibleException) as e:
            print(f"Error: {e}")
            return False


class Logout(WebDriverMethod):
    def logout(self):
        pass


if __name__ == "__main__":
    test = Login()
    print(test.login("admin", "admin1"))
