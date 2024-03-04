# configure_channels.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    TimeoutException,
)
from web_elements import ConfigureChannelElements, MainMenuElements
from configure_roles import ConfigureRole
from configure_input import ConfigureInput
from configure_backup_source import ConfigureBackupSource
from configure_output import ConfigureOutput
from web_elements import ConfigureInputElements
import time


class ConfigureChannel(ConfigureRole):
    def __init__(
        self,
        channel_name,
        input_type,
        output_type,
        backup_source_type,
        input_options,
        output_options,
        backup_source_options,
        preset_name,
    ):
        self.input_elements = ConfigureInputElements()
        self.channel_elements = ConfigureChannelElements()
        self.channel_name = channel_name
        self.input_type = input_type
        self.input_options = input_options
        self.backup_source_type = backup_source_type
        self.backup_source_options = backup_source_options
        self.output_type = output_type
        self.output_options = output_options
        self.preset_name = preset_name

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
            return False

    def pre_channel_configuration(self):
        try:
            self.navigate_to_configure_channels()
            # Click the button to add a new channel or find an existing one

            if not self.find_exist_channel():
                self.click_element(
                    By.CSS_SELECTOR, self.channel_elements.channel_add_button
                )
                # Wait for the time to move to the channel creation page.
                print("- Channel(Input, Backup Source, Output) 생성")
            else:
                print("- Channel(Input, Backup Source, Output) 수정")

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")
            return False

    def post_channel_configuration(self):
        try:
            self.input_text(
                By.CSS_SELECTOR, self.channel_elements.channel_name, self.channel_name
            )
            time.sleep(1)
            self.click_element(
                By.CSS_SELECTOR, self.channel_elements.channel_save_button
            )

            try:
                error_message = self.find_web_element(
                    By.CSS_SELECTOR, self.input_elements.input_common_error_message
                ).get_attribute("innerText")
                if (
                    error_message
                    == "최소 하나의 Output이 필요합니다. 채널을 생성하지 못하여 테스트를 종료합니다."
                ):
                    print(error_message)
                    self.quit_driver()
                    return False
                else:
                    return True

            except (
                NoSuchElementException,
                ElementNotVisibleException,
                TimeoutException,
            ) as e:
                print(f"Error: {e}")
                return False

        except (
            NoSuchElementException,
            ElementNotVisibleException,
            TimeoutException,
        ) as e:
            print(f"Error: {e}")
            return False

    def setup_input(self):
        try:
            configure_input = ConfigureInput(self.input_type)
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

            if self.input_type in input_functions:
                return input_functions[self.input_type](self.input_options)

        except Exception as e:
            return False

    def setup_backups_source(self):
        try:
            set_backupsource_result = bool()
            if not self.backup_source_type == None:
                configure_backup_source = ConfigureBackupSource(self.ackup_source_type)
                self.navigate_to_configure_channels()
                time.sleep(1)
                self.find_exist_channel()

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

                if self.backup_source_type in backup_source_functions:
                    set_backupsource_result = backup_source_functions[
                        self.backup_source_type
                    ](self.backup_source_options)
                    time.sleep(1)

                # Save backup source options.
                self.click_element(
                    By.CSS_SELECTOR, self.channel_elements.channel_save_button
                )
            return set_backupsource_result

        except Exception as e:
            return False

    def setup_output(self):
        try:
            configure_output = ConfigureOutput(
                self.output_type,
                self.preset_name["Videopreset Name"],
                self.preset_name["Audiopreset Name"],
            )
            output_functions = {
                "UDP/IP": configure_output.output_udp,
                "RTSP": configure_output.output_rtsp,
                "RTMP": configure_output.output_rtmp,
                "HLS": configure_output.output_hls,
            }

            if self.output_type in output_functions:
                return output_functions[self.output_type](self.output_options)

        except Exception as e:
            return False

    def find_exist_channel(self):
        try:
            channel_table = self.find_web_element(
                By.XPATH, self.channel_elements.channel_table
            )

            for tr in channel_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute(
                    "innerText"
                )
                if column_value == self.channel_name:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    time.sleep(0.5)
                    return True  # channel found and clicked
            return False  # channel not found

        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False
