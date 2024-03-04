import os
import sys
import time
import allure
import pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from configure_audiopresets import ConfigureAudiopreset
from configure_videopresets import ConfigureVideopreset
from configure_channels import ConfigureChannel
from login import Login

pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("UDP/IP Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.sub_suite("UDP/IP Multicast Input")
class TestUDPMulticastInput:
    preset_name = {
        "Videopreset Name": "1280x720 | H.264 | 29.97 | 4Mbps | Testing",
        "Audiopreset Name": "AAC | 128K | 48kHz | Testing",
    }

    videopreset_options = {
        "Codec": "H.264/AVC",
        "Encoding engine": "S/W codec",
        "Resolution": "1280 x 720 (HD 720x)",
        "Frame Rate": "29.97",
        "# of B frames": "2",
        "Bitrate": "4000",
        "I-Frame Interval": "60",
        "Buffering Time": "120",
    }

    audiopreset_options = {
        "Codec": "AAC",
        "MPEG version": "MPEG4",
        "Profile": "Default",
        "Channels": "Stereo",
        "Sampling Rate": "48000",
        "Bitrate": "128",
    }

    input_udp_options = {
        "Network URL": "224.30.30.10:15008",
        "Interface": "NIC1",
        "Enable TS over RTP": False,
        "Enable SRT": True,
        "Max input Mbps": "10",
        "Enable HA Mode": "Disabled",
        "Program Selection Mode": "PIDs",
        "Video ID": "1024",
        "Audio ID": "1025",
    }

    output_udp_options = {
        "Primary Output Address": "10.1.0.220",
        "Primary Output Port": "19005",
        "Primary Network Interface": "NIC1",
        "Service Name": "testing",
    }

    @staticmethod
    def attach_response_result(step_name, success_message, failure_message):
        def step_decorator(func):
            def step_wrapper(*args, **kwargs):
                with allure.step(step_name):
                    result = func(*args, **kwargs)
                    status_message = success_message if result else failure_message
                    allure.attach(
                        status_message,
                        name=step_name,
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    assert result, failure_message

            return step_wrapper

        return step_decorator

    @attach_response_result("로그인", "Login 성공", "Login 실패")
    def login_step(self, id, pwd):
        with allure.step("Login"):
            login_instance = Login()
            return login_instance.login(id, pwd)

    @attach_response_result(
        "Video Preset 생성", "Video Preset 생성 성공", "Video Preset 생성 실패"
    )
    def create_videopreset_step(self, preset_name, preset_options):
        with allure.step("Create Video Preset"):
            videopreset_instance = ConfigureVideopreset()
            return videopreset_instance.configure_videopreset(
                preset_name, preset_options
            )

    @attach_response_result(
        "Audio Preset 생성", "Audio Preset 생성 성공", "Audio Preset 생성 실패"
    )
    def create_audiopreset_step(self, preset_name, preset_options):
        with allure.step("Create Audio Preset"):
            audiopreset_instance = ConfigureAudiopreset()
            return audiopreset_instance.configure_audiopreset(
                preset_name, preset_options
            )

    @attach_response_result("Channel 생성", "Channel 생성 성공", "Channel 생성 실패")
    def create_channel_step(self, *args, **kwargs):
        channel_instance = ConfigureChannel(*args, **kwargs)
        # with allure.step("Create UDP/IP Input Channel"):
        channel_instance.pre_channel_configuration()
        time.sleep(1)
        with allure.step("Create Output"):
            channel_instance.setup_output()
            time.sleep(3)
        with allure.step("Create Input"):
            channel_instance.setup_input()
        return channel_instance.post_channel_configuration()

    @allure.suite("UDP/IP Input")
    @allure.title("UDP/IP Multicast Input")
    def test_udp_input(self):
        self.login_step("admin", "admin")
        self.create_videopreset_step(
            self.preset_name["Videopreset Name"], self.videopreset_options
        )
        self.create_audiopreset_step(
            self.preset_name["Audiopreset Name"], self.audiopreset_options
        )
        self.create_channel_step(
            "UDP Testing Channel",
            "UDP/IP",
            "UDP/IP",
            None,
            self.input_udp_options,
            self.output_udp_options,
            None,
            self.preset_name,
        )
