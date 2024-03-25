# configure_channels.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotVisibleException,
)
from webdriver_method import WebDriverMethod
from web_elements import ConfigureInputElements
import time


class ConfigureInput(WebDriverMethod):
    def __init__(self, input_type):
        self.input_elements = ConfigureInputElements()
        try:
            if "UDP" == input_type:
                input_type = "UDP/IP"
            elif "RTP" == input_type or "RTSP" == input_type:
                input_type = "RTP/RTSP"
            elif "HTTP" == input_type or "HLS" == input_type:
                input_type = "HTTP/HLS"
            self.select_element(By.CSS_SELECTOR, self.input_elements.input_type, "text", input_type)

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def input_udp(self, input_options):
        program_selection_mode_flag = bool()
        input_relevant_keys = [
            "Network URL",
            "SSM host",
            "Max input Mbps",
            "Program Number",
            "Service Name",
            "Video ID",
            "Audio ID",
        ]
        select_relevant_keys = ["Interface", "Enable HA Mode", "Program Selection Mode"]
        try:
            self.sub_step_log(f"Create UDP/IP Input")

            for key, value in input_options.items():
                if isinstance(value, dict):
                    self.option_log(f"{key} : {str(value)[1:-1]}")
                else:
                    self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.input_elements,
                    (
                        f"input_udp_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"input_udp_{key.lower().replace(' ', '_')}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in select_relevant_keys):
                    if "Program Selection Mode" in key:
                        # mode = self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                        self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                        program_selection_mode_flag = True
                        try:
                            self.accept_alert()
                            time.sleep(1)
                            self.input_text(
                                By.CSS_SELECTOR,
                                self.input_elements.input_common_analysis_window,
                                "6000",
                            )
                            time.sleep(1)
                        except:
                            pass
                    else:
                        self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                # elif any(keyword in key for keyword in input_relevant_keys):
                if any(keyword in key for keyword in input_relevant_keys):
                    if key == "Audio ID" and isinstance(input_options["Audio ID"], dict):
                        for index, sub_value in enumerate(value.values()):
                            if index == 0:
                                self.input_text(By.CSS_SELECTOR, element_selector, sub_value)
                            else:
                                self.input_text(
                                    By.CSS_SELECTOR,
                                    self.input_elements.input_udp_audio_id_extend.format(index, index),
                                    sub_value,
                                )
                                # Audio ID 입력후 어딘가 클릭해야 다음 ID 입력란이 생성 되기 때문에 Input 백그라운드를 클릭하도록 함
                                self.click_element(By.XPATH, '//*[@id="editform"]/div[1]/div[3]')
                                time.sleep(0.3)
                    else:
                        if key in ["Program Number", "Service Name"]:
                            if program_selection_mode_flag:
                                self.input_text(By.CSS_SELECTOR, element_selector, value)
                        else:
                            self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    if isinstance(value, bool) and value:
                        self.click_element(By.CSS_SELECTOR, element_selector)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def input_rtsp(self, input_options):
        try:
            self.sub_step_log(f"Create RTP/RTSP Input")
            for key, value in input_options.items():
                self.option_log(f"{key} : {value}")
                if key == "SDP File":
                    self.input_text(By.CSS_SELECTOR, self.input_elements.input_rtp_sdp_file, value)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def input_rtmp(self, input_options):
        try:
            self.sub_step_log(f"Create RTMP Input")
            for key, value in input_options.items():
                self.option_log(f"{key} : {value}")
                if key == "URL":
                    self.input_text(By.CSS_SELECTOR, self.input_elements.input_rtmp_url, value)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def input_hls(self, input_options):
        try:
            self.info_log("Create HLS Input")
            for key, value in input_options.items():
                self.option_log(f"{key} : {value}")
                if key == "URL":
                    self.input_text(By.CSS_SELECTOR, self.input_elements.input_hls_url, value)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def input_sdi(self, input_options):
        input_relevant_keys = ["Teletext page", "VBI lines"]
        try:
            self.sub_step_log(f"Create SDI Input")

            for key, value in input_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.input_elements,
                    (
                        f"input_sdi_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"input_sdi_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    self.select_element(By.CSS_SELECTOR, element_selector, "text", value)

            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def input_playlist(self, input_options):
        input_relevant_keys = ["URI", "Recurring the last N files"]
        try:
            self.info_log("Create Playlist Input")
            # playlist_type = input_options.get('Type')
            # self.select_element(
            #     By.CSS_SELECTOR, self.input_elements.input_playlist_type, 'text', playlist_type)

            for key, value in input_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.input_elements,
                    (
                        f"input_playlist_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"input_playlist_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                    if "Type" == key:
                        time.sleep(1)

            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def input_smpte_st_2110(self, input_options):
        input_relevant_keys = [
            "Video SDP URL",
            "Audio SDP URL",
            "Ancillary SDP URL",
            "Teletext page",
        ]
        try:
            self.sub_step_log(f"Create SMPTE ST 2110 Input")

            for key, value in input_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.input_elements,
                    (
                        f"input_smpte_st_2110_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"input_smpte_st_2110_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    self.select_element(By.CSS_SELECTOR, element_selector, "text", value)

            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def input_ndi(self, input_options):
        try:
            self.sub_step_log(f"Create NDI Input")

            for key, value in input_options.items():
                self.info_log(f"{key} : {value}")
                element_selector = getattr(
                    self.input_elements,
                    (
                        f"input_ndi_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"input_ndi_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )
                self.input_text(By.CSS_SELECTOR, element_selector, value)

            return True
        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False
