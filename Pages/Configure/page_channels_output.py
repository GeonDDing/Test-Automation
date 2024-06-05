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
            self.step_log(f"Add {output_type} Output")
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
        time.sleep(3)
        try:
            self.sub_step_log(f"Select Video, Audio Profile")
            # Video preset 을 선택하기 위에 Stream edit icon 을 클릭
            self.clickable_click(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            # Video preset 셀렉터가 나타날 때 까지 기다림
            if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_video_profile):
                # Vidoe preset 선택
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
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_add_stream_button))
                    )
                    self.click(By.CSS_SELECTOR, self.output_elements.output_add_stream_button)
                except:
                    self.click(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_audio_profile):
                # Audio preset 선택
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

    def output_page(self, output_type, output_options):
        try:
            self.sub_step_log(f"{output_type} Output Configuration Setting")
            time.sleep(3)
            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                output_element = self.get_element_selector(output_type, key)
                if "Subtitle" in key or "Teletext" in key:
                    output_subtitle_element = self.get_element_selector(output_type, key + ("_checkbox"))
                    print(output_subtitle_element)
                    self.click(By.CSS_SELECTOR, output_subtitle_element)
                if "input" in output_element:
                    self.input_box(By.XPATH, output_element, value)
                elif "select" in output_element:
                    self.select_box(By.CSS_SELECTOR, output_element, "text", value)
                elif "checkbox" in output_element:
                    self.click(By.CSS_SELECTOR, output_element)
            time.sleep(1)
            self.click(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True
        except Exception as e:
            self.error_log(f"{output_type} output setting error : {key} | {output_element} | {(e)}")
            return False

    def output_udp(self, output_options):
        output_type = "UDP"
        return self.output_page(output_type, output_options)

    def output_hls(self, output_options):
        output_type = "HLS"
        return self.output_page(output_type, output_options)

    def output_rtsp(self, output_options):
        output_type = "RTSP"
        return self.output_page(output_type, output_options)

    def output_rtmp(self, output_options):
        output_type = "RTMP"
        return self.output_page(output_type, output_options)

    def output_live_smooth_streaming(self, output_options):
        output_type = "LSS"
        return self.output_page(output_type, output_options)

    def output_dash(self, output_options):
        output_type = "DASH"
        return self.output_page(output_type, output_options)

    def output_cmaf(self, output_options):
        output_type = "CMAF"
        return self.output_page(output_type, output_options)

    def get_element_selector(self, output_type, key):
        element_selector = getattr(
            self.output_elements,
            (
                f"output_{output_type.lower()}_{'_'.join(key.replace(' ', '_').replace('-', '_').lower().split())}".replace(
                    '"', ""
                )
            ),
            None,
        )
        return element_selector
