import os
import sys
import time
import allure

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from configure_audiopresets import ConfigureAudiopreset
from configure_videopresets import ConfigureVideopreset
from configure_channels import ConfigureChannel
from configure_roles import ConfigureRole
from configure_groups import ConfigureGroup
from configure_devices import ConfigureDevice
from monitor_device import MonitorDevice
from stats_receiver import StatsReceiver
from login import Login


pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("UDP/IP Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Input")
class TestUDPInputProgramNumber:
    test_configuration_data = {
        "ID": "admin",
        "PW": "admin",
        "Role Options": {"Name": "UI Testing Role"},
        "Group Options": {"Name": "UI Testing Group", "Domain": "Live"},
        "Device Options": {
            "Name": "Local Device",
            "IP": "127.0.0.1",
        },
        "Channel Name": "UDP Program Number Testing",
        "Input Type": "UDP",
        "Output Type": "UDP",
        "Backup Source Type": None,
        "Preset Name": {
            "Videopreset Name": "1280x720 | H.264 | 29.97 | 4Mbps | Testing",
            "Audiopreset Name": "AAC | 128K | 48kHz | Testing",
        },
        "Videopreset Options": {
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
        "Audiopreset Options": {
            "Codec": "AAC",
            "MPEG version": "MPEG4",
            "Profile": "Default",
            "Channels": "Stereo",
            "Sampling Rate": "48000",
            "Bitrate": "128",
        },
        "Input Options": {
            "Network URL": "224.30.30.10:19006",
            "Interface": "NIC2",
            "Enable TS over RTP": False,
            "Enable SRT": False,
            "Max input Mbps": "10",
            "Enable HA Mode": "Disabled",
            "Program Selection Mode": "Program number",
            "Program Number": "1010",
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "19007",
            "Primary Network Interface": "NIC1",
            # "Service Name": "testing",
        },
        "Backup Source Options": None,
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
            return login_instance.login(kwargs["ID"], kwargs["PW"])

    @attach_result("Video Preset 생성", "Video Preset 생성 성공", "Video Preset 생성 실패")
    def create_videopreset(self, **kwargs):
        with allure.step("Create video preset"):
            videopreset_instance = ConfigureVideopreset()
            # Required parameters: Videopreset Name, Videopreset Options
            return videopreset_instance.configure_videopreset(
                kwargs["Preset Name"]["Videopreset Name"], kwargs["Videopreset Options"]
            )

    @attach_result("Audio Preset 생성", "Audio Preset 생성 성공", "Audio Preset 생성 실패")
    def create_audiopreset(self, **kwargs):
        with allure.step("Create audio preset"):
            audiopreset_instance = ConfigureAudiopreset()
            # Required parameters: Audiopreset Name, Audiopreset Options
            return audiopreset_instance.configure_audiopreset(
                kwargs["Preset Name"]["Audiopreset Name"], kwargs["Audiopreset Options"]
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

    @attach_result("Role 생성", "Role 생성 성공", "Role 생성 실패")
    def create_role(self, **kwargs):
        with allure.step("Role Configuration"):
            role_instance = ConfigureRole()
            # Required parametes: Role Name, Channel Name
            return role_instance.configure_role(kwargs["Role Options"]["Name"], kwargs["Channel Name"])

    @attach_result("Group 생성", "Group 생성 성공", "Group 생성 실패")
    def create_group(self, **kwargs):
        with allure.step("Group Configuration"):
            group_instance = ConfigureGroup()
            # Required parameters: Group Name, Domain
            return group_instance.configure_group(kwargs["Group Options"]["Name"], kwargs["Group Options"]["Domain"])

    @attach_result("Device 생성", "Device 생성 성공", "Device 생성 실패")
    def create_device(self, **kwargs):
        with allure.step("Group Configuration"):
            device_instance = ConfigureDevice()
            # Required parameters: Device Name, Device IP, Group Name, Role Name
            return device_instance.configure_device(
                kwargs["Device Options"]["Name"],
                kwargs["Device Options"]["IP"],
                kwargs["Group Options"]["Name"],
                kwargs["Role Options"]["Name"],
            )

    @attach_result("Channel 시작", "Channel 시작 성공", "Channel 시작 실패")
    def channel_start(self, **kwargs):
        with allure.step("Channel Start"):
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.chidx = channel_info[1]
            return channel_info[0]

    @attach_result("Channel Stats 요청", "Channel Stats 요청 성공", "Channel Stats 요청 실패")
    def get_channel_stats(self, **kwargs):
        with allure.step("Get Channel Stats"):
            stats_instance = StatsReceiver()
            # Required parameters: Channel Index
            return stats_instance.exec_multiprocessing(self.chidx)

    @attach_result("Channel 종료", "Channel 종료 성공", "Channel 종료 실패")
    def channel_stop(self, **kwargs):
        with allure.step("Channel Stop"):
            monitor_device_instance = MonitorDevice()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.chidx, kwargs["Channel Name"])

    """ 
    The 'create_channel' function parameter definitions are as follows.
    Channel Name, Input Type, Output Type, Backup Source Type,
    Input Option, Output Option, Backup Source Option, Preset Name
    """

    @allure.sub_suite("UDP/IP")
    @allure.title("UDP/IP Input Prpgram Number")
    def test_udp_input(self):
        test_functions = [
            # self.login,
            # self.create_videopreset,
            # self.create_audiopreset,
            self.create_channel,
            self.create_role,
            # self.create_group,
            # self.create_device,
            self.channel_start,
            self.get_channel_stats,
            self.channel_stop,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.test_configuration_data)
