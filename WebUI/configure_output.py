# configure_output.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    TimeoutException,
)
from webdriver_method import WebDriverMethod
from web_elements import ConfigureOutputElements
import time


class ConfigureOutput(WebDriverMethod):
    def __init__(self, output_type, videopreset_name, audiopreset_name):
        self.output_elements = ConfigureOutputElements()
        # Click output add button
        try:
            if not self.find_exist_output(output_type):
                self.click_element(By.CSS_SELECTOR, self.output_elements.output_add_output_button)
                # Wait for the time to move to the group creation page.
                time.sleep(1)
                # Since there is no existing Group with the same name, a Group is created with that name.
                if "UDP" in output_type:
                    output_type = "TS UDP/IP"

                self.select_element(
                    By.CSS_SELECTOR,
                    self.output_elements.output_type,
                    "text",
                    output_type,
                )
                self.click_element(By.CSS_SELECTOR, self.output_elements.output_create_button)
            self.select_stream_preset(videopreset_name, audiopreset_name)

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def find_exist_output(self, output_type):
        try:
            if "UDP" in output_type:
                output_type = "TS"

            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, self.output_elements.output_table))
                )
                output_table = self.find_web_element(By.XPATH, self.output_elements.output_table)

            except TimeoutException as e:
                return False

                self.quit_driver()

            for tr in output_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[3].get_attribute("innerText")

                if f"{output_type}:" in column_value:
                    tr.find_elements(By.TAG_NAME, "td")[3].click()
                    # self.option_log(f"{column_value}")
                    return True  # Output found and clicked

            return False  # Output not found

        except NoSuchElementException as e:
            self.error_log(e)
            # Handle the error as needed, for example, return False or raise the exception again
            return False

    def select_stream_preset(self, videopreset_name, audiopreset_name):
        try:
            self.sub_step_log(f"Select Video, Audio Profile")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_edit_stream))
            )
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            self.option_log(f"Videopreset : {videopreset_name}")
            self.select_element(
                By.CSS_SELECTOR,
                self.output_elements.output_video_profile,
                "text",
                videopreset_name,
            )
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream_save_button)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_add_stream_button))
                )
                self.click_element(By.CSS_SELECTOR, self.output_elements.output_add_stream_button)
                self.option_log(f"Audiopreset : {audiopreset_name}")
                if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_audio_profile):
                    self.select_element(
                        By.CSS_SELECTOR,
                        self.output_elements.output_audio_profile,
                        "text",
                        audiopreset_name,
                    )

            except:
                if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream):
                    self.click_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
                if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_audio_profile):
                    self.select_element(
                        By.CSS_SELECTOR,
                        self.output_elements.output_audio_profile,
                        "text",
                        audiopreset_name,
                    )
                    self.option_log(f"Audiopreset : {audiopreset_name}")

            self.click_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream_save_button)
            self.wait_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            return True

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException, AttributeError) as e:
            self.error_log(e)
            return False

    def output_udp(self, output_options):
        relevant_keys = [
            "Primary Network Interface",
            "Secondary Network Interface",
            "NULL packet padding",
        ]
        try:
            self.sub_step_log(f"Create UDP/IP Output")

            # Output option setting
            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.output_elements,
                    (
                        f"output_udp_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"output_udp_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in relevant_keys):
                    self.select_element(By.XPATH, element_selector, "text", value)
                elif "Broadcasting standard" in key:
                    broadcasting_standard_element = (
                        self.output_elements.output_udp_broadcasting_standard_atsc
                        if value == "ATSC"
                        else self.output_elements.output_udp_broadcasting_standard_dvb
                    )
                    self.click_element(By.CSS_SELECTOR, broadcasting_standard_element)
                elif "DVB-Subtitle-Track" in key:
                    self.click_element(By.XPATH, self.output_elements.output_udp_dvb_subtitle_track_checkbox)
                    time.sleep(1)
                    self.input_text(By.XPATH, element_selector, value)

                else:
                    if element_selector:
                        # fmt: off
                        if "DVB-Subtitle-Track" in key:
                            if not self.find_web_element(By.XPATH, self.output_elements.output_udp_dvb_subtitle_track_checkbox).get_attribute("checked"):
                                self.click_element(By.XPATH, self.output_elements.output_udp_dvb_subtitle_track_checkbox)
                        elif "DVB-Teletext-Track" in key:
                            if not self.find_web_element(By.XPATH, self.output_elements.output_udp_dvb_teletext_track_checkbox).get_attribute("checked"):
                                self.click_element(By.XPATH, self.output_elements.output_udp_dvb_teletext_track_checkbox)
                        # fmt: on
                        self.input_text(By.XPATH, element_selector, value)

            self.click_element(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def output_hls(self, output_options):
        click_relevant_keys = [
            "Keep remote segments",
            "Create Subfolder",
            "Create I-frame Playlists",
            "Tagging playlists with timestamp",
            "Enable ID3 TDEN tag",
            "Enable Encryption",
            'Append "ENDLIST" at Stop',
        ]
        try:
            self.sub_step_log(f"Create HLS Output")

            # Output option setting
            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.output_elements,
                    (
                        f"output_hls_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"output_hls_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if "Segment Naming" in key:
                    self.select_element(By.XPATH, element_selector, "text", value)
                elif "Subtitle Type" in key:
                    self.select_element(By.XPATH, element_selector, "text", value)
                    if "DVB-Subtitle" in key:
                        self.input_text(By.XPATH, element_selector, value)
                    if "DVB-Teletext" in key:
                        self.input_text(By.XPATH, element_selector, value)
                elif "SCTE-35 Signaling" in key:
                    self.select_element(By.XPATH, element_selector, "text", value)
                # elif key in hls_click_options:
                elif any(keyword in key for keyword in click_relevant_keys):
                    self.click_element(By.XPATH, element_selector)
                else:
                    self.input_text(By.XPATH, element_selector, value)

            self.click_element(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def output_rtsp(self, output_options):
        try:
            self.sub_step_log(f"Create RTSP Output")

            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.output_elements,
                    (
                        f"output_rtsp_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"output_rtsp_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )
                self.input_text(By.XPATH, element_selector, value)
            time.sleep(1)
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True
        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def output_rtmp(self, output_options):
        relevant_keys = ["Subtitle Language", "CDN Authentication"]
        try:
            self.info_log("Create RTMP Output")
            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.output_elements,
                    (
                        f"output_rtmp_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"output_rtmp_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in relevant_keys):
                    self.select_element(By.XPATH, element_selector, "text", value)
                else:
                    self.input_text(By.XPATH, element_selector, value)

            self.click_element(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def output_live_smooth_streaming(self, output_options):
        input_relevant_keys = [
            "Fragment duration",
            "Publishing Point URL",
            "Secondary Point URL",
        ]
        click_relevant_keys = [
            "ISMT Properties",
            "DVB-Subtitle",
            "DVB-Teletext",
            "Enable SCTE35",
            'Send "mfra" at Stop',
        ]
        try:
            self.sub_step_log(f"Create  Live Smooth Streaming Output")

            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.output_elements,
                    (
                        f"output_lss_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"output_lss_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.XPATH, element_selector, value)
                elif any(keyword in key for keyword in click_relevant_keys):
                    self.click_element(By.CSS_SELECTOR, element_selector)
                else:
                    self.select_element(By.XPATH, element_selector, "text", value)

            self.click_element(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def output_dash(self, output_options):
        relevant_keys = [
            "Segment Naming",
            "Mode",
            "SegmentTemplate Mode",
            "HEVC CodecTag",
            "Subtitle Type",
            "DRM Type",
        ]
        try:
            self.sub_step_log(f"Create DASH Output")

            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.output_elements,
                    (
                        f"output_dash_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"output_dash_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in relevant_keys):
                    self.select_element(By.XPATH, element_selector, "text", value)
                elif "SCTE-35 Signalling" in key:
                    self.click_element(By.CSS_SELECTOR, element_selector)
                else:
                    self.select_element(By.XPATH, element_selector, "text", value)

            self.click_element(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False

    def output_cmaf(self, output_options):
        select_relevant_keys = [
            "Ingest Protocol",
            "HTTP Method",
            "Segment Naming",
            "HEVC CodecTag",
            "DRM Type",
            "DASH SegmentTemplate Mode",
        ]
        click_relevant_keys = [
            "Enable Low Latency Transfer",
            "Create Subfolder",
            "DVB-Subtitle-Track",
            "DVB-Teletext-Track",
            "SCTE-35 Signalling",
            "Enable ID3",
            'Use UTC in "tfdt"',
            'Use Negative Time Offset in "trun"',
            'Append "ENDLIST" at Stop',
        ]
        try:
            self.sub_step_log(f"Create  CMAF Output")

            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.output_elements,
                    (
                        f"output_dash_{''.join(key.replace(' ', '_').replace('-', '_').lower())}"
                        if "-" in key
                        else f"output_dash_{key.replace(' ', '_').lower()}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in select_relevant_keys):
                    self.select_element(By.XPATH, element_selector, "text", value)
                elif any(keyword in key for keyword in click_relevant_keys):
                    self.click_element(By.CSS_SELECTOR, element_selector)
                else:
                    self.select_element(By.XPATH, element_selector, "text", value)

            self.click_element(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(e)
            return False
