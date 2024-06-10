# page_channels_output.py
from selenium.webdriver.common.by import By
from TestConfig.web_locator import ChannelsOutputElements
from Pages.Configure.page_stream import OutputAddStream
import time


class ChannelsOutput(OutputAddStream):
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

    def add_output(self, output_type):
        try:
            self.step_log(f"Add {output_type} Output")
            self.click(By.CSS_SELECTOR, self.output_elements.output_add_output_button)
            if "UDP" in output_type:
                output_type = "TS UDP/IP"
            elif "LSS" in output_type:
                output_type = "Live Smooth Streaming"
            # Output Type 선택
            self.drop_down(
                By.CSS_SELECTOR,
                self.output_elements.output_type,
                "text",
                output_type,
            )
            # 선택한 output type 으로 Output 생성
            self.click(By.CSS_SELECTOR, self.output_elements.output_create_button)
        except Exception as e:
            self.error_log(f"Add output button error | {repr(e)}")

    def output_setup_page(self, output_type, output_options):
        output_subtitle_element = str()
        try:
            self.sub_step_log(f"{output_type} Output Configuration Setting")
            time.sleep(3)
            for key, value in output_options.items():
                self.option_log(f"{key} : {value}")
                output_element = self.get_element_selector(output_type, key)
                if ("Subtitle" in key or "Teletext" in key) and "Type" not in key:
                    output_subtitle_element = self.get_element_selector(output_type, key + ("_checkbox"))
                    if output_subtitle_element != None:
                        self.click(By.CSS_SELECTOR, output_subtitle_element)
                    else:
                        self.input_box(By.XPATH, output_element, value)
                else:
                    if "input" in output_element and "checkbox" not in output_element:
                        self.input_box(By.XPATH, output_element, value)
                    elif "select" in output_element:
                        self.click(By.CSS_SELECTOR, output_element)
                        self.drop_down(By.CSS_SELECTOR, output_element, "text", value)
                        self.click(By.CSS_SELECTOR, output_element)
                        time.sleep(3)
                    elif "input[type=checkbox]" in output_element:
                        if isinstance(value, bool) and value:
                            if not self.is_checked(By.CSS_SELECTOR, output_element):
                                self.click(By.CSS_SELECTOR, output_element)
            time.sleep(1)
            self.click(By.CSS_SELECTOR, self.output_elements.output_save_button)
            return True
        except Exception as e:
            self.error_log(f"{output_type} output setting error : {key} | {output_element} | {(e)}")
            return False

    def output_udp(self, output_options):
        output_type = "UDP"
        return self.output_setup_page(output_type, output_options)

    def output_hls(self, output_options):
        output_type = "HLS"
        return self.output_setup_page(output_type, output_options)

    def output_rtsp(self, output_options):
        output_type = "RTSP"
        return self.output_setup_page(output_type, output_options)

    def output_rtmp(self, output_options):
        output_type = "RTMP"
        return self.output_setup_page(output_type, output_options)

    def output_live_smooth_streaming(self, output_options):
        output_type = "LSS"
        return self.output_setup_page(output_type, output_options)

    def output_dash(self, output_options):
        output_type = "DASH"
        return self.output_setup_page(output_type, output_options)

    def output_cmaf(self, output_options):
        output_type = "CMAF"
        return self.output_setup_page(output_type, output_options)

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
