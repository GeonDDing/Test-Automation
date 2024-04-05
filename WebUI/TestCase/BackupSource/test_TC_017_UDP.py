import time
import allure
from configure_audiopresets import ConfigureAudiopreset
from configure_videopresets import ConfigureVideopreset
from configure_channels import ConfigureChannel
from configure_roles import ConfigureRole
from monitor_device import MonitorDevice
from stats_receiver import StatsReceiver


pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("UDP/IP BackupSource")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("BackupSource")
class TestBackupSourceUDP:
    chidx = int()
    test_configuration_data = {
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
        "Channel Name": "Backup Source UDP Testing",
        "Input Type": "Playlist",
        "Output Type": "UDP",
        "Backup Source Type": "UDP",
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
            "Type": "Local Static Playlist",
            "Playlists name": "bbb",
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "15017",
            "Primary Network Interface": "NIC1",
        },
        "Backup Source Options": {
            "Network URL": "224.30.30.10:17009",
            "Interface": "NIC2",
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

    @attach_result(
        "Video Preset Creation",
        "Video Preset Creation Successful",
        "Video Preset Creation Failed",
    )
    def create_videopreset(self, **kwargs):
        with allure.step("Create video preset"):
            videopreset_instance = ConfigureVideopreset()
            # Required parameters: Videopreset Name, Videopreset Options
            return videopreset_instance.configure_videopreset(
                kwargs["Preset Name"]["Videopreset Name"], kwargs["Videopreset Options"]
            )

    @attach_result(
        "Audio Preset Creation",
        "Audio Preset Creation Successful",
        "Audio Preset Creation Failed",
    )
    def create_audiopreset(self, **kwargs):
        with allure.step("Create audio preset"):
            audiopreset_instance = ConfigureAudiopreset()
            # Required parameters: Audiopreset Name, Audiopreset Options
            return audiopreset_instance.configure_audiopreset(
                kwargs["Preset Name"]["Audiopreset Name"], kwargs["Audiopreset Options"]
            )

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
        with allure.step("Backup Source "):
            is_backup_source = channel_instance.setup_backups_source()
        if all((is_pre, is_output, is_input, is_post, is_backup_source)):
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
        "Primary Source Stats Request",
        "Primary Source Stats Request Successful",
        "Primary Source Stats Request Failed",
    )
    def get_primary_source_channel_stats(self, **kwargs):
        with allure.step("Primary Source Stats"):
            stats_instance = StatsReceiver()
            # Required parameters: Channel Index
            stats_result = stats_instance.exec_multiprocessing(self.chidx, kwargs["Channel Name"])
            if type(stats_result[0]) == bool:
                allure.attach(
                    "\n".join(stats_result[1]),
                    name="Primary Source Stats Infomation",
                    attachment_type=allure.attachment_type.TEXT,
                )
                return stats_result[0]
            else:
                MonitorDevice().channel_stop(self.chidx, stats_result)
                return False

    @attach_result(
        "Switch Backup Source",
        "Switch Backup Source Successful",
        "Switch Backup Source Failed",
    )
    def switch_source(self, **kwargs):
        with allure.step("Switch Backup Source"):
            channel_instance = ConfigureChannel(**kwargs)
            return channel_instance.switch_backup_source(self.chidx)

    @attach_result(
        "Backup Source Stats Request",
        "Backup Source Stats Request Successful",
        "Backup Source Stats Request Failed",
    )
    def get_backup_source_channel_stats(self, **kwargs):
        with allure.step("Backup Source Stats"):
            stats_instance = StatsReceiver()
            # Required parameters: Channel Index
            stats_result = stats_instance.exec_multiprocessing(self.chidx, kwargs["Channel Name"])
            if type(stats_result[0]) == bool:
                allure.attach(
                    "\n".join(stats_result[1]),
                    name="Backup Source Stats Infomation",
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

    @allure.sub_suite("UDP/IP")
    @allure.title("UDP/IP")
    def test_backup_source_udp(self):
        print("\n")
        test_functions = [
            #
            # self.create_videopreset,
            # self.create_audiopreset,
            self.create_channel,
            self.create_role,
            self.channel_start,
            self.get_primary_source_channel_stats,
            self.switch_source,
            self.get_backup_source_channel_stats,
            self.channel_stop,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.test_configuration_data)
