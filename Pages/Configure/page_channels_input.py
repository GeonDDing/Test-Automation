# page_channels_input.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ChannelsInputElements
import time


class ChannelsInput(WebDriverSetup):
    def __init__(self, input_type):
        self.input_elements = ChannelsInputElements()
        self.input_type = input_type
        if input_type == "UDP":
            self.input_type = "UDP/IP"
        elif input_type in ["RTP", "RTSP"]:
            self.input_type = "RTP/RTSP"
        elif input_type in ["HTTP", "HLS"]:
            self.input_type = "HTTP/HLS"
        elif input_type in "LSS":
            self.input_type = "Live Smooth Streaming"
        try:
            self.drop_down(
                By.CSS_SELECTOR,
                self.input_elements.input_type,
                "text",
                self.input_type,
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

    def input_setup_page(self, input_options):
        try:
            self.sub_step_log(f"{self.input_type} Input Configuration Setting")
            # Input option setting
            for key, value in input_options.items():
                # 각 옵션 별 Element 를 만들어 주기 위한 함수
                input_element = self.get_input_elements(key)
                # Audio ID 가 여러개의 Value를 딕셔너리 형태로 가질 수 있어서 '{}' 를 제거하고 Value 만 보여주기 위해 value[1:-1]로 출력
                if isinstance(value, dict):
                    self.option_log(f"{key} : {str(value)[1:-1]}")
                # 일반적인 Key, Value 를 출력
                else:
                    self.option_log(f"{key} : {value}")
                # UDP 입력 Program Selection Mode 에서 Service Name을 선택 할 시 Analysis Window의 값이 4000ms 이상이어야 함
                if "Program Selection Mode" in key:
                    self.drop_down(By.CSS_SELECTOR, input_element, "text", value)
                    try:
                        self.accept_alert()
                        time.sleep(1)
                        self.input_box(
                            By.CSS_SELECTOR,
                            self.input_elements.input_common_analysis_window,
                            "6000",
                        )
                    except:
                        pass
                elif (
                    "input" in input_element and "text" in input_element and "input[type=checkbox]" not in input_element
                ):
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
                                # #01, #02 를 넘기고 #03 부터 입력되는 것을 방지하기 위해 1초 딜레이 추가
                                time.sleep(1)
                                # Audio ID 가 #04 부터는 빈 공간을 클릭해야 다음 Audio ID 입력 칸이 나타남
                                self.click(By.XPATH, '//*[@id="editform"]/div[1]/div[3]')
                    else:
                        self.input_box(By.CSS_SELECTOR, input_element, value)
                elif 'input[type="checkbox"]' in input_element:
                    if isinstance(value, bool) and value:
                        if not self.is_checked(By.CSS_SELECTOR, input_element):
                            self.click(By.CSS_SELECTOR, input_element)
                elif "select" in input_element:
                    self.drop_down(By.CSS_SELECTOR, input_element, "text", str(value))
                # For Loop 속도가 빨라서 옵션 입력을 제대로 못하는 경우가 있어 1s 딜레이 추가
                time.sleep(1)
            return True
        except Exception as e:
            self.error_log(f"{self.input_type} input setting error : {key} | {repr(e)}")
            return False

    def input_udp(self, input_options):
        return self.input_setup_page(input_options)

    def input_rtsp(self, input_options):
        return self.input_setup_page(input_options)

    def input_rtmp(self, input_options):
        return self.input_setup_page(input_options)

    def input_hls(self, input_options):
        return self.input_setup_page(input_options)

    def input_sdi(self, input_options):
        return self.input_setup_page(input_options)

    def input_playlist(self, input_options):
        return self.input_setup_page(input_options)

    def input_smpte_st_2110(self, input_options):
        return self.input_setup_page(input_options)

    def input_ndi(self, input_options):
        return self.input_setup_page(input_options)

    def get_input_elements(self, key):
        element = getattr(
            self.input_elements,
            f"input_{self.input_type.lower().replace(' ','_').replace('/ip', '')}_{key.replace(' ', '_').replace('-', '_').lower()}",
            None,
        )
        print(
            f"input_{self.input_type.lower().replace(' ','_').replace('/ip', '')}_{key.replace(' ', '_').replace('-', '_').lower()}"
        )
        return element
