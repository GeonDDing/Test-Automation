# configure_role.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from configure_devices import ConfigureDevice
from web_elements import ConfigureRoleElements, MainMenuElements
import time


class ConfigureRole(ConfigureDevice):
    def __init__(self):
        self.role_elements = ConfigureRoleElements()

    def navigate_to_configure_roles(self):
        try:
            # Navigate to the 'Configure Roles' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(By.XPATH, MainMenuElements().configure_roles)
            time.sleep(1)  # Wait for the 'CONFIGURE Role' page to load

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def configure_role(self, role_name, *channel_name):
        try:
            self.navigate_to_configure_roles()

            # Click the button to add a new role or find an existing one
            if not self.find_exist_role(role_name):
                self.step_log(f"Role 생성")
                self.click_element(By.CSS_SELECTOR, self.role_elements.role_add_button)
                # Wait for the time to move to the group creation page.
                time.sleep(1)
                # Since there is no existing Role with the same name, a Role is created with that name.
                self.input_text(By.CSS_SELECTOR, self.role_elements.role_name, role_name)

                if channel_name:
                    for index, channel_value in enumerate(channel_name):
                        self.select_element(
                            By.XPATH,
                            self.role_elements.add_channel_list,
                            "text",
                            channel_value,
                        )
                        self.option_log(f"Channel : {channel_name[index]}")
            else:
                self.step_log(f"Role 수정")
                while True:
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, self.role_elements.role_remove_button))
                        )
                        self.click_element(By.CSS_SELECTOR, self.role_elements.role_remove_button)
                        time.sleep(0.5)
                    except:
                        break

                if channel_name:
                    for index, channel_value in enumerate(channel_name):
                        # selected_channel_list = f"//*[@id='channel{index}']"
                        self.select_element(By.XPATH, self.role_elements.add_channel_list, "text", channel_value)
                        self.option_log(f"Channel : {channel_name[index]} ")

            self.click_element(By.CSS_SELECTOR, self.role_elements.role_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def find_exist_role(self, role_name):
        try:
            role_table = self.find_web_element(By.XPATH, self.role_elements.role_table)

            for tr in role_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                if column_value == role_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True  # Role found and clicked

            return False  # Role not found

        except NoSuchElementException as e:
            self.error_log(e)
            # Handle the error as needed, for example, return False or raise the exception again
            return False
