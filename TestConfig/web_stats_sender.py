import xml.etree.ElementTree as elementTree
import configparser
import requests
import time
import os
from TestConfig.web_log import WebLog


class StatsSender(WebLog):
    def __init__(self):
        try:
            script_directory = os.path.dirname(os.path.realpath(__file__))
            config_path = os.path.join(script_directory, "config.ini")
            config = configparser.ConfigParser()
            config.read(config_path)
            self.url = config.get("Webpage", "url")

        except Exception as e:
            self.exec_log("An error occurred:", e)

    def stats_sender(self, queue, chidx, channel_name, config_channel_name):
        try:
            output_info = None
            max_retries = int(3)
            start_time = time.time()
            mchidx = f"0{chidx+1:02}"
            while max_retries > 0:
                try:
                    stat_response = requests.get(f"{self.url}:900{chidx}/stats")

                except requests.exceptions.ConnectionError as e:
                    max_retries = max_retries - 1
                    self.warning_log(f"#{mchidx} Retrying in 10 seconds...")
                    if max_retries == 0:
                        self.error_log(f"#{mchidx} A connection error occurred and terminated.")
                        queue.put("quit")
                        break
                    time.sleep(10)
                    pass

                else:
                    try:
                        root = elementTree.fromstring(stat_response.text)

                    except elementTree.ParseError as e:
                        max_retries = max_retries - 1
                        self.warning_log(f"#{mchidx} XML could not be parsed. Retrying in 10 seconds...")
                        if max_retries == 0:
                            self.error_log(f"#{mchidx} Terminated because xml could not be parsed.")
                            queue.put("quit")
                            break
                        time.sleep(10)
                        pass

                    else:
                        max_retries = 3
                        config_name = root.find("configName").text
                        source_layer = root.find("sourceLayer").text
                        source_stat = root.find("sourceStat").text
                        codec_type_mapping = {"0": "H.264/AVC", "8": "HEVC"}
                        if config_name == channel_name:
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

                            if output_info != None:
                                queue.put((chidx, channel_name, source_layer, source_stat, output_info))
                        else:
                            self.error_log("Channel names do not match.")
                            config_channel_name.append(config_name)
                            queue.put("Channel names do not match")
                            break
                        if time.time() - start_time > 10:
                            queue.put("quit")
                            break
                        time.sleep(2)
        except Exception as e:
            self.error_log(f"Stats sender error | {repr(e)}")
            queue.put("quit")
