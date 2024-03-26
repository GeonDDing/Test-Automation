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
        try:
            if not self.find_exist_output(output_type):
                self.add_output(output_type)
            time.sleep(1)
            # Output edit 페이지 진입 시, Video, Audio preset 설정 부터 진행
            self.select_stream_preset(videopreset_name, audiopreset_name)
        except Exception as e:
            self.error_log(f"Output initialize error {e}")

    def add_output(self, output_type):
        try:
            # Channel edit 페이지에서 Add Output button 이 나타날 때 까지 기다림
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_add_output_button))
            )
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_add_output_button)
            if "UDP" in output_type:
                output_type = "TS UDP/IP"
            # Output Type 선택
            self.select_element(
                By.CSS_SELECTOR,
                self.output_elements.output_type,
                "text",
                output_type,
            )
            # 선택한 output type 으로 Output 생성
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_create_button)
        except TimeoutException as e:
            self.error_log(f"Add output button error {e}")

    def find_exist_output(self, output_type):
        try:
            if "UDP" in output_type:
                output_type = "TS"
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, self.output_elements.output_table))
                )
                output_table = self.find_web_element(By.XPATH, self.output_elements.output_table)
            except TimeoutException as e:
                return False
            for tr in output_table.find_elements(By.XPATH, ".//tbody/tr"):
                column_value = tr.find_elements(By.TAG_NAME, "td")[3].get_attribute("innerText")
                if f"{output_type}:" in column_value:
                    tr.find_elements(By.TAG_NAME, "td")[3].click()
                    # self.option_log(f"{column_value}")
                    return True  # Output found and clicked
            return False  # Output not found
        except NoSuchElementException as e:
            self.error_log(f"Not found exist output {e}")
            # Handle the error as needed, for example, return False or raise the exception again
            return False

    def select_stream_preset(self, videopreset_name, audiopreset_name):
        try:
            self.sub_step_log(f"Select Video, Audio Profile")
            # Output 설정 페이지에서 Stream edit icon이 나타날 때 까지 기다림
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_edit_stream))
            )
            # Video preset 을 선택하기 위에 Stream edit icon 을 클릭
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            # Video preset 셀렉터가 나타날 때 까지 기다림
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_video_profile))
            )
            # Vidoe preset 선택
            self.select_element(
                By.CSS_SELECTOR,
                self.output_elements.output_video_profile,
                "text",
                videopreset_name,
            )
            self.option_log(f"Videopreset : {videopreset_name}")
            # 선택한 Video preset 을 저장
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream_save_button)
            # TS UDP/IP, RTSP, RTMP ... Add Stream button이 없는 경우 Edit Icon을 클릭해서 Video, Audio 를 같은 스트림에서 선택해야
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_add_stream_button))
                )
                # Add Stream button exist case
                self.click_element(By.CSS_SELECTOR, self.output_elements.output_add_stream_button)
            except:
                # Add Stream button not exist case
                self.click_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            # Audio preset 셀렉터가 나타날 때 까지 기다림
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_audio_profile))
            )
            # Audio preset 선택
            self.select_element(
                By.CSS_SELECTOR,
                self.output_elements.output_audio_profile,
                "text",
                audiopreset_name,
            )
            self.option_log(f"Audiopreset : {audiopreset_name}")
            # 선택한 Audio preset 저장
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream_save_button)
            # Stream edit icon이 나타날 때 (Output 설정 페이지가 보여짐) 까지 기다림
            self.wait_element(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            return True
        except Exception as e:
            self.error_log(f"Select stream error {e}")
            return False

    def output_options_handler(self, output_type, output_options, select_options_key, click_options_key):
        try:
            # Output option settings
            self.sub_step_log(f"{output_type} Input Configuration Setting")
            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = self.get_element_selector(output_type, key)
                if element_selector:
                    if any(keyword in key for keyword in select_options_key):
                        # Radio button case
                        if key in ["ISMT Properties", "Enable SCTE35"]:
                            self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                        else:
                            self.select_element(By.XPATH, element_selector, "text", value)
                    elif any(keyword in key for keyword in click_options_key):
                        self.click_element(By.XPATH, element_selector)
                    else:
                        self.input_text(By.XPATH, element_selector, value)
            self.click_element(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            self.error_log(f"{output_type} output setting error {e}")
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
