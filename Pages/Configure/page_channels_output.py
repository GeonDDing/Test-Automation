# page_channels_output.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ChannelsOutputElements
import time


class ChannelsOutput(WebDriverSetup):
    def __init__(self, output_type, videopreset_name, audiopreset_name):
        self.output_elements = ChannelsOutputElements()
        try:
            if not self.find_exist_output(output_type):
                self.add_output(output_type)
            time.sleep(1)
            # Output edit 페이지 진입 시, Video, Audio preset 설정 부터 진행
            self.select_stream_preset(videopreset_name, audiopreset_name)
        except Exception as e:
            self.error_log(f"Output initialize error | {repr(e)}")

    def add_output(self, output_type):
        try:
            self.click(By.CSS_SELECTOR, self.output_elements.output_add_output_button)
            if "UDP" in output_type:
                output_type = "TS UDP/IP"
            # Output Type 선택
            self.select_box(
                By.CSS_SELECTOR,
                self.output_elements.output_type,
                "text",
                output_type,
            )
            # 선택한 output type 으로 Output 생성
            self.click(By.CSS_SELECTOR, self.output_elements.output_create_button)
        except Exception as e:
            self.error_log(f"Add output button error | {repr(e)}")

    def find_exist_output(self, output_type):
        try:
            if "UDP" in output_type:
                output_type = "TS"
                output_table = self.find_element(By.XPATH, self.output_elements.output_table)
            for tr in output_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[3].get_attribute("innerText")
                if f"{output_type}:" in column_value:
                    tr.find_elements(By.TAG_NAME, "td")[3].click()
                    return True
            return False
        except Exception as e:
            # 새로 만든 채널의 경우 Output이 없는게 맞기 때문에 해당 Exception 은 예외 메시지를 처리하지 않음
            return False

    def select_stream_preset(self, videopreset_name, audiopreset_name):
        try:
            self.sub_step_log(f"Select Video, Audio Profile")
            # Video preset 을 선택하기 위에 Stream edit icon 을 클릭
            self.clickable_click(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            # Video preset 셀렉터가 나타날 때 까지 기다림
            if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_video_profile):
                # Vidoe preset 선택
                time.sleep(1)
                self.select_box(
                    By.CSS_SELECTOR,
                    self.output_elements.output_video_profile,
                    "text",
                    videopreset_name,
                )
                self.option_log(f"Videopreset : {videopreset_name}")
                # 선택한 Video preset 을 저장
                self.clickable_click(By.CSS_SELECTOR, self.output_elements.output_edit_stream_save_button)
            # TS UDP/IP, RTSP, RTMP ... Add Stream button이 없는 경우 Edit Icon을 클릭해서 Video, Audio 를 같은 스트림에서 선택해야
            try:
                self.clickable_click(By.CSS_SELECTOR, self.output_elements.output_add_stream_button)
            except:
                # Add Stream button not exist case
                self.clickable_click(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            # Audio preset 셀렉터가 나타날 때 까지 기다림
            if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_audio_profile):
                # Audio preset 선택
                time.sleep(1)
                self.select_box(
                    By.CSS_SELECTOR,
                    self.output_elements.output_audio_profile,
                    "text",
                    audiopreset_name,
                )
                self.option_log(f"Audiopreset : {audiopreset_name}")
                # 선택한 Audio preset 저장
            self.clickable_click(By.CSS_SELECTOR, self.output_elements.output_edit_stream_save_button)
            """
            Stream edit icon이 나타날 때 (Output 설정 페이지가 보여짐) 까지 기다림
            기다리지 않으면 페이지가 열리지 않은 상태에서 Output option 을 입력하려고 시도하기 때문에
            no such element 에러가 발생함
            """
            self.wait_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            return True
        except Exception as e:
            self.error_log(f"Select stream error | {repr(e)}")
            return False

    def output_options_handler(self, output_type, output_options, select_options_key, click_options_key):
        try:
            # Output option settings
            self.sub_step_log(f"{output_type} Output Configuration Setting")
            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = self.get_element_selector(output_type, key)
                if element_selector:
                    if any(keyword in key for keyword in select_options_key):
                        # Radio button case
                        if key in ["ISMT Properties", "Enable SCTE35"]:
                            self.select_box(By.CSS_SELECTOR, element_selector, "text", value)
                        else:
                            self.select_box(By.XPATH, element_selector, "text", value)
                    elif any(keyword in key for keyword in click_options_key):
                        if not self.is_checked(By.XPATH, element_selector):
                            self.click(By.XPATH, element_selector)
                    else:
                        # UDP output subtitle 설정
                        if key in ["DVB-Teletext-Track", "DVB-Subtitle-Track"]:
                            sutitle_element_selector = self.get_element_selector(output_type, f"{key}_checkbox")
                            if not self.is_checked(By.XPATH, f"{sutitle_element_selector}"):
                                self.click(By.XPATH, f"{sutitle_element_selector}")
                        self.input_box(By.XPATH, element_selector, value)
            self.click(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True
        except Exception as e:
            self.error_log(f"{output_type} output setting error | {repr(e)}")
            return False

    def output_udp(self, output_options):
        output_type = "UDP"
        select_options_key = [
            "Primary Network Interface",
            "Secondary Network Interface",
            "NULL packet padding",
            "On input loss",
            "Table ID",
            "Modulation Mode",
            "Service Type",
        ]
        click_options_key = [
            "Enable SCTE-35 Passthru",
            "Enable ID3 TDEN tag",
            "Enable TS over RTP",
            "ProMPEG",
            "SRT",
            "ATS/EBP",
            "VCT",
        ]
        return self.output_options_handler(output_type, output_options, select_options_key, click_options_key)

    def output_hls(self, output_options):
        output_type = "HLS"
        click_options_key = [
            "Keep remote segments",
            "Create Subfolder",
            "Create I-frame Playlists",
            "Tagging playlists with timestamp",
            "Enable ID3 TDEN tag",
            "Enable Encryption",
            'Append "ENDLIST" at Stop',
        ]
        return self.output_options_handler(output_type, output_options, [], click_options_key)

    def output_rtsp(self, output_options):
        output_type = "RTSP"
        return self.output_options_handler(output_type, output_options, [], [])

    def output_rtmp(self, output_options):
        output_type = "RTMP"
        select_options_key = ["Subtitle Language", "CDN Authentication"]
        return self.output_options_handler(output_type, output_options, select_options_key, [])

    def output_live_smooth_streaming(self, output_options):
        output_type = "LSS"
        click_options_key = [
            "ISMT Properties",
            "DVB-Subtitle",
            "DVB-Teletext",
            "Enable SCTE35",
            'Send "mfra" at Stop',
        ]
        return self.output_options_handler(output_type, output_options, [], click_options_key)

    def output_dash(self, output_options):
        output_type = "DASH"
        select_options_key = [
            "Segment Naming",
            "Mode",
            "SegmentTemplate Mode",
            "HEVC CodecTag",
            "Subtitle Type",
            "DRM Type",
            "Event Message Format",
        ]
        click_options_key = [
            "SCTE-35 Signalling",
        ]
        return self.output_options_handler(output_type, output_options, select_options_key, click_options_key)

    def output_cmaf(self, output_options):
        output_type = "CMAF"
        select_options_key = [
            "Ingest Protocol",
            "HTTP Method",
            "Segment Naming",
            "HEVC CodecTag",
            "DRM Type",
            "DASH SegmentTemplate Mode",
        ]
        click_options_key = [
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
        return self.output_options_handler(output_type, output_options, select_options_key, click_options_key)

    def get_element_selector(self, output_type, key):
        element_selector = getattr(
            self.output_elements,
            (f"output_{output_type.lower()}_{'_'.join(key.replace(' ', '_').replace('-', '_').lower().split())}"),
            None,
        )
        return element_selector
