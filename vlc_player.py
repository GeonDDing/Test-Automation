import vlc
import time
import cv2
import os.path


class StreamDump:
    def stream_dump(self, url, tc_name):
        duration = 30
        start_time = time.time()
        vlcInstance = vlc.Instance("--demux=ts")
        player = vlcInstance.media_player_new()
        media = vlcInstance.media_new(url)
        media.add_option(f"sout=file/ts:{tc_name}.ts")
        player.set_media(media)
        player.play()
        captured = False

        while time.time() - start_time < duration:
            time.sleep(1)
            if os.path.isfile(f"{tc_name}.ts") and (os.path.getsize(f"{tc_name}.ts") > 1):
                if not captured and time.time() - start_time >= 15:
                    video_file = cv2.VideoCapture(f"{tc_name}.ts")
                    ret, frame = video_file.read()
                    if ret:
                        cv2.imwrite(f"{tc_name}.png", frame)
                        captured = True

        player.stop()
        media.release()


StreamDump().stream_dump("udp://@10.1.0.220:22000", "udp_test")
