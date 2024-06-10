# page_audiopresets.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ConfigureAudiopresetElements, MainMenuElements
import time


class ConfigureAudiopreset(WebDriverSetup):
    def __init__(self):
        self.audiopreset_elements = ConfigureAudiopresetElements()

    def access_configure_audiopresets(self):
        try:
            self.click(By.XPATH, MainMenuElements().configure)
            self.click(By.XPATH, MainMenuElements().configure_audio_presets)
            time.sleep(1)
        except Exception as e:
            self.error_log(f"An error occurred while accessing the audio preset configuration page | {repr(e)}")

    def configure_audiopreset(self, preset_name, audiopreset_options=None):
        try:
            self.access_configure_audiopresets()
            if not self.find_exist_audiopreset(preset_name):
                self.step_log(f"Audio Preset Creation")
                self.click(By.CSS_SELECTOR, self.audiopreset_elements.audiopreset_add_button)
                self.input_box(
                    By.CSS_SELECTOR,
                    self.audiopreset_elements.audiopreset_name,
                    preset_name,
                )
            else:
                self.step_log(f"Audio Preset Modification")
            # Codec
            # H.264/AVC | H.265/HEVC
            select_relevant_keys = [
                "Codec",
                "MPEG version",
                "Profile",
                "Channels",
                "Sampling Rate",
                "Bitrate",
            ]
            for key, value in audiopreset_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.audiopreset_elements,
                    (
                        f"audiopreset_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"audiopreset_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )
                if any(keyword in key for keyword in select_relevant_keys):
                    self.drop_down(By.CSS_SELECTOR, element_selector, "text", value)
                elif "Evolution Framework" == key:
                    self.click(By.CSS_SELECTOR, element_selector)
                else:
                    self.input_box(By.CSS_SELECTOR, element_selector, value)
            self.click(By.CSS_SELECTOR, self.audiopreset_elements.audiopreset_save_button)
            return True

        except Exception as e:
            self.error_log(f"Audio preset setting error | {repr(e)}")
            return False

    def find_exist_audiopreset(self, audiopreset_name):
        try:
            audiopreset_table = self.find_element(By.XPATH, ConfigureAudiopresetElements().audiopreset_table)
            for tr in audiopreset_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                if column_value == audiopreset_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True
            return False
        except Exception as e:
            self.error_log(f"Not found exist audio preset | {repr(e)}")
            return False
