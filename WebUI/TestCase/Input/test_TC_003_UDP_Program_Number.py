import os
import sys
import time
import allure

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from configure_channels import ConfigureChannel
from configure_roles import ConfigureRole
from monitor_device import MonitorDevice
from stats_receiver import StatsReceiver
from login import Login


pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("UDP/IP Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Input")
class TestInputUDPProgramNumber:
    test_configuration_data = {
        "ID": "admin",
        "PW": "admin",
        "Role Options": {"Name": "UI Testing Role"},
        "Group Options": {"Name": "UI Testing Group", "Domain": "Live"},
        "Device Options": {
            "Name": "Local Device",
            "IP": "127.0.0.1",
        },
        "Channel Name": "UDP Program Number Input Testing",
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
            "Program Selection Mode": "Program number",
            "Program Number": "1010",
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "19007",
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

    @attach_result("Channel Creation", "Channel Creation Successful", "Channel Creation Failed")
    def create_channel(self, **kwargs):
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
        with allure.step("Role Configuration"):
            role_instance = ConfigureRole()
            # Required parameters: Role Name, Channel Name
            return role_instance.configure_role(kwargs["Role Options"]["Name"], kwargs["Channel Name"])

    @attach_result("Channel Start", "Channel Start Successful", "Channel Start Failed")
    def channel_start(self, **kwargs):
        with allure.step("Channel Start"):
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.chidx = channel_info[1]
            return channel_info[0]

    @attach_result("Channel Stats Request", "Channel Stats Request Successful", "Channel Stats Request Failed")
    def get_channel_stats(self, **kwargs):
        with allure.step("Get Channel Stats"):
            stats_instance = StatsReceiver()
            # Required parameters: Channel Index
            stats_result = stats_instance.exec_multiprocessing(self.chidx, kwargs["Channel Name"])
            if type(stats_result) == bool:
                return stats_result
            else:
                MonitorDevice().channel_stop(self.chidx, stats_result)
                return False

    @attach_result("Channel Stop", "Channel Stop Successful", "Channel Stop Failed")
    def channel_stop(self, **kwargs):
        with allure.step("Channel Stop"):
            monitor_device_instance = MonitorDevice()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.chidx, kwargs["Channel Name"])

    @allure.sub_suite("UDP/IP")
    @allure.title("UDP/IP Prpgram Number Input")
    def test_input_udp_program_number(self):
        print("\n")
        test_functions = [
            self.create_channel,
            self.create_role,
            self.channel_start,
            self.get_channel_stats,
            self.channel_stop,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.test_configuration_data)


if __name__ == "__main__":
    test = TestInputUDPProgramNumber()
    test.test_input_udp_program_number()
