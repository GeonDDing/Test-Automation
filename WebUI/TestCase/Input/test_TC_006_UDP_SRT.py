import os
import sys
import time
import allure

# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from configure_channels import ConfigureChannel
from configure_roles import ConfigureRole
from monitor_device import MonitorDevice
from stats_receiver import StatsReceiver
from login import Login


pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("UDP/IP Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Input")
class TestInputUDPSRT:
    srt_sender_configuration_data = {
        "ID": "admin",
        "PW": "admin",
        "Role Options": {"Name": "UI Testing Role"},
        "Group Options": {
            "Name": "UI Testing Group",
            "Domain": "Live",
        },
        "Device Options": {
            "Name": "Local Device",
            "IP": "127.0.0.1",
        },
        "Channel Name": "UDP SRT Sender Testing",
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
        "Common Options": {
            "Evergreen Timeout": "4000",
            "Analysis window": "4000",
        },
        "Input Options": {
            "Network URL": "224.30.30.10:18007",
            "Interface": "NIC2",
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.145",
            "Primary Output Port": "15005",
            "Primary Network Interface": "NIC1",
            "SRT": True,
        },
        "Backup Source Options": None,
    }

    srt_receiver_configuration_data = {
        "Channel Name": "UDP SRT Receiver Testing",
        "Input Type": "UDP",
        "Output Type": "UDP",
        "Backup Source Type": None,
        "Preset Name": {
            "Videopreset Name": "1280x720 | H.264 | 29.97 | 4Mbps | Testing",
            "Audiopreset Name": "AAC | 128K | 48kHz | Testing",
        },
        "Common Options": {
            "Evergreen Timeout": "4000",
            "Analysis window": "4000",
        },
        "Input Options": {
            "Network URL": "10.1.0.145:15005",
            "Interface": "NIC1",
            "Enable SRT": True,
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "19008",
            "Primary Network Interface": "NIC1",
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

    @attach_result("Login", "Login Successful", "Login Failed")
    def login(self, **kwargs):
        with allure.step("Login"):
            login_instance = Login()
            return login_instance.login(kwargs["ID"], kwargs["PW"])

    @attach_result("Sender Channel Creation", "Sender Channel Creation Successful", "Sender Channel Creation Failed")
    def create_sender_channel(self, **kwargs):
        channel_instance = ConfigureChannel(**kwargs)
        channel_instance.pre_channel_configuration()
        with allure.step("Create output"):
            channel_instance.setup_output()
            time.sleep(1)
        with allure.step("Create input"):
            channel_instance.setup_input()
        return channel_instance.post_channel_configuration()

    @attach_result(
        "Receiver Channel Creation", "Receiver Channel Creation Successful", "Receiver Channel Creation Failed"
    )
    def create_receiver_channel(self, **kwargs):
        kwargs = self.srt_receiver_configuration_data
        channel_instance = ConfigureChannel(**kwargs)
        channel_instance.pre_channel_configuration()
        with allure.step("Create output"):
            channel_instance.setup_output()
            time.sleep(1)
        with allure.step("Create input"):
            channel_instance.setup_input()
        return channel_instance.post_channel_configuration()

    @attach_result("Role Creation", "Role Creation Successful", "Role Creation Failed")
    def create_role(self, **kwargs):
        kwargs["Channel Name"] = [
            "UDP SRT Sender Testing",
            "UDP SRT Receiver Testing",
        ]
        with allure.step("Role Configuration"):
            role_instance = ConfigureRole()
            # Required parameters: Role Name, Channel Name
            return role_instance.configure_role(
                kwargs["Role Options"]["Name"], kwargs["Channel Name"][0], kwargs["Channel Name"][1]
            )

    @attach_result("Sender Channel Start", "Sender Channel Start Successful", "Sender Channel Start Failed")
    def sender_channel_start(self, **kwargs):
        with allure.step("Channel Start"):
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.sender_chidx = channel_info[1]
            time.sleep(10)
            if StatsReceiver().exec_multiprocessing(self.sender_chidx, kwargs["Channel Name"]):
                return channel_info[0]
            else:
                return False

    @attach_result("Receiver Channel Start", "Receiver Channel Start Successful", "Receiver Channel Start Failed")
    def receiver_channel_start(self, **kwargs):
        with allure.step("Channel Start"):
            kwargs = self.srt_receiver_configuration_data
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.receiver_chidx = channel_info[1]
            return channel_info[0]

    @attach_result("Receiver Channel Stats Request", "Channel Stats Request Successful", "Channel Stats Request Failed")
    def get_receiver_channel_stats(self, **kwargs):
        with allure.step("Get Channel Stats"):
            kwargs = self.srt_receiver_configuration_data
            # kwargs["Channel Name"] = "UDP SRT Receiver Testing"
            stats_instance = StatsReceiver()
            # Required parameters: Channel Index
            stats_result = stats_instance.exec_multiprocessing(self.receiver_chidx, kwargs["Channel Name"])
            # Multiprocessing 함수에서 출력하는 로그는 stdout에 안나오기 때문에 report에 직접 추가
            if type(stats_result[0]) == bool:
                allure.attach(
                    "\n".join(stats_result[1]),
                    name="Channel Stats Infomation",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return stats_result[0]
            else:
                MonitorDevice().channel_stop(self.receiver_chidx, stats_result)
                return False

    @attach_result("Sender Channel Stop", "Channel Stop Successful", "Channel Stop Failed")
    def sender_channel_stop(self, **kwargs):
        with allure.step("Channel Stop"):
            monitor_device_instance = MonitorDevice()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.sender_chidx, kwargs["Channel Name"])

    @attach_result("Receiver Channel Stop", "Channel Stop Successful", "Channel Stop Failed")
    def receiver_channel_stop(self, **kwargs):
        with allure.step("Channel Stop"):
            kwargs = self.srt_receiver_configuration_data
            monitor_device_instance = MonitorDevice()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.receiver_chidx, kwargs["Channel Name"])

    @allure.sub_suite("UDP/IP")
    @allure.title("UDP/IP SRT Input")
    def test_input_udp_srt(self):
        print("\n")
        test_functions = [
            # self.login,
            self.create_sender_channel,
            self.create_receiver_channel,
            self.create_role,
            self.sender_channel_start,
            self.receiver_channel_start,
            self.get_receiver_channel_stats,
            self.receiver_channel_stop,
            self.sender_channel_stop,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.srt_sender_configuration_data)
