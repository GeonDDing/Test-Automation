import os
import sys
import time
import allure
import pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from configure_audiopresets import ConfigureAudiopreset
from configure_videopresets import ConfigureVideopreset
from configure_channels import ConfigureChannel
from configure_roles import ConfigureRole
from monitor_device import MonitorDevice
from login import Login

pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("UDP/IP Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("UDP/IP Input")
class TestUDPMulticastInput:
    test_data = {
        "id": "admin",
        "pw": "admin",
        "role_name": "LiveRole",
        "channel_name": "UDP Testing Channel",
        "input_type": "UDP",
        "output_type": "UDP",
        "backup_source_type": None,
        "preset_name": {
            "Videopreset Name": "1280x720 | H.264 | 29.97 | 4Mbps | Testing",
            "Audiopreset Name": "AAC | 128K | 48kHz | Testing",
        },
        "videopreset_options": {
            "Codec": "H.264/AVC",
            "Encoding engine": "S/W codec",
            "Resolution": "1280 x 720 (HD 720x)",
            "Frame Rate": "29.97",
            "# of B frames": "2",
            "Bitrate": "4000",
            "H.264 Profile": "Main",
            "I-Frame Interval": "60",
            "Buffering Time": "120",
        },
        "audiopreset_options": {
            "Codec": "AAC",
            "MPEG version": "MPEG4",
            "Profile": "Default",
            "Channels": "Stereo",
            "Sampling Rate": "48000",
            "Bitrate": "128",
        },
        "input_options": {
            "Network URL": "224.30.30.10:15008",
            "Interface": "NIC2",
            "Enable TS over RTP": False,
            "Enable SRT": False,
            "Max input Mbps": "10",
            "Enable HA Mode": "Disabled",
            "Program Selection Mode": "PIDs",
            # "Video ID": "1024",
            # "Audio ID": "1025",
        },
        "output_options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "19005",
            "Primary Network Interface": "NIC1",
            "Service Name": "testing",
        },
        "backup_source_options": None,
    }

    @staticmethod
    def attach_result(step_name, success_message, failure_message):
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

    @attach_result("로그인", "Login 성공", "Login 실패")
    def login(self, **kwargs):
        with allure.step("Login"):
            login_instance = Login()
            return login_instance.login(kwargs["id"], kwargs["pw"])

    @attach_result("Video Preset 생성", "Video Preset 생성 성공", "Video Preset 생성 실패")
    def create_videopreset(self, **kwargs):
        with allure.step("Create video preset"):
            videopreset_instance = ConfigureVideopreset()
            return videopreset_instance.configure_videopreset(
                kwargs["preset_name"]["Videopreset Name"], kwargs["videopreset_options"]
            )

    @attach_result("Audio Preset 생성", "Audio Preset 생성 성공", "Audio Preset 생성 실패")
    def create_audiopreset(self, **kwargs):
        with allure.step("Create audio preset"):
            audiopreset_instance = ConfigureAudiopreset()
            return audiopreset_instance.configure_audiopreset(
                kwargs["preset_name"]["Audiopreset Name"], kwargs["audiopreset_options"]
            )

    @attach_result("Channel 생성", "Channel 생성 성공", "Channel 생성 실패")
    def create_channel(self, **kwargs):
        channel_instance = ConfigureChannel(**kwargs)
        channel_instance.pre_channel_configuration()
        with allure.step("Create output"):
            channel_instance.setup_output()
            time.sleep(1)
        with allure.step("Create input"):
            channel_instance.setup_input()
        return channel_instance.post_channel_configuration()

    @attach_result("Role에 Channel 등록", "Role에 Channel 추가 성공", "Role에 Channel 추가 실패")
    def add_channel_to_role(self, **kwargs):
        role_instance = ConfigureRole()
        return role_instance.configure_role(kwargs["role_name"], kwargs["channel_name"])

    @attach_result("Channel 시작", "Channel 시작 성공", "Channel 시작 실패")
    def channel_start(self, **kwargs):
        monitor_device_instance = MonitorDevice()
        return monitor_device_instance.channel_start(kwargs["channel_name"])

    """ 
    The 'create_channel' function parameter definitions are as follows.
    Channel Name, Input Type, Output Type, Backup Source Type,
    Input Option, Output Option, Backup Source Option, Preset Name
    """

    @allure.sub_suite("UDP/IP Multicast Input")
    @allure.title("UDP/IP Multicast Input")
    def test_udp_input(self):
        self.login(**self.test_data)
        self.create_videopreset(**self.test_data)
        self.create_audiopreset(**self.test_data)
        self.create_channel(**self.test_data)
        self.add_channel_to_role(**self.test_data)
        self.channel_start(**self.test_data)


if __name__ == "__main__":
    instance = TestUDPMulticastInput()
    instance.test_udp_input()
