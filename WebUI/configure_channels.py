# configure_channels.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from web_elements import ConfigureChannelElements, MainMenuElements
from configure_roles import ConfigureRole
from configure_input import ConfigureInput
from configure_backup_source import ConfigureBackupSource
from configure_output import ConfigureOutput
from web_elements import ConfigureInputElements
import time


class ConfigureChannel(ConfigureRole):
    def __init__(self, **kwagrs):
        self.input_elements = ConfigureInputElements()
        self.channel_elements = ConfigureChannelElements()
        self.channel_configure_data = kwagrs

    def navigate_to_configure_channels(self):
        try:
            # Navigate to the 'Configure channels' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(By.XPATH, MainMenuElements().configure_channels)
            time.sleep(1)  # Wait for the 'CONFIGURE - Channel' page to load

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def pre_channel_configuration(self):
        try:
            self.navigate_to_configure_channels()
            # Click the button to add a new channel or find an existing one
            if not self.find_exist_channel():
                self.click_element(By.CSS_SELECTOR, self.channel_elements.channel_add_button)
                # Wait for the time to move to the channel creation page.
                self.step_log(f"Channel(Input, Backup Source, Output) Creation")
                self.info_log(f"Channel : {self.channel_configure_data['Channel Name']}")
            else:
                self.step_log(f"Channel(Input, Backup Source, Output) Modification")
                self.info_log(f"Channel : {self.channel_configure_data['Channel Name']}")

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def post_channel_configuration(self):
        try:
            self.input_text(
                By.CSS_SELECTOR, self.channel_elements.channel_name, self.channel_configure_data["Channel Name"]
            )
            time.sleep(1)
            self.click_element(By.CSS_SELECTOR, self.channel_elements.channel_save_button)
            error_message = self.find_web_element(
                By.CSS_SELECTOR, self.input_elements.input_common_error_message
            ).get_attribute("innerText")

            if error_message == "At least one Output is required. The test stops because the channel fails.":
                self.error_log(error_message)
                self.quit_driver()
                return False
            else:
                return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def setup_input(self):
        try:
            configure_input = ConfigureInput(self.channel_configure_data["Input Type"])
            input_functions = {
                "UDP": configure_input.input_udp,
                "RTP": configure_input.input_rtsp,
                "RTSP": configure_input.input_rtsp,
                "RTMP": configure_input.input_rtmp,
                "HTTP": configure_input.input_hls,
                "HLS": configure_input.input_hls,
                "SDI": configure_input.input_sdi,
                "Playlist": configure_input.input_playlist,
                "SMPTE ST 2110": configure_input.input_smpte_st_2110,
                "NDI": configure_input.input_ndi,
            }

            if self.channel_configure_data["Input Type"] in input_functions:
                return input_functions[self.channel_configure_data["Input Type"]](
                    self.channel_configure_data["Input Options"]
                )

        except Exception as e:
            return False

    def setup_backups_source(self):
        try:
            set_backupsource_result = bool()
            if not self.channel_configure_data["Backup Source Type"] == None:
                configure_backup_source = ConfigureBackupSource(self.channel_configure_data["Backup Source Type"])
                self.navigate_to_configure_channels()
                time.sleep(1)
                self.find_exist_channel()

                backup_source_functions = {
                    "UDP": configure_backup_source.backup_source_udp,
                    "RTP": configure_backup_source.backup_source_rtp,
                    "RTSP": configure_backup_source.backup_source_rtp,
                    "RTMP": configure_backup_source.backup_source_rtmp,
                    "HTTP": configure_backup_source.backup_source_hls,
                    "HLS": configure_backup_source.backup_source_hls,
                    "SDI": configure_backup_source.backup_source_sdi,
                    "Playlist": configure_backup_source.backup_source_playlist,
                    "SMPTE ST 2110": configure_backup_source.backup_source_smpte_st_2110,
                    "NDI": configure_backup_source.backup_source_ndi,
                }

                if self.channel_configure_data["Backup Source Type"] in backup_source_functions:
                    set_backupsource_result = backup_source_functions[
                        self.channel_configure_data["Backup Source Type"]
                    ](self.channel_configure_data["Backup Source Options"])

                    time.sleep(1)
                # Save backup source options.
                self.click_element(By.CSS_SELECTOR, self.channel_elements.channel_save_button)
            return set_backupsource_result

        except Exception as e:
            return False

    def setup_output(self):
        try:
            configure_output = ConfigureOutput(
                self.channel_configure_data["Output Type"],
                self.channel_configure_data["Preset Name"]["Videopreset Name"],
                self.channel_configure_data["Preset Name"]["Audiopreset Name"],
            )
            output_functions = {
                "UDP": configure_output.output_udp,
                "RTSP": configure_output.output_rtsp,
                "RTMP": configure_output.output_rtmp,
                "HLS": configure_output.output_hls,
            }

            if self.channel_configure_data["Output Type"] in output_functions:
                return output_functions[self.channel_configure_data["Output Type"]](
                    self.channel_configure_data["Output Options"]
                )

        except Exception as e:
            self.error_log(e)
            return False

    def find_exist_channel(self):
        try:
            channel_table = self.find_web_element(By.XPATH, self.channel_elements.channel_table)

            for tr in channel_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")

                if column_value == self.channel_configure_data["Channel Name"]:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    time.sleep(0.5)
                    return True  # channel found and clicked

            return False  # channel not found

        except NoSuchElementException as e:
            self.error_log(e)
            # Handle the error as needed, for example, return False or raise the exception again
            return False
