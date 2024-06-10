# configure_videopresets.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ConfigureVideopresetElements, MainMenuElements
import time


class ConfigureVideopreset(WebDriverSetup):
    def __init__(self):
        self.videopreset_elements = ConfigureVideopresetElements()

    def access_configure_videopresets(self):
        try:
            self.click(By.XPATH, MainMenuElements().configure)
            self.click(By.XPATH, MainMenuElements().configure_video_presets)
            time.sleep(1)
        except Exception as e:
            self.error_log(f"An error occurred while accessing the vdieo preset configuration page  | {repr(e)}")
            return False

    def configure_videopreset(self, preset_name, videopreset_options=None):
        try:
            self.access_configure_videopresets()

            if not self.find_exist_videopreset(preset_name):
                self.step_log(f"Video Preset Creation")
                self.click(By.CSS_SELECTOR, self.videopreset_elements.videopreset_add_button)
                self.input_box(
                    By.CSS_SELECTOR,
                    self.videopreset_elements.videopreset_name,
                    preset_name,
                )
            else:
                self.step_log(f"Video Preset Modification")
            # Codec
            # H.264/AVC | H.265/HEVC
            select_relevant_keys = ["Codec", "Encoding engine", "Resolution", "H.264 Profile"]
            input_relevant_keys = ["I-Frame Interval", "Bitrate", "Frame Rate", "Buffering Time"]

            for key, value in videopreset_options.items():
                element_selector = getattr(
                    self.videopreset_elements,
                    (
                        f"videopreset_{''.join(key.replace(' ', '_').replace('.', '').replace('-', '_').lower())}"
                        if "-" in key or "." in key
                        else f"videopreset_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )
                self.option_log(f"{key} : {value}")

                if any(keyword in key for keyword in select_relevant_keys):
                    self.drop_down(By.CSS_SELECTOR, element_selector, "text", value)
                elif any(keyword in key for keyword in input_relevant_keys):
                    self.input_box(By.CSS_SELECTOR, element_selector, value)

            self.input_box(By.CSS_SELECTOR, self.videopreset_elements.videopreset_bframe, "2")
            self.click(By.CSS_SELECTOR, self.videopreset_elements.videopreset_save_button)
            return True
        except Exception as e:
            self.error_log(f"Video preset setting error | {repr(e)}")
            return False

    def find_exist_videopreset(self, videopreset_name):
        try:
            videopreset_table = self.find_element(By.XPATH, ConfigureVideopresetElements().videopreset_table)

            for tr in videopreset_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                if column_value == videopreset_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True
            return False
        except Exception as e:
            self.error_log(f"Not found exist video preset | {repr(e)}")
            return False
