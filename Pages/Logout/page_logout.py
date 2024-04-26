# Logout.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import LogoutElements


class Logout(WebDriverSetup):
    def logout(self):
        try:
            # 1. 로그인 상태인지 페이지 확인
            if self.driver.current_url != f"{self.url}/hms/login.php":
                # 2.로그아웃 버튼 클릭
                self.click(By.CSS_SELECTOR, LogoutElements.logout_button)
                return True
            else:
                return False
        except Exception as e:
            print("Failed to compile logout, exception is %s" % repr(e))
            return False
