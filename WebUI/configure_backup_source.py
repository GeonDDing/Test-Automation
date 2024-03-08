# configure_channels.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import ConfigureBackupSourceElements, ConfigureInputElements
import time


class ConfigureBackupSource(WebDriverMethod):
    def __init__(self, backup_source_type):
        self.backup_source_elements = ConfigureBackupSourceElements()
        self.input_elements = ConfigureInputElements()
        try:
            self.select_element(
                By.CSS_SELECTOR,
                self.backup_source_elements.backup_source_type,
                "text",
                backup_source_type,
            )

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")

        finally:
            self.quit_driver()

    def backup_source_udp(self, backup_source_options):
        input_relevant_keys = [
            "Network URL",
            "SSM host",
            "Max input Mbps",
            "Video ID",
            "Audio ID",
        ]
        select_relevant_keys = ["Interface", "Enable HA Mode", "Program Selection Mode"]
        try:
            self.sub_step_log("UDP Backup Source 설정")

            for key, value in backup_source_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(
                    self.backup_source_elements,
                    (
                        f"input_udp_{''.join(key.replace(' ', '_').lower().split('-'))}"
                        if "-" in key
                        else f"input_udp_{key.lower().replace(' ', '_')}"
                    ),
                    None,
                )

                if any(keyword in key for keyword in select_relevant_keys):
                    if "Program Selection Mode" in key:
                        mode = self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                        try:
                            self.accept_alert()
                            self.input_text(
                                By.CSS_SELECTOR,
                                self.input_elements.input_common_analysis_window,
                                "6000",
                            )
                            time.sleep(1)

                        except:
                            pass

                        if mode in ["Program number", "Service name"]:
                            mapping = {
                                "Program number": (
                                    self.backup_source_elements.backup_source_udp_program_number,
                                    "1010",
                                ),
                                "Service name": (
                                    self.backup_source_elements.backup_source_udp_service_name,
                                    "E2 Channel",
                                ),
                            }
                            self.input_text(By.CSS_SELECTOR, *mapping.get(mode))
                    else:
                        self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                elif any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    if isinstance(value, bool) and value:
                        self.click_element(By.CSS_SELECTOR, element_selector)
                    else:
                        self.click_element(By.CSS_SELECTOR, element_selector)

            return True

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")
            return False

        finally:
            self.quit_driver()

    def backup_source_rtp(self, backup_source_options):
        try:
            self.sub_step_log("RTP Backup Source 설정")
            self.input_text(
                By.CSS_SELECTOR,
                self.backup_source_elements.backup_source_udp_network_url,
                backup_source_options.get("sdf_file"),
            )

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")

        finally:
            self.quit_driver()

    def backup_source_rtmp(self, backup_source_options):
        try:
            self.sub_step_log("RTMP Backup Source 설정")
            self.input_text(
                By.CSS_SELECTOR,
                self.backup_source_elements.backup_source_udp_network_url,
                backup_source_options.get("url"),
            )

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")

        finally:
            self.quit_driver()

    def backup_source_hls(self, backup_source_options):
        try:
            self.sub_step_log("HLS Backup Source 설정")
            self.input_text(
                By.CSS_SELECTOR,
                self.backup_source_elements.backup_source_hls_url,
                backup_source_options.get("url"),
            )

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")

    def backup_source_sdi(self, backup_source_options):
        try:
            self.sub_step_log("SDI Backup Source 설정")

            for key, value in backup_source_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(self.backup_source_elements, f"input_sdi_{key}", None)

                if element_selector:
                    if key in ["teletext_page", "vbi_lines"]:
                        self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    self.select_element(By.CSS_SELECTOR, element_selector, "text", value)

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")

        finally:
            self.quit_driver()

    def backup_source_playlist(self, backup_source_options):
        try:
            self.sub_step_log("Playlist Backup Source 설정")
            playlist_type = backup_source_options.get("type")

            if playlist_type:
                self.select_element(
                    By.CSS_SELECTOR,
                    self.backup_source_elements.backup_source_playlist_type,
                    "text",
                    playlist_type,
                )
                if playlist_type == "Local Static Playlist":
                    self.select_element(
                        By.CSS_SELECTOR,
                        self.backup_source_elements.backup_source_playlist_playlists_name,
                    )
                elif playlist_type == "Clipcasting XML" or playlist_type == "Remote Media Asset Directory":
                    self.input_text(
                        By.CSS_SELECTOR,
                        self.backup_source_elements.backup_source_playlist_clipcasting_uri,
                        backup_source_options.get("uri"),
                    )
                    if playlist_type == "Remote Media Asset Directory":
                        self.input_text(
                            By.CSS_SELECTOR,
                            self.backup_source_elements.backup_source_playlist_remote_media_asset_uri,
                            backup_source_options.get("recurring"),
                        )
                        self.select_element(
                            By.CSS_SELECTOR,
                            self.backup_source_elements.backup_soruce_playlist_sort_by,
                            "text",
                            backup_source_options.get("sort_by"),
                        )

            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")
        finally:
            self.quit_driver()

    def backup_source_smpte_st_2110(self, backup_source_options):
        try:
            self.sub_step_log("SMPTE ST 2110 Backup Source 설정")

            for key, value in backup_source_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(self.backup_source_elements, f"input_smpte_st_2110_{key}", None)
                if element_selector:
                    if key in [
                        "video_sdp_url",
                        "audio_sdp_url",
                        "ancillary_sdp_url",
                        "teletext_page",
                    ]:
                        self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    self.select_element(By.CSS_SELECTOR, element_selector, "text", value)
                time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")

        finally:
            self.quit_driver()

    def backup_source_ndi(self, backup_source_options):
        try:
            self.sub_step_log("NDI Backup Source 설정")

            for key, value in backup_source_options.items():
                self.option_log(f"{key} : {value}")
                element_selector = getattr(self.backup_source_elements, f"input_ndi_{key}", None)
                self.input_text(By.CSS_SELECTOR, element_selector, value)
                time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException) as e:
            self.error_log(f"{e}")

        finally:
            self.quit_driver()
