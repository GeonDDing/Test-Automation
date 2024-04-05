import time
import allure
from configure_channels import ConfigureChannel
from configure_roles import ConfigureRole
from monitor_device import MonitorDevice
from stats_receiver import StatsReceiver
from settings_networking import SettingsNetworking


pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("Playlist Input")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Input")
class TestInputPlaylistNielsenID3:
    test_configuration_data = {
        "ID": "admin",
        "PW": "admin",
        "Role Options": {
            "Name": "UI Testing Role",
        },
        "Channel Name": "Input Playlist Nielsen ID3 Testing",
        "Input Type": "Playlist",
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
            "Nielsen ID3": True,
            "Distributor ID": "Playlist ID3",
        },
        "Input Options": {
            "Type": "Local Static Playlist",
            "Playlists name": "bbb",
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "15016",
            "Primary Network Interface": "NIC1",
        },
        "Backup Source Options": None,
        "Networking": {
            "Services Options": {
                "SMB path": "smb://mek:mediaExcel5@10.1.0.10/mek",
            },
        },
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

    @attach_result("Network Setting", "Network Setting Successful", "Network Setting Failed")
    def set_network(self, **kwargs):
        with allure.step("SMB Setting"):
            network_instance = SettingsNetworking()
            return network_instance.networking_services(kwargs["Networking"]["Services Options"])

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

    @allure.sub_suite("Playlist")
    @allure.title("Nielsen ID3")
    def test_input_playlist_nielsen_id3(self):
        print("\n")
        test_functions = [
            self.set_network,
            self.create_channel,
            self.create_role,
            self.channel_start,
            self.get_channel_stats,
            self.channel_stop,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.test_configuration_data)