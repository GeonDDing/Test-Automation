# from webdriver_method import WebDriverMethod
import allure
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from configure_roles import ConfigureRole
from configure_devices import ConfigureDevice
from configure_groups import ConfigureGroup
from configure_channels import Configurechannel
from configure_audiopresets import ConfigureAudiopreset
from configure_videopresets import ConfigureVideopreset
from configure_tasks import ConfigureTask
from login import Login

# login_instance = Login()
# device_instance = ConfigureDevice()
# group_instance = ConfigureGroup()
# role_instance = ConfigureRole()
# channel_instance = Configurechannel()
# audiopreset_instance = ConfigureAudiopreset()
# videopreset_instance = ConfigureVideopreset()
# task_instance = ConfigureTask()


pytestmark = [allure.epic("Testing Automation"), allure.feature("UDP/IP Input")]

profile_name = {
    "Videopreset Name": "1280x720 | H.264 | 29.97 | 4Mbps | Testing",
    "Audiopreset Name": "AAC | 128K | 48kHz | Testing",
}

videopreset = {
    "Codec": "H.264/AVC",
    "Encoding engine": "S/W codec",
    "Resolution": "1280 x 720 (HD 720x)",
    "Frame Rate": "29.97",
    "# of B frames": "2",
    "Bitrate": "4000",
    "I-Frame Interval": "60",
    "Buffering Time": "120",
}

audiopreset = {
    "Codec": "AAC",
    "MPEG version": "MPEG4",
    "Profile": "Default",
    "Channels": "Stereo",
    "Sampling Rate": "48000",
    "Bitrate": "128",
}


# @allure.step("로그인")
# def login_step(id, pwd):
#     with allure.step("Login"):
#         login_status = bool()
#         test_result = str()
#         login_instance = Login()
#         login_status = login_instance.login(id, pwd)
#         if login_status[0]:
#             allure.attach(
#                 "Login 성공",
#                 name="Login",
#                 attachment_type=None,
#             )
#             test_result = "TEST PASS"
#         else:
#             allure.attach(
#                 "Login 실패",
#                 name="Login",
#                 attachment_type=None,
#             )
#             test_result = "TEST FAIL"
#         assert login_status[0], test_result


# @allure.step("Video Profile 생성")
# def videoprest_setp(profile_name, videopreset_options):
#     with allure.step("Create Video Profile"):
#         videopreset_status = bool()
#         test_result = str()
#         videopreset_instance = ConfigureVideopreset()
#         videopreset_status = videopreset_instance.configure_videopreset(
#             profile_name, videopreset_options
#         )
#         if videopreset_status[0]:
#             allure.attach(
#                 "Video Profile 생성 완료",
#                 name="Video Profile 생성",
#                 attachment_type=None,
#             )
#             test_result = "TEST PASS"
#         else:
#             allure.attach(
#                 "Video Profile 생성 실패",
#                 name="Video Profile 생성",
#                 attachment_type=None,
#             )
#             test_result = "TEST FAIL"
#         assert videopreset_status[0], test_result


# # @pytest.mark.parametrize("id,pwd", [("admin", "admin"), ("admin1", "admin")])
# @allure.title("UDP/IP Multicast Input")
# def test_udp_input():
#     login_step("admin", "admin1")
#     videoprest_setp(profile_name["Videopreset Name"], videopreset)


@allure.step("로그인")
def login_step(id, pwd):
    with allure.step("Login"):
        login_instance = Login()
        login_status = login_instance.login(id, pwd)
        if login_status[0]:
            allure.attach("Login 성공", name="Login", attachment_type=None)
            assert login_status[0], "TEST PASS"
        else:
            allure.attach("Login 실패", name="Login", attachment_type=None)
            assert login_status[0], "TEST FAIL"


@allure.step("Video Preset 생성")
def videopreset_step(profile_name, videopreset_options):
    with allure.step("Video Preset"):
        videopreset_instance = ConfigureVideopreset()
        videopreset_status = videopreset_instance.configure_videopreset(
            profile_name, videopreset_options
        )
        if videopreset_status[0]:
            allure.attach(
                "Video Preset 생성 성공",
                name="Video Preset 생성",
                attachment_type=None,
            )
            assert videopreset_status[0], "TEST PASS"
        else:
            allure.attach(
                "Video Preset 생성 실패",
                name="Video Preset 생성",
                attachment_type=None,
            )
            assert videopreset_status[0], "TEST FAIL"


@allure.title("UDP/IP Multicast Input")
def test_udp_input():
    login_step("admin", "admin")
    videopreset_step(profile_name["Videopreset Name"], videopreset)
