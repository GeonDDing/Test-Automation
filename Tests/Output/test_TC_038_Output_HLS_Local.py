import time
import allure
from Pages.Configure.page_channels import ConfigureChannel
from Pages.Configure.page_roles import ConfigureRole
from Pages.Monitor.page_monitor_device import MonitorDevice
from TestConfig.web_stats_receiver import StatsReceiver
from Pages.Login.page_login import Login
from Pages.Logout.page_logout import Logout

pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("HLS Output")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Output")
class TestOutputHLSLocal:
    test_configuration_data = {
        "ID": "admin",
        "PW": "admin",
        "Role Options": {
            "Name": "UI Testing Role",
        },
        "Channel Name": "Output HSL Local Testing",
        "Input Type": "Playlist",
        "Output Type": "HLS",
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
            "Type": "Local Static Playlist",
            "Playlists name": "bbb",
        },
        "Output Options": {
            "Duration": "2",
            "Segments ring size": "15",
            "Primary Master playlist path": "videos/test_automation_@@CHIDX@@/",
            "Master playlist name": "master.m3u8",
            'Append "ENDLIST" at Stop': True,
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
        "Channel Creation",
        "Channel Creation Successful",
        "Channel Creation Failed",
    )
    def create_channel(self, **kwargs):
        channel_instance = ConfigureChannel(**kwargs)
        is_pre = channel_instance.pre_channel_configuration()
        with allure.step("Output Options Setup"):
            is_output = channel_instance.setup_output()
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
            return role_instance.configure_role(kwargs["Role Options"]["Name"], kwargs["Channel Name"])

    @attach_result(
        "Channel Start",
        "Channel Start Successful",
        "Channel Start Failed",
    )
    def channel_start(self, **kwargs):
        with allure.step("Channel Start"):
            monitor_device_instance = MonitorDevice()
            channel_info = list()
            # Required parameters: Channel Name
            channel_info = monitor_device_instance.channel_start(kwargs["Channel Name"])
            self.chidx = channel_info[1]
            return channel_info[0]

    @attach_result(
        "Channel Stats Request",
        "Channel Stats Request Successful",
        "Channel Stats Request Failed",
    )
    def get_channel_stats(self, **kwargs):
        with allure.step("Get Channel Stats"):
            stats_instance = StatsReceiver()
            # Required parameters: Channel Index
            stats_result = stats_instance.exec_multiprocessing(self.chidx, kwargs["Channel Name"])
            if type(stats_result[0]) == bool:
                allure.attach(
                    "\n".join(stats_result[1]),
                    name="Channel Stats Infomation",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return stats_result[0]
            else:
                MonitorDevice().channel_stop(self.chidx, stats_result)
                return False

    @attach_result(
        "Channel Stop",
        "Channel Stop Successful",
        "Channel Stop Failed",
    )
    def channel_stop(self, **kwargs):
        with allure.step("Channel Stop"):
            monitor_device_instance = MonitorDevice()
            # Required parameters: Channel Name
            return monitor_device_instance.channel_stop(self.chidx, kwargs["Channel Name"])

    @attach_result(
        "Logout",
        "Logout Successful",
        "Logout Failed",
    )
    def logout(self):
        with allure.step("Logout"):
            logout_instance = Logout()
            return logout_instance.logout()

    @allure.sub_suite("HLS")
    @allure.title("Local")
    def test_output_hls_local(self):
        print("\n")
        test_functions = [
            self.login,
            self.create_channel,
            self.create_role,
            self.channel_start,
            self.get_channel_stats,
            self.channel_stop,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.test_configuration_data)

        self.logout()
