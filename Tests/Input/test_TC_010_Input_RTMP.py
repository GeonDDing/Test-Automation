import time
import allure
from Pages.Configure.page_channels import ConfigureChannel
from Pages.Configure.page_roles import ConfigureRole
from Pages.Monitor.page_mdevice import MonitorDevice
from TestConfig.web_stats_receiver import StatsReceiver
from Pages.Login.page_login import Login
from Pages.Logout.page_logout import Logout

pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("RTMP Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Input")
class TestInputTRMP:
    rtmp_receiver_configuration_data = {
        "ID": "admin",
        "PW": "admin",
        "Role Options": {
            "Name": "UI Testing Role",
        },
        "Channel Name": "Input RTMP Receiver Testing",
        "Input Type": "RTMP",
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
            "URL": "rtmp://10.1.0.145:1935/live/rtmp_testing",
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "15010",
            "Primary Network Interface": "NIC1",
        },
        "Backup Source Options": None,
    }

    rtmp_sender_configuration_data = {
        "Role Options": {
            "Name": "UI Testing Role",
        },
        "Channel Name": "Input RTMP Sender Testing",
        "Input Type": "UDP",
        "Output Type": "RTMP",
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

    @attach_result(
        "Login",
        "Login Successful",
        "Login Failed",
    )
    def login(self, **kwargs):
        with allure.step("Login"):
            login_instance = Login()
            return login_instance.login(kwargs["ID"], kwargs["PW"])

    @attach_result(
        "RTMP Receiver Channel Creation",
        "Channel Creation Successful",
        "Channel Creation Failed",
    )
    def create_rtmp_receiver_channel(self, **kwargs):
        channel_instance = ConfigureChannel(**kwargs)
        is_pre = channel_instance.pre_channel_configuration()
        with allure.step("Output Options Setup"):
            is_output = channel_instance.setup_output()
            time.sleep(1)
        with allure.step("Input Options Setup"):
            is_input = channel_instance.setup_input()
        with allure.step("Channel Creation Finalization"):
            is_post = channel_instance.post_channel_configuration()
        if all((is_pre, is_output, is_input, is_post)):
            return True
        else:
            return False

    @attach_result(
        "RTMP Sender Channel Creation",
        "Channel Creation Successful",
        "Channel Creation Failed",
    )
    def create_rtmp_sender_channel(self, **kwargs):
        kwargs = self.rtmp_sender_configuration_data
        channel_instance = ConfigureChannel(**kwargs)
        is_pre = channel_instance.pre_channel_configuration()
        with allure.step("Output Options Setup"):
            is_output = channel_instance.setup_output()
            time.sleep(1)
        with allure.step("Input Options Setup"):
            is_input = channel_instance.setup_input()
        with allure.step("Channel Creation Finalization"):
            is_post = channel_instance.post_channel_configuration()
        if all((is_pre, is_output, is_input, is_post)):
            return True
        else:
            return False

    @attach_result(
        "Role Creation",
        "Role Creation Successful",
        "Role Creation Failed",
    )
    def create_role(self, **kwargs):
        with allure.step("Role Configuration"):
            role_instance = ConfigureRole()
            # Required parameters: Role Name, Channel Name
            return role_instance.configure_role(
                kwargs["Role Options"]["Name"],
                self.rtmp_receiver_configuration_data["Channel Name"],
                self.rtmp_sender_configuration_data["Channel Name"],
            )

    @attach_result(
        "RTMP Receiver Channel Start",
        "Channel Start Successful",
        "Channel Start Failed",
    )
    def input_channel_start(self, **kwargs):
        with allure.step("RTMP Receiver Channel Start"):
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.input_chidx = channel_info[1]
            return channel_info[0]

    @attach_result(
        "RTMP Sender Channel Start",
        "Channel Start Successful",
        "Channel Start Failed",
    )
    def output_channel_start(self, **kwargs):
        kwargs = self.rtmp_sender_configuration_data
        with allure.step("RTMP Sender Channel Start"):
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.output_chidx = channel_info[1]

            if StatsReceiver().exec_multiprocessing(self.output_chidx, kwargs["Channel Name"]):
                return channel_info[0]
            else:
                return False

    @attach_result(
        "RTMP Receiver Channel Stats Request", "Channel Stats Request Successful", "Channel Stats Request Failed"
    )
    def get_channel_stats(self, **kwargs):
        with allure.step("Get RTMP Receiver Channel Stats"):
            stats_instance = StatsReceiver()
            # Required parameters: Channel Index
            stats_result = stats_instance.exec_multiprocessing(self.input_chidx, kwargs["Channel Name"])
            if type(stats_result[0]) == bool:
                allure.attach(
                    "\n".join(stats_result[1]),
                    name="Channel Stats Infomation",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return stats_result[0]
            else:
                MonitorDevice().channel_stop(self.input_chidx, stats_result)
                return False

    @attach_result(
        "RTMP Receiver Channel Stop",
        "Channel Stop Successful",
        "Channel Stop Failed",
    )
    def input_channel_stop(self, **kwargs):
        with allure.step("RTMP Receiver Channel Stop"):
            monitor_device_instance = MonitorDevice()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.input_chidx, kwargs["Channel Name"])

    @attach_result(
        "RTMP Sender Channel Stop",
        "Channel Stop Successful",
        "Channel Stop Failed",
    )
    def output_channel_stop(self, **kwargs):
        kwargs = self.rtmp_sender_configuration_data
        with allure.step("RTMP Sender Channel Stop"):
            monitor_device_instance = MonitorDevice()
            start_result = bool()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.output_chidx, kwargs["Channel Name"])

    @attach_result(
        "Logout",
        "Logout Successful",
        "Logout Failed",
    )
    def logout(self):
        with allure.step("Logout"):
            logout_instance = Logout()
            return logout_instance.logout()

    @allure.sub_suite("RTMP")
    @allure.title("RTMP")
    def test_input_rtmp(self):
        test_functions = [
            self.login,
            self.create_rtmp_receiver_channel,
            self.create_rtmp_sender_channel,
            self.create_role,
            self.output_channel_start,
            self.input_channel_start,
            self.get_channel_stats,
            self.input_channel_stop,
            self.output_channel_stop,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.rtmp_receiver_configuration_data)

        self.logout()
