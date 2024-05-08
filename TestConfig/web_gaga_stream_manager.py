# gaga_stream_manager.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    TimeoutException,
)
from TestConfig.web_driver_setup import WebDriverSetup
from TestConfig.web_locator import GaGaWebElements

import time


class GaGaStreamManager(WebDriverSetup):
    def __init__(self):
        self.gaga_elements = GaGaWebElements()
        self.driver.get("http://10.1.0.9")

    def find_exist_stream(self, stream_name):
        try:
            active_stream_table = self.find_element(By.XPATH, self.gaga_elements.gaga_active_stream_table)

            for tr in active_stream_table.find_elements(By.XPATH, ".//tbody/tr"):
                tds = tr.find_elements(By.TAG_NAME, "td")

                if tds:
                    active_stream = tds[2].get_attribute("innerText").split("/")[-1]
                    if stream_name == active_stream:
                        print(f"   {active_stream} is a stream that is already active.")
                        return True

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            print(f"[ERROR] {e}")

    def gaga_stream_upload(self, element_list=None):
        try:
            # Construct current page URL
            folder = "/".join(element_list[0].split("/"))
            page = "%2F".join(folder.split())
            gaga_page = f"http://10.1.0.9?folder={page}"

            self.driver.get(gaga_page)
            time.sleep(1)
            # Find stream table
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, self.gaga_elements.gaga_stream_in_table))
                )
                stream_in_table = self.find_element(By.XPATH, self.gaga_elements.gaga_stream_in_table)

            except TimeoutException:
                stream_in_table = self.find_element(By.XPATH, "/html/body/div/table[2]")

            for tr in stream_in_table.find_elements(By.XPATH, ".//tbody/tr"):
                tds = tr.find_elements(By.TAG_NAME, "td")

                if tds:
                    file_element = tds[0].get_attribute("innerText").strip()
                    if element_list[1] == file_element:
                        if not self.find_exist_stream(element_list[1]):
                            print(f"   Upload Stream : {file_element} / {element_list[2]}")
                            tds[0].click()
                            time.sleep(0.5)
                            self.input_box(
                                By.CSS_SELECTOR,
                                self.gaga_elements.gaga_stream_cast_to,
                                element_list[2],
                            )
                            self.click(
                                By.CSS_SELECTOR,
                                self.gaga_elements.gaga_start_streaming_button,
                            )
                            break

        except (NoSuchElementException, ElementNotVisibleException, AttributeError) as e:
            print(e)


if __name__ == "__main__":
    gaga_upload = GaGaStreamManager()
    stream_list = [
        ["/Streams/", "Rachid.ts", "224.30.30.10:17009"],
        ["/Streams/", "BBB2.0_N2N6PCFD_short_Nielsen.ts", "224.30.30.10:12000"],
        ["/Streams/", "H2HD_DVB_SUBS_HERO_v2.ts", "224.30.30.10:18003"],
        ["/Streams/", "Avatar_with_timecode_H264HD.ts", "224.30.30.10:18007"],
        ["/Streams/", "KT_tvN_TS_20130616_040650_00069.ts", "224.30.30.10:15008"],
        ["/Streams/", "multi_ird_duppids.ts", "224.30.30.10:19006"],
        ["/Streams/NTT/", "rtp_input_11000.pcap", "225.26.1.22"],
        ["/Streams/", "KBS_joy_HD_1080i_.ts", "224.30.30.10:18005"],
        ["Streams/tmp", "32_Audio.ts", "224.30.30.10:12003"],
        ["/Streams/", "NFL_Football_CC.ts", "224.30.30.10:17003"],
    ]

    for i in range(0, len(stream_list)):
        print("{0}. Stream : {1} / Address : {2}".format(i + 1, stream_list[i][1], stream_list[i][2]))
        gaga_upload.gaga_stream_upload(stream_list[i])
