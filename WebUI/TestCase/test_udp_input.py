import os
import sys

import allure
import pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from configure_audiopresets import ConfigureAudiopreset
from configure_videopresets import ConfigureVideopreset
from login import Login

pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("UDP/IP Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.sub_suite("UDP/IP Multicast Input")
class TestUDPMulticastInput:
    profile_name = {
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

    @staticmethod
    def attach_response_result(step_name, success_message, failure_message):
        def step_decorator(func):
            def step_wrapper(*args, **kwargs):
                with allure.step(step_name):
                    result = func(*args, **kwargs)
                    status_message = success_message if result else failure_message
                    allure.attach(status_message, name=step_name, attachment_type=None)
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
    def videopreset_step(self, preset_name, preset_options):
        with allure.step("Video Preset"):
            videopreset_instance = ConfigureVideopreset()
            return videopreset_instance.configure_videopreset(
                preset_name, preset_options
            )

    @attach_response_result(
        "Audio Preset 생성", "Audio Preset 생성 성공", "Audio Preset 생성 실패"
    )
    def audiopreset_step(self, preset_name, preset_options):
        with allure.step("Audio Preset"):
            audiopreset_instance = ConfigureAudiopreset()
            return audiopreset_instance.configure_audiopreset(
                preset_name, preset_options
            )

    @allure.suite("UDP/IP Input")
    @allure.title("UDP/IP Multicast Input")
    def test_udp_input(self):
        self.login_step("admin", "admin")
        self.videopreset_step(
            self.profile_name["Videopreset Name"], self.videopreset_options
        )
        self.audiopreset_step(
            self.profile_name["Audiopreset Name"], self.audiopreset_options
        )
