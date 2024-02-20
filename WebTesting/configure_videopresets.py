# configure_videopresets.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException
from webdriver_method import WebDriverMethod
from web_elements import ConfigureVideopresetElements, MainMenuElements
import time


class ConfigureVideopreset(WebDriverMethod):
    def __init__(self):
        self.videopreset_elements = ConfigureVideopresetElements()

    def navigate_to_configure_videopresets(self):
        try:
            # Navigate to the 'Configure videopresets' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(
                By.XPATH, MainMenuElements().configure_video_presets)
            # Wait for the 'CONFIGURE - Videopreset' page to load
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def configure_videopreset(self, profile_name, videopreset_options=None):
        try:
            print('Video Profile Settings')
            self.navigate_to_configure_videopresets()

            # Click the button to add a new videopreset or find an existing one
            if not self.find_exist_videopreset(profile_name):
                self.click_element(
                    By.CSS_SELECTOR, self.videopreset_elements.videopreset_add_button)
                # Wait for the time to move to the videopreset creation page.
                time.sleep(1)
                # Since there is no existing videopreset with the same name, a videopreset is created with that name.
                self.input_text(By.CSS_SELECTOR,
                                self.videopreset_elements.videopreset_name, profile_name)
            else:
                print('A videopreset with the same name exists.')
            # Codec
            # H.264/AVC | H.265/HEVC
            select_relevant_keys = ['Codec', 'Encoding engine', 'Resolution']
            input_relevant_keys = ['Bitrate', 'Frame Rate',
                                   'I-Frame Interval', 'Buffering Time']

            for key, value in videopreset_options.items():
                print(f"  ㆍ{key} : {value}")
                element_selector = getattr(
                    self.videopreset_elements, f"videopreset_{''.join(key.replace(' ', '_').lower().split('-'))}" if '-' in key else f"videopreset_{key.replace(' ', '_').lower()}", None)
                if any(keyword in key for keyword in select_relevant_keys):
                    self.select_element(
                        By.CSS_SELECTOR, element_selector, 'text', value)
                elif any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR, element_selector, value)

            self.input_text(By.CSS_SELECTOR,
                            self.videopreset_elements.videopreset_bframe, '2')
            self.click_element(
                By.CSS_SELECTOR, self.videopreset_elements.videopreset_save_button)
            # Wait for a moment before continuing
            print('Videopreset setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def find_exist_videopreset(self, videopreset_name):
        try:
            videopreset_table = self.find_web_element(
                By.XPATH, ConfigureVideopresetElements().videopreset_table)

            for tr in videopreset_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, 'td')[
                    0].get_attribute('innerText')
                if column_value == videopreset_name:
                    tr.find_elements(By.TAG_NAME, 'td')[0].click()
                    return True  # Videopreset found and clicked
            return False  # Videopreset not found
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False
