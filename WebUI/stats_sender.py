import xml.etree.ElementTree as elementTree
import configparser
import requests
import time
import os
from web_log import WebLog


class StatsSender:
    def __init__(self):
        try:
            script_directory = os.path.dirname(os.path.realpath(__file__))  # 현재 경로만 추출
            config_path = os.path.join(script_directory, "config.ini")  # 현재 경로에서 config.ini 찾음
            config = configparser.ConfigParser()
            config.read(config_path)
            self.url = config.get("Webpage", "url")
        except Exception as e:
            WebLog.error_log("An error occurred:", e)

    def stats_sender(self, queue):
        output_info = None
        max_retries = 3
        while max_retries > 0:
            try:
                chidx = 0
                stat_response = requests.get(f"{self.url}:900{chidx}/stats")

            except requests.exceptions.ConnectionError as e:
                max_retries -= 1
                WebLog.info_log(f"Retrying in 5 seconds...")
                if max_retries == 0:
                    WebLog.info_log("A connection error occurred and terminated.")
                    queue.put("quit")
                    break
                time.sleep(5)
            else:
                try:
                    root = elementTree.fromstring(stat_response.text)

                except elementTree.ParseError as e:
                    max_retries -= 1
                    WebLog.info_log(f"Retrying in 5 seconds...")

                    if max_retries == 0:
                        WebLog.info_log("Terminated because xml could not be parsed.")
                        queue.put("quit")
                        break
                    time.sleep(5)
                else:
                    max_retries = 3
                    source_layer = root.find("sourceLayer").text
                    source_stat = root.find("sourceStat").text
                    codec_type_mapping = {"0": "H.264/AVC", "8": "HEVC"}

                    for stats in root.findall("stream"):
                        codec_type_mapping = {"0": "H.264/AVC", "8": "HEVC"}
                        video_codec_type = codec_type_mapping.get(stats.find("videoCodecType").text, "Unknown")
                        video_width = stats.find("videoWidth").text
                        video_height = stats.find("videoHeight").text
                        video_rate = float(stats.find("videoRate").text) / 1000000
                        frame_count = stats.find("muxedFrameCount").text
                        frame_rate = stats.find("frameRate").text

                        if not video_rate == 0.0:
                            mux_rate = float(stats.find("muxRate").text) / 1000000
                            output_info = f"{video_codec_type} {video_width}x{video_height} {video_rate:.3f} Mbps {frame_rate} fps | Mux Rate: {mux_rate:.3f} Mbps | Frames : {frame_count}"

                    if output_info is not None:
                        queue.put((chidx, source_layer, source_stat, output_info))
                    time.sleep(2)
