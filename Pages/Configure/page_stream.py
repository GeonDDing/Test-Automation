# page_channels_output.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ChannelsOutputElements
import time


class OutputAddStream(WebDriverSetup):
    def __init__(self):
        self.output_elements = ChannelsOutputElements()

    def select_stream_preset(self, videopreset_name, audiopreset_name):
        time.sleep(3)
        try:
            self.sub_step_log(f"Select Video, Audio Profile")
            # Video preset 을 선택하기 위에 Stream edit icon 을 클릭
            self.clickable_click(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            # Video preset 셀렉터가 나타날 때 까지 기다림
            if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_video_profile):
                # Vidoe preset 선택
                self.drop_down(
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
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.output_elements.output_add_stream_button))
                    )
                    self.click(By.CSS_SELECTOR, self.output_elements.output_add_stream_button)
                except:
                    self.click(By.CSS_SELECTOR, self.output_elements.output_edit_stream)
            if self.wait_element(By.CSS_SELECTOR, self.output_elements.output_audio_profile):
                # Audio preset 선택
                self.drop_down(
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
