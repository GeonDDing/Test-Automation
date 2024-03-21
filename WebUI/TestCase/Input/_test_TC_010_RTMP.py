import os
import sys
import time
import allure

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from configure_channels import ConfigureChannel
from configure_roles import ConfigureRole
from configure_groups import ConfigureGroup
from configure_devices import ConfigureDevice
from monitor_device import MonitorDevice
from stats_receiver import StatsReceiver
from login import Login


pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("RTMP Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Input")
class TestInputTRMP:
    rtmp_input_configuration_data = {
        "ID": "admin",
        "PW": "admin",
        "Role Options": {"Name": "UI Testing Role"},
        "Group Options": {"Name": "UI Testing Group", "Domain": "Live"},
        "Device Options": {
            "Name": "Local Device",
            "IP": "127.0.0.1",
        },
        "Channel Name": "RTMP Input Testing",
        "Input Type": "RTMP",
        "Output Type": "UDP",
        "Backup Source Type": None,
        "Preset Name": {
            "Videopreset Name": "1280x720 | H.264 | 29.97 | 4Mbps | Testing",
            "Audiopreset Name": "AAC | 128K | 48kHz | Testing",
        },
        "Input Options": {
            "URL": "rtmp://10.1.0.145:1935/live/rtmp_testing",
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "14005",
            "Primary Network Interface": "NIC1",
        },
        "Backup Source Options": None,
    }

    rtmp_output_configuration_data = {
        "Role Options": {"Name": "UI Testing Role"},
        "Channel Name": "RTMP Output Testing",
        "Input Type": "UDP",
        "Output Type": "RTMP",
        "Backup Source Type": None,
        "Preset Name": {
            "Videopreset Name": "1280x720 | H.264 | 29.97 | 4Mbps | Testing",
            "Audiopreset Name": "AAC | 128K | 48kHz | Testing",
        },
        "Input Options": {
            "Network URL": "224.30.30.10:15008",
            "Interface": "NIC2",
        },
        "Output Options": {
            "Broadcast Address": "10.1.0.145",
            "Broadcast Port": "1935",
            "Broadcast Path": "live",
            "Stream Name": "rtmp_testing",
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

    @attach_result("RTMP Input Channel Creation", "Channel Creation Successful", "Channel Creation Failed")
    def create_rtmp_input_channel(self, **kwargs):
        channel_instance = ConfigureChannel(**kwargs)
        channel_instance.pre_channel_configuration()
        with allure.step("Create output"):
            channel_instance.setup_output()
            time.sleep(1)
        with allure.step("Create input"):
            channel_instance.setup_input()
        return channel_instance.post_channel_configuration()

    @attach_result("RTMP Output Channel Creation", "Channel Creation Successful", "Channel Creation Failed")
    def create_rtmp_output_channel(self, **kwargs):
        kwargs = self.rtmp_output_configuration_data
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
            kwargs["Channel Name"] = [
                "RTMP Output Testing",
                "RTMP Input Testing",
            ]
            # Required parameters: Role Name, Channel Name
            return role_instance.configure_role(
                kwargs["Role Options"]["Name"], kwargs["Channel Name"][0], kwargs["Channel Name"][1]
            )

    @attach_result("Group Creation", "Group Creation Successful", "Group Creation Failed")
    def create_group(self, **kwargs):
        with allure.step("Group Configuration"):
            group_instance = ConfigureGroup()
            # Required parameters: Group Name, Domain
            return group_instance.configure_group(kwargs["Group Options"]["Name"], kwargs["Group Options"]["Domain"])

    @attach_result("Device Creation", "Device Creation Successful", "Device Creation Failed")
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

    @attach_result("Channel Start", "Channel Start Successful", "Channel Start Failed")
    def input_channel_start(self, **kwargs):
        with allure.step("Channel Start"):
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.input_chidx = channel_info[1]
            return channel_info[0]

    @attach_result("Channel Start", "Channel Start Successful", "Channel Start Failed")
    def output_channel_start(self, **kwargs):
        with allure.step("Channel Start"):
            kwargs["Channel Name"] = "RTMP Output Testing"
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.output_chidx = channel_info[1]
            time.sleep(10)
            return channel_info[0]

    @attach_result("Input Channel Stats Request", "Channel Stats Request Successful", "Channel Stats Request Failed")
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

    @attach_result("RTMP Input Channel Stop", "Channel Stop Successful", "Channel Stop Failed")
    def input_channel_stop(self, **kwargs):
        with allure.step("Channel Stop"):
            monitor_device_instance = MonitorDevice()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.input_chidx, kwargs["Channel Name"])

    @attach_result("RTMP Output Channel Stop", "Channel Stop Successful", "Channel Stop Failed")
    def output_channel_stop(self, **kwargs):
        with allure.step("Channel Stop"):
            kwargs["Channel Name"] = "RTMP Output Testing"
            monitor_device_instance = MonitorDevice()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.output_chidx, kwargs["Channel Name"])

    @allure.sub_suite("RTMP")
    @allure.title("RTMP Input")
    def test_input_rtmp(self):
        print("\n")
        test_functions = [
            # self.login,
            self.create_rtmp_input_channel,
            self.create_rtmp_output_channel,
            self.create_role,
            self.output_channel_start,
            self.input_channel_start,
            self.get_channel_stats,
            self.input_channel_stop,
            self.output_channel_stop,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.rtmp_input_configuration_data)


if __name__ == "__main__":
    tc = TestInputTRMP()
    tc.test_input_rtmp()
