# configure_channels.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    TimeoutException,
)
from webdriver_method import WebDriverMethod
from web_elements import ConfigureChannelElements, MainMenuElements
from configure_roles import ConfigureRole
from configure_input import ConfigureInput
from configure_backup_source import ConfigureBackupSource
from configure_output import ConfigureOutput
from web_elements import ConfigureInputElements
import time


class Configurechannel(ConfigureRole):
    def __init__(self):
        self.input_elements = ConfigureInputElements()
        self.channel_elements = ConfigureChannelElements()

    def navigate_to_configure_channels(self):
        try:
            # Navigate to the 'Configure channels' page
            self.click_element(By.XPATH, MainMenuElements().configure)
            self.click_element(By.XPATH, MainMenuElements().configure_channels)
            time.sleep(1)  # Wait for the 'CONFIGURE - Channel' page to load

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")

    def configure_channel(
        self,
        channel_name,
        input_type,
        output_type,
        backup_source_type=None,
        input_options=None,
        output_options=None,
        backup_source_options=None,
        profile_name=None,
    ):
        try:
            print("Channel settings")
            self.navigate_to_configure_channels()
            # Click the button to add a new channel or find an existing one

            if not self.find_exist_channel(channel_name):
                self.click_element(
                    By.CSS_SELECTOR, self.channel_elements.channel_add_button
                )
                # Wait for the time to move to the channel creation page.
            else:
                print("A channel with the same name exists.")

            configure_output = ConfigureOutput(
                output_type,
                profile_name["Videopreset Name"],
                profile_name["Audiopreset Name"],
            )

            output_functions = {
                "UDP/IP": configure_output.output_udp,
                "RTSP": configure_output.output_rtsp,
                "RTMP": configure_output.output_rtmp,
                "HLS": configure_output.output_hls,
            }

            if output_type in output_functions:
                output_functions[output_type](output_options)

            time.sleep(1)

            self.input_text(
                By.CSS_SELECTOR, self.channel_elements.channel_name, channel_name
            )

            configure_input = ConfigureInput(input_type)

            input_functions = {
                "UDP/IP": configure_input.input_udp,
                "RTP/RTSP": configure_input.input_rtsp,
                "RTMP": configure_input.input_rtmp,
                "HTTP/HLS": configure_input.input_hls,
                "SDI": configure_input.input_sdi,
                "Playlist": configure_input.input_playlist,
                "SMPTE ST 2110": configure_input.input_smpte_st_2110,
                "NDI": configure_input.input_ndi,
            }

            if input_type in input_functions:
                input_functions[input_type](input_options)
                time.sleep(1)

            self.click_element(
                By.CSS_SELECTOR, self.channel_elements.channel_save_button
            )

            try:
                error_message = self.find_web_element(
                    By.CSS_SELECTOR, self.input_elements.input_common_error_message
                ).get_attribute("innerText")
                if error_message == "The Channel must have at least one Output.":
                    print(error_message)
                    print(
                        "The test ends because no output is generated and the channel cannot be created."
                    )
                    self.quit_driver()

            except (
                NoSuchElementException,
                ElementNotVisibleException,
                TimeoutException,
            ) as e:
                print(f"Error: {e}")

            # Entered when there is a backup source option.
            # Return to the channel menu to set the backup source and additional options.
            if not backup_source_type == None:
                configure_backup_source = ConfigureBackupSource(backup_source_type)
                self.navigate_to_configure_channels()
                time.sleep(1)
                self.find_exist_channel(channel_name)

                backup_source_functions = {
                    "UDP/IP": configure_backup_source.backup_source_udp,
                    "RTP/RTSP": configure_backup_source.backup_source_rtp,
                    "RTMP": configure_backup_source.backup_source_rtmp,
                    "HTTP/HLS": configure_backup_source.backup_source_hls,
                    "SDI": configure_backup_source.backup_source_sdi,
                    "Playlist": configure_backup_source.backup_source_playlist,
                    "SMPTE ST 2110": configure_backup_source.backup_source_smpte_st_2110,
                    "NDI": configure_backup_source.backup_source_ndi,
                }

                if backup_source_type in backup_source_functions:
                    backup_source_functions[backup_source_type](backup_source_options)
                    time.sleep(1)

                # Save backup source options.
                self.click_element(
                    By.CSS_SELECTOR, self.channel_elements.channel_save_button
                )
            print("Channel setting complete")

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")

    def find_exist_channel(self, channel_name):
        try:
            channel_table = self.find_web_element(
                By.XPATH, self.channel_elements.channel_table
            )

            for tr in channel_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute(
                    "innerText"
                )
                if column_value == channel_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    time.sleep(0.5)
                    return True  # channel found and clicked
            return False  # channel not found

        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False
