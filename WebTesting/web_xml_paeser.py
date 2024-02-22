import xml.etree.ElementTree as elementTree
import requests
import time


class WebXMLParser():
    def xml_parser(self, url, chidx):

        try:
            stat_response = requests.get(
                f"http://{url}:900{chidx}/stats", verify=False)
            root = elementTree.fromstring(stat_response.text)
            source_layer = root.find('sourceLayer').text
            source_stat = root.find('sourceStat').text
            codec_type_mapping = {'0': 'H.264/AVC', '8': 'HEVC'}

            # SourceLayer 를 Que로 날려서 상태 체크 필요
            if source_layer == '0':
                if source_stat == '-1':
                    print(f"Ch {chidx+1} Evergreen occurred")
            elif source_layer == '2':
                print(f"Ch{chidx+1} Switch to backup source")
                if source_stat == '-1':
                    print(f"Ch{chidx+1} Evergreen occurred")

            for stats in root.findall('stream'):
                codec_type_mapping = {'0': 'H.264/AVC', '8': 'HEVC'}
                video_codec_type = codec_type_mapping.get(
                    stats.find('videoCodecType').text, 'Unknown')
                video_width = stats.find('videoWidth').text
                video_height = stats.find('videoHeight').text
                video_rate = float(stats.find('videoRate').text)/1000000
                frame_count = stats.find('muxedFrameCount').text
                frame_rate = stats.find('frameRate').text
                if not video_rate == 0.0:
                    mux_rate = float(stats.find('muxRate').text)/1000000
                    output_info = f"{video_codec_type} {video_width}x{video_height} {video_rate:.3f} Mbps {frame_rate} fps | Mux Rate: {mux_rate:.3f} Mbps | Frames : {frame_count}"

            print(output_info)
            return source_layer, source_stat

        except Exception as e:
            print(e)


if __name__ == '__main__':
    test = WebXMLParser()
    while True:
        test.xml_parser('10.1.0.145', 0)
        time.sleep(2)
