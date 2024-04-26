import allure
from Pages.Configure.page_audiopresets import ConfigureAudiopreset
from Pages.Configure.page_videopresets import ConfigureVideopreset
from Pages.Configure.page_roles import ConfigureRole
from Pages.Configure.page_groups import ConfigureGroup
from Pages.Configure.page_devices import ConfigureDevice
from Pages.Login.page_login import Login
from Pages.Logout.page_logout import Logout

pytestmark = [allure.epic("WebUI Test Automation"), allure.feature("Settings")]


@allure.parent_suite("WebUI Test Automation")
@allure.suite("Settings")
class TestPreSettings:
    test_configuration_data = {
        "ID": "admin",
        "PW": "admin",
        "Role Options": {
            "Name": "UI Testing Role",
        },
        "Group Options": {
            "Name": "UI Testing Group",
            "Domain": "Live",
        },
        "Device Options": {
            "Name": "Local Device",
            "IP": "127.0.0.1",
        },
        "Channel Name": "Channel_001",
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
            "Network URL": "224.30.30.10:15008",
            "Interface": "NIC2",
        },
        "Output Options": {
            "Primary Output Address": "10.1.0.220",
            "Primary Output Port": "15001",
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
        "Group Creation",
        "Group Creation Successful",
        "Group Creation Failed",
    )
    def create_group(self, **kwargs):
        with allure.step("Group Configuration"):
            group_instance = ConfigureGroup()
            # Required parameters: Group Name, Domain
            return group_instance.configure_group(kwargs["Group Options"]["Name"], kwargs["Group Options"]["Domain"])

    @attach_result(
        "Device Creation",
        "Device Creation Successful",
        "Device Creation Failed",
    )
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

    @attach_result(
        "Logout",
        "Logout Successful",
        "Logout Failed",
    )
    def logout(self):
        with allure.step("Logout"):
            logout_instance = Logout()
            return logout_instance.logout()

    @allure.sub_suite("Settings")
    @allure.title("Pre Settings")
    def test_pre_setting(self):
        test_functions = [
            self.login,
            self.create_videopreset,
            self.create_audiopreset,
            self.create_role,
            self.create_group,
            self.create_device,
        ]

        for test_step_func in test_functions:
            test_step_func(**self.test_configuration_data)

        self.logout()


if __name__ == "__main__":
    test = TestPreSettings()
    test.test_pre_setting()
