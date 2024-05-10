# page_channels_input.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ChannelsInputElements
import time


class ChannelsInput(WebDriverSetup):
    def __init__(self, input_type):
        self.input_elements = ChannelsInputElements()
        try:
            if input_type == "UDP":
                input_type = "UDP/IP"
            elif input_type in ["RTP", "RTSP"]:
                input_type = "RTP/RTSP"
            elif input_type in ["HTTP", "HLS"]:
                input_type = "HTTP/HLS"
            self.select_box(
                By.CSS_SELECTOR,
                self.input_elements.input_type,
                "text",
                input_type,
            )
        except Exception as e:
            self.error_log(f"Input initialize error | {repr(e)}")
            return False

    def input_common(self, common_options):
        try:
            for key, value in common_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.input_elements,
                    f"input_common_{key.replace(' ', '_').replace('-', '_').lower()}",
                    None,
                )
                if key in ["Evergreen Timeout", "Analysis window", "Distributor ID"]:
                    self.input_box(By.CSS_SELECTOR, element_selector, value)
                else:
                    self.click(By.CSS_SELECTOR, element_selector)
        except Exception as e:
            self.error_log(f"Input common option setting error | {repr(e)}")

    def input_options_handler(self, input_type, input_options, input_options_key, select_options_key):
        try:
            self.sub_step_log(f"{input_type} Input Configuration Setting")
            # Input option setting
            for key, value in input_options.items():
                # 각 옵션 별 Element 를 만들어 주기 위한 함수
                input_element = self.get_input_elements(input_type, key)
                # Audio ID 가 여러개의 Value를 딕셔너리 형태로 가질 수 있어서 '{}' 를 제거하고 Value 만 보여주기 위해 value[1:-1]로 출력
                if isinstance(value, dict):
                    self.option_log(f"{key} : {str(value)[1:-1]}")
                # 일반적인 Key, Value 를 출력
                else:
                    self.option_log(f"{key} : {value}")
                # any는 하나라도 True 이면 결과가 True 이기 때문에 keyword 가 select_options_key 리스트에 존재하면 True를 반환하고 Element 선택
                # if any(keyword in key for keyword in select_options_key):
                # UDP 입력 Program Selection Mode 에서 Service Name을 선택 할 시 Analysis Window의 값이 4000ms 이상이어야 함
                if "Program Selection Mode" in key:
                    self.select_box(By.CSS_SELECTOR, input_element, "text", value)
                    try:
                        self.accept_alert()
                        time.sleep(1)
                        self.input_box(
                            By.CSS_SELECTOR,
                            self.input_elements.input_common_analysis_window,
                            "6000",
                        )
                        time.sleep(1)
                    except:
                        pass
                # else:
                #     self.select_box(By.CSS_SELECTOR, input_element, "text", value)
                # elif any(keyword in key for keyword in input_options_key):
                # Audio ID 가 4개 이상 (0~32개 까지 가능)
                if key == "Audio ID" and isinstance(input_options["Audio ID"], dict):
                    # Audio ID 가 #01 부터 순차적으로 입력 됨
                    for index, sub_value in enumerate(value.values()):
                        if index == 0:
                            self.input_box(By.CSS_SELECTOR, input_element, sub_value)
                        else:
                            self.input_box(
                                By.CSS_SELECTOR,
                                self.input_elements.input_udp_audio_id_extend.format(index, index),
                                sub_value,
                            )
                            # #01, #02 를 넘기고 #03 부터 입력되는 것을 방지하기 위해 5ms 딜레이 추가
                            time.sleep(0.5)
                            # Audio ID 가 #04 부터는 빈 공간을 클릭해야 다음 Audio ID 입력 칸이 나타남
                            self.click(By.XPATH, '//*[@id="editform"]/div[1]/div[3]')
                # Element input text
                # else:
                #     self.input_box(By.CSS_SELECTOR, input_element, value)
                # Input option 중 체크박스 선택은 True, False 로 주기 때문에 Value가 Boolean 타입이면서 True일 때 클릭
                # else:

                if "input" in input_element and "text" in input_element:
                    self.input_box(By.CSS_SELECTOR, input_element, value)
                elif "input" in input_element and "checkbox" in input_element:
                    if isinstance(value, bool) and value:
                        if not self.is_checked(By.CSS_SELECTOR, input_element):
                            self.click(By.CSS_SELECTOR, input_element)
                elif "select" in input_element:
                    self.select_box(By.CSS_SELECTOR, input_element, "text", value)

                # For Loop 속도가 빨라서 옵션 입력을 제대로 못하는 경우가 있어 5ms 딜레이 추가
                time.sleep(0.5)
            return True

        except Exception as e:
            self.error_log(f"{input_type} input setting error | {repr(e)}")
            return False

    def input_udp(self, input_options):
        input_type = "UDP"
        input_options_key = [
            "Network URL",
            "SSM host",
            "Max input Mbps",
            "Program Number",
            "Service Name",
            "Video ID",
            "Audio ID",
        ]
        select_options_key = [
            "Interface",
            "Enable HA Mode",
            "Program Selection Mode",
        ]
        return self.input_options_handler(input_type, input_options, input_options_key, select_options_key)

    def input_rtsp(self, input_options):
        input_type = "RTP"
        input_options_key = [
            "SDP File",
        ]
        return self.input_options_handler(input_type, input_options, input_options_key, [])

    def input_rtmp(self, input_options):
        input_type = "RTMP"
        input_options_key = [
            "URL",
        ]
        return self.input_options_handler(input_type, input_options, input_options_key, [])

    def input_hls(self, input_options):
        input_type = "HLS"
        input_options_key = [
            "URL",
        ]
        return self.input_options_handler(input_type, input_options, input_options_key, [])

    def input_sdi(self, input_options):
        input_type = "SDI"
        input_options_key = [
            "Teletext page",
            "VBI lines",
        ]
        select_options_key = [
            "Video format",
            "Time code type",
            "Timed text source",
            "Teletext character set",
            "Teletext Language Tag",
        ]
        return self.input_options_handler(input_type, input_options, input_options_key, select_options_key)

    def input_playlist(self, input_options):
        input_type = "Playlist"
        input_options_key = [
            "URI",
            "Recurring the last N files",
        ]
        select_options_key = ["Type", "Playlists name"]
        return self.input_options_handler(input_type, input_options, input_options_key, select_options_key)

    def input_smpte_st_2110(self, input_options):
        input_type = "SMPTE ST 2110"
        input_options_key = [
            "Video SDP URL",
            "Audio SDP URL",
            "Ancillary SDP URL",
            "Teletext page",
        ]
        select_options_key = []
        return self.input_options_handler(input_type, input_options, input_options_key, select_options_key)

    def input_ndi(self, input_options):
        input_type = "NDI"
        input_options_key = []
        select_options_key = []
        return self.input_options_handler(input_type, input_options, input_options_key, select_options_key)

    def get_input_elements(self, input_type, key):
        element = getattr(
            self.input_elements,
            f"input_{input_type.lower()}_{key.replace(' ', '_').replace('-', '_').lower()}",
            None,
        )
        return element
