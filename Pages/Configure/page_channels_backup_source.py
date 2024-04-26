# page_channels_backup_source.py
from selenium.webdriver.common.by import By
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import ChannelsInputElements, ChannelsBackupSourceElements
import time


class ChannelsBackupSource(WebDriverSetup):
    def __init__(self, backup_source_type):
        self.backup_source_elements = ChannelsBackupSourceElements()
        self.input_elements = ChannelsInputElements()
        if backup_source_type == "UDP":
            backup_source_type = "UDP/IP"
        elif backup_source_type in ["RTP", "RTSP"]:
            backup_source_type = "RTP/RTSP"
        elif backup_source_type in ["HTTP", "HLS"]:
            backup_source_type = "HTTP/HLS"
        try:
            if not self.find_element(By.XPATH, '//*[@id="backupSourceBlock"]/div/table').is_displayed():
                self.click(
                    By.XPATH,
                    self.backup_source_elements.backup_soruce_settings_button,
                )
            self.select_box(
                By.CSS_SELECTOR,
                self.backup_source_elements.backup_source_type,
                "text",
                backup_source_type,
            )
        except Exception as e:
            self.error_log(f"Not found backup source table | {repr(e)}")
            return False

    def backup_source_options_handler(
        self, backup_source_type, backup_source_options, backup_source_options_key, select_options_key
    ):
        try:
            self.sub_step_log(f"{backup_source_type} Backup Source Configuration Setting")
            # Backup Source option setting
            for key, value in backup_source_options.items():
                # 각 옵션 별 Element 를 만들어 주기 위한 함수
                backup_source_element = self.get_backup_source_elements(backup_source_type, key)
                # Audio ID 가 여러개의 Value를 딕셔너리 형태로 가질 수 있어서 '{}' 를 제거하고 Value 만 보여주기 위해 value[1:-1]로 출력
                if isinstance(value, dict):
                    self.option_log(f"{key} : {str(value)[1:-1]}")
                # 일반적인 Key, Value 를 출력
                else:
                    self.option_log(f"{key} : {value}")
                # any는 하나라도 True 이면 결과가 True 이기 때문에 keyword 가 select_options_key 리스트에 존재하면 True를 반환하고 Element 선택
                if any(keyword in key for keyword in select_options_key):
                    # UDP 입력 Program Selection Mode 에서 Service Name을 선택 할 시 Analysis Window의 값이 4000ms 이상이어야 함
                    if "Program Selection Mode" in key:
                        self.select_box(By.CSS_SELECTOR, backup_source_element, "text", value)
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
                    else:
                        self.select_box(By.CSS_SELECTOR, backup_source_element, "text", value)
                elif any(keyword in key for keyword in backup_source_options_key):
                    # Audio ID 가 4개 이상 (0~32개 까지 가능)
                    if key == "Audio ID" and isinstance(backup_source_options["Audio ID"], dict):
                        # Audio ID 가 #01 부터 순차적으로 입력 됨
                        for index, sub_value in enumerate(value.values()):
                            if index == 0:
                                self.input_box(By.CSS_SELECTOR, backup_source_element, sub_value)
                            else:
                                self.input_box(
                                    By.CSS_SELECTOR,
                                    self.backup_source_elements.backup_source_udp_audio_id_extend.format(index, index),
                                    sub_value,
                                )
                                # #01, #02 를 넘기고 #03 부터 입력되는 것을 방지하기 위해 0.5s 딜레이 추가
                                time.sleep(0.5)
                                # Audio ID 가 #04 부터는 빈 공간을 클릭해야 다음 Audio ID 입력 칸이 나타남
                                self.click(By.XPATH, '//*[@id="backupSourceBlock"]/div')
                    # Element Backup Source text
                    else:
                        self.input_box(By.CSS_SELECTOR, backup_source_element, value)
                # Backup Source option 중 체크박스 선택은 True, False 로 주기 때문에 Value가 Boolean 타입이면서 True일 때 클릭
                else:
                    if isinstance(value, bool) and value:
                        if not self.is_checked(By.CSS_SELECTOR, backup_source_element):
                            self.click(By.CSS_SELECTOR, backup_source_element)
                # For Loop 속도가 빨라서 옵션 입력을 제대로 못하는 경우가 있어 5ms 딜레이 추가
                time.sleep(0.5)
            return True

        except Exception as e:
            self.error_log(f"{backup_source_type} Backup Source setting error | {repr(e)}")
            return False

    def backup_source_udp(self, backup_source_options):
        backup_source_type = "UDP"
        backup_source_options_key = [
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
        return self.backup_source_options_handler(
            backup_source_type, backup_source_options, backup_source_options_key, select_options_key
        )

    def backup_source_rtsp(self, backup_source_options):
        backup_source_type = "RTP"
        backup_source_options_key = [
            "SDP File",
        ]
        return self.backup_source_options_handler(
            backup_source_type, backup_source_options, backup_source_options_key, []
        )

    def backup_source_rtmp(self, backup_source_options):
        backup_source_type = "RTMP"
        backup_source_options_key = [
            "URL",
        ]
        return self.backup_source_options_handler(
            backup_source_type, backup_source_options, backup_source_options_key, []
        )

    def backup_source_hls(self, backup_source_options):
        backup_source_type = "HLS"
        backup_source_options_key = [
            "URL",
        ]
        return self.backup_source_options_handler(
            backup_source_type, backup_source_options, backup_source_options_key, []
        )

    def backup_source_sdi(self, backup_source_options):
        backup_source_type = "SDI"
        backup_source_options_key = [
            "Teletext page",
            "VBI lines",
        ]
        select_options_key = [
            "Input Port",
            "Video format",
            "Time code type",
            "Timed text source",
            "Teletext character set",
            "Teletext Language Tag",
        ]
        return self.backup_source_options_handler(
            backup_source_type, backup_source_options, backup_source_options_key, select_options_key
        )

    def backup_source_playlist(self, backup_source_options):
        backup_source_type = "Playlist"
        backup_source_options_key = [
            "URI",
            "Recurring the last N files",
        ]
        select_options_key = ["Type", "Playlists name"]
        return self.backup_source_options_handler(
            backup_source_type, backup_source_options, backup_source_options_key, select_options_key
        )

    def backup_source_smpte_st_2110(self, backup_source_options):
        backup_source_type = "SMPTE ST 2110"
        backup_source_options_key = [
            "Video SDP URL",
            "Audio SDP URL",
            "Ancillary SDP URL",
            "Teletext page",
        ]
        select_options_key = []
        return self.backup_source_options_handler(
            backup_source_type, backup_source_options, backup_source_options_key, select_options_key
        )

    def backup_source_ndi(self, backup_source_options):
        backup_source_type = "NDI"
        backup_source_options_key = []
        select_options_key = []
        return self.backup_source_options_handler(
            backup_source_type, backup_source_options, backup_source_options_key, select_options_key
        )

    def get_backup_source_elements(self, backup_source_type, key):
        element = getattr(
            self.backup_source_elements,
            f"backup_source_{backup_source_type.lower()}_{key.replace(' ', '_').replace('-', '_').lower()}",
            None,
        )
        return element
