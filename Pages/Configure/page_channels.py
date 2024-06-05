# configure_channels.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import (
    ConfigureChannelElements,
    MainMenuElements,
    ChannelsInputElements,
    ChannelsBackupSourceElements,
)
from Pages.Configure.page_channels_backup_source import ChannelsBackupSource
from Pages.Configure.page_channels_input import ChannelsInput
from Pages.Configure.page_channels_output import ChannelsOutput
import xml.etree.ElementTree as elementTree
import time
import requests


class ConfigureChannel(WebDriverSetup):
    def __init__(self, **kwagrs):
        super().__init__()
        self.input_elements = ChannelsInputElements()
        self.backup_source_elements = ChannelsBackupSourceElements()
        self.channel_elements = ConfigureChannelElements()
        self.channel_configure_data = kwagrs

    def access_configure_channels(self):
        try:
            self.click(By.XPATH, MainMenuElements().configure)
            self.click(By.XPATH, MainMenuElements().configure_channels)
            time.sleep(1)
        except Exception as e:
            self.error_log(f"An error occurred while accessing the channel configuration page | {repr(e)}")
            return False

    def pre_channel_configuration(self):
        self.page_implicitly_wait()
        try:
            self.access_configure_channels()
            if not self.find_exist_channel():
                self.click(By.CSS_SELECTOR, self.channel_elements.channel_add_button)
                self.step_log(f"Channel(Input, Backup Source, Output) Creation")
            else:
                self.step_log(f"Channel(Input, Backup Source, Output) Modification")
            self.info_log(f"Channel : {self.channel_configure_data['Channel Name']}")
            return True
        except Exception as e:
            self.error_log(f"Pre channel configuration setting error | {repr(e)}")
            return False

    def post_channel_configuration(self):
        self.page_implicitly_wait()
        try:
            self.input_box(
                By.CSS_SELECTOR, self.channel_elements.channel_name, self.channel_configure_data["Channel Name"]
            )
            self.click(By.CSS_SELECTOR, self.channel_elements.channel_save_button)
            error_message = self.find_element(
                By.CSS_SELECTOR, self.input_elements.input_common_error_message
            ).get_attribute("innerText")

            if error_message == "At least one Output is required. The test stops because the channel fails.":
                self.error_log(error_message)
                self.quit_driver()
                return False
            else:
                return True
        except Exception as e:
            self.error_log(f"Post channel configuration setting error | {repr(e)}")
            return False

    def setup_input(self):
        setup_input_return = bool()
        try:
            configure_input = ChannelsInput(self.channel_configure_data["Input Type"])
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
                setup_input_return = input_functions[self.channel_configure_data["Input Type"]](
                    self.channel_configure_data["Input Options"]
                )
                configure_input.input_common(self.channel_configure_data["Common Options"])
                return setup_input_return
        except Exception as e:
            self.error_log(f"Input configuration setting error | {repr(e)}")
            return False

    def setup_backups_source(self):
        try:
            setup_backupsource_return = bool()
            if not self.channel_configure_data["Backup Source Type"] == None:
                self.access_configure_channels()
                self.find_exist_channel()
                configure_backup_source = ChannelsBackupSource(self.channel_configure_data["Backup Source Type"])
                backup_source_functions = {
                    "UDP": configure_backup_source.backup_source_udp,
                    "RTP": configure_backup_source.backup_source_rtsp,
                    "RTSP": configure_backup_source.backup_source_rtsp,
                    "RTMP": configure_backup_source.backup_source_rtmp,
                    "HTTP": configure_backup_source.backup_source_hls,
                    "HLS": configure_backup_source.backup_source_hls,
                    "SDI": configure_backup_source.backup_source_sdi,
                    "Playlist": configure_backup_source.backup_source_playlist,
                    "SMPTE ST 2110": configure_backup_source.backup_source_smpte_st_2110,
                    "NDI": configure_backup_source.backup_source_ndi,
                }
                if self.channel_configure_data["Backup Source Type"] in backup_source_functions:
                    setup_backupsource_return = backup_source_functions[
                        self.channel_configure_data["Backup Source Type"]
                    ](self.channel_configure_data["Backup Source Options"])
                self.click(By.CSS_SELECTOR, self.channel_elements.channel_save_button)
            return setup_backupsource_return
        except Exception as e:
            self.error_log(f"Failed to enter channel edit page | {repr(e)}")
            return False

    def setup_output(self):
        try:
            configure_output = ChannelsOutput(
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
            self.error_log(f"Output configuration setting error | {repr(e)}")
            return False

    def switch_backup_source(self, chidx):
        try:
            self.step_log(f"Switching Backup Source")
            self.click(By.CSS_SELECTOR, self.backup_source_elements.backup_source_switch_source_button.format(chidx))
            self.accept_alert()
            time.sleep(10)
            # stats xml 에서 'sourceLayer' 가 2인 경우 Backup source 로 전환 성공, 0이면 Primary source
            switch_req = requests.get(self.url + f":900{chidx}/stats")
            root = elementTree.fromstring(switch_req.text)
            if root.find("sourceLayer").text == "2":
                return True
            else:
                self.error_log("Failed to switching backup source")
                return False
        except Exception as e:
            self.error_log(f"Not found backup source switch button | {repr(e)}")
            return False

    def find_exist_channel(self):
        try:
            channel_table = self.find_element(By.XPATH, self.channel_elements.channel_table)
            for tr in channel_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                if column_value == self.channel_configure_data["Channel Name"]:
                    tr.find_elements(By.TAG_NAME, "td")[0].click()
                    time.sleep(0.5)
                    return True
            return False
        except Exception as e:
            self.error_log(f"Not found exist channel | {repr(e)}")
            return False
