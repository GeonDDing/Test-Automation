# configure_audiopresets.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import ConfigureAudiopresetElements, MainMenuElements
import time


class ConfigureAudiopreset(WebDriverMethod):
    def __init__(self):
        self.audiopreset_elements = ConfigureAudiopresetElements()

    def access_configure_audiopresets(self):
        try:
            # Navigate to the 'Configure audiopresets' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(By.XPATH, MainMenuElements().configure_audio_presets)
            # Wait for the 'CONFIGURE - Audiopreset' page to load
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(f"An error occurred while accessing the audio preset configuration page  {e}")

    def configure_audiopreset(self, preset_name, audiopreset_options=None):
        try:
            self.access_configure_audiopresets()
            # Click the button to add a new audiopreset or find an existing one
            if not self.find_exist_audiopreset(preset_name):
                self.step_log(f"Audio Preset Creation")
                self.click_element(By.CSS_SELECTOR, self.audiopreset_elements.audiopreset_add_button)
                # Wait for the time to move to the audiopreset creation page.
                time.sleep(1)
                # Since there is no existing audiopreset with the same name, a audiopreset is created with that name.
                self.input_text(
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
                    self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                elif "Evolution Framework" == key:
                    self.click_element(By.CSS_SELECTOR, element_selector)
                else:
                    self.input_text(By.CSS_SELECTOR, element_selector, value)

            # Save audiopreset settings
            self.click_element(By.CSS_SELECTOR, self.audiopreset_elements.audiopreset_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(f"Audio preset setting error {e}")
            return False

    def find_exist_audiopreset(self, audiopreset_name):
        try:
            audiopreset_table = self.find_web_element(By.XPATH, ConfigureAudiopresetElements().audiopreset_table)

            for tr in audiopreset_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                if column_value == audiopreset_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    return True  # audiopreset found and clicked

            return False  # audiopreset not found

        except NoSuchElementException as e:
            self.error_log(f"Not found exist audio preset {e}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False
