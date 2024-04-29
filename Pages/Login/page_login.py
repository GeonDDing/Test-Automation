# Login.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import LoginElements


class Login(WebDriverSetup):
    def login(self, username, password):
        print("test login")
        try:
            # 1. 로그인 페이지 진입
            self.driver.get(self.url)
            # 2. 유요한 아이디 입력
            self.input_box(By.CSS_SELECTOR, LoginElements.login, username)
            # 유요한 비밀번호 입력
            self.input_box(By.CSS_SELECTOR, LoginElements.password, password)
            # 로그인 버튼 클릭
            self.click(By.CSS_SELECTOR, LoginElements.login_button)
            if self.driver.current_url == f"{self.url}/hms/index.php":
                print("True !!!")
                return True
        except Exception as e:
            print("Failed to compile login, exception is %s" % repr(e))
            return False


if __name__ == "__main__":
    test = Login()
    test.login("amdin", "admin")
