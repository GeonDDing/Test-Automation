import subprocess
import shutil
import platform, os.path, time
from TestConfig.web_log import WebLog


class StreamCapture(WebLog):
    def stream_capture(self, capture_queue, url, outputName, capture_image):
        captureTime = 10
        while True:
            if capture_queue.get() == "start":
                self.exec_log("Start output stream dump and image capture.")
                outputStream = "{0}_{1}.ts".format(self.convert_date()[3], outputName)
                outputImage = "{0}_{1}.png".format(self.convert_date()[3], outputName)
                ffmpegStreamDumpCommand = [
                    "ffmpeg",
                    "-loglevel",
                    "panic",
                    "-i",
                    url,
                    "-t",
                    "25",
                    "-c:v",
                    "copy",
                    "-c:a",
                    "copy",
                    # "dvbsub",
                    outputStream,
                ]
                try:
                    subprocess.run(ffmpegStreamDumpCommand, timeout=30, check=True)
                except subprocess.TimeoutExpired:
                    self.error_log("Termination of stream dump process due to timeout.")
                    return None
                except subprocess.CalledProcessError as e:
                    pass
                else:
                    time.sleep(2)
                    ffmpegImageCaptureCommand = [
                        "ffmpeg",
                        "-loglevel",
                        "panic",
                        "-i",
                        str(outputStream),
                        "-ss",
                        str(captureTime),
                        "-s",
                        "640x360",
                        "-vframes",
                        "1",
                        outputImage,
                    ]
                    try:
                        subprocess.run(ffmpegImageCaptureCommand)
                        capture_image.append(outputImage)
                    except subprocess.TimeoutExpired:
                        self.error_log("Termination of image capture process due to timeout.")
                        return None
                    except subprocess.CalledProcessError as e:
                        pass
                    else:
                        if os.path.isfile(outputImage):
                            if platform.system() == "Windows":
                                shutil.move(f"{outputImage}", "Capture/")
                                self.exec_log("End output stream dump and image capture.")
                                return capture_image
                            else:
                                shutil.move(f"{outputImage}", "Capture/")
                                self.exec_log("End output stream dump and image capture.")
                                return capture_image
            if capture_queue.get() == "quit":
                return capture_image
