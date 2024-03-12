import xml.etree.ElementTree as elementTree
import os
import requests
import configparser
import time
from web_log import WebLog


class ChannelStats:
    def __init__(self):
        try:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            config_path = os.path.join(current_directory, "config.ini")
            config = configparser.ConfigParser()
            config.read(config_path)
            self.url = config.get("Webpage", "url")

        except Exception as e:
            WebLog.error_log("An error occurred:", e)

    def channel_stats(self, chidx):
        output_info = None
        is_evergreen_flag = True
        prev_source_layer = prev_source_stat = None
        max_retries = 3
        start_time = time.time()

        while max_retries > 0:
            if time.time() - start_time > 60:
                break

            try:
                stat_response = requests.get(f"{self.url}:900{chidx}/stats")

            except requests.exceptions.ConnectionError as e:
                max_retries -= 1
                WebLog.warning_log(f"Retrying in 5 seconds...")

                if max_retries == 0:
                    WebLog.error_log("A connection error occurred and terminated.")
                    break
                time.sleep(5)

            else:
                try:
                    root = elementTree.fromstring(stat_response.text)

                except elementTree.ParseError as e:
                    max_retries -= 1
                    WebLog.warning_log(f"Retrying in 5 seconds...")

                    if max_retries == 0:
                        WebLog.error_log("Terminated because xml could not be parsed.")
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

                    if prev_source_layer is not None and source_layer != prev_source_layer:
                        if prev_source_layer == "0":
                            WebLog.exec_log(
                                f"   #{chidx+1:03} User replaced source, Input Changed"
                                if source_layer == "1"
                                else f"   #{chidx+1:03} Source changed (source:#1)"
                            )
                        elif prev_source_layer == "1":
                            WebLog.exec_log(
                                f"#{chidx+1:03} Restored to the {'Primary' if source_layer == '0' else 'Backup'} source"
                            )
                        elif prev_source_layer == "2":
                            WebLog.exec_log(
                                f"   #{chidx+1:03} User replaced source, Input Changed"
                                if source_layer == "1"
                                else f"   #{chidx+1:03} Source changed (source:#0)"
                            )

                    if source_stat == "-1" and is_evergreen_flag:
                        WebLog.exec_log(f"   #{chidx+1:03} Evergreen occurred.")
                        is_evergreen_flag = False
                    elif source_stat != "-1":
                        if not is_evergreen_flag and prev_source_stat != source_stat:
                            WebLog.exec_log(f"   #{chidx+1:03} Evergreen recovered.")
                            is_evergreen_flag = True
                        WebLog.exec_log(
                            f'   #{chidx+1:03} {"Primary" if source_layer == "0" else "Backup" if source_layer == "2" else "Replaced"} Source : {output_info}'
                        )

                    prev_source_layer, prev_source_stat = source_layer, source_stat
                    time.sleep(2)


if __name__ == "__main__":
    test = ChannelStats()
    test.channel_stats(0)
