# test_execute.py
from configure_roles import ConfigureRole
from configure_devices import ConfigureDevice
from configure_groups import ConfigureGroup
from configure_channels import ConfigureChannel
from configure_audiopresets import ConfigureAudiopreset
from configure_videopresets import ConfigureVideopreset
from configure_tasks import ConfigureTask
from login import Login
from webdriver_method import WebDriverMethod
from datetime import datetime
import sys


preset_name = {
    "Videopreset Name": "1280x720 | H.264 | 29.97 | 4Mbps | Testing",
    "Audiopreset Name": "AAC | 128K | 48kHz | Testing",
}

videopreset_options = {
    "Codec": "H.264/AVC1",
    "Encoding engine": "S/W codec",
    "Resolution": "1280 x 720 (HD 720x)",
    "Frame Rate": "29.97",
    "# of B frames": "2",
    "Bitrate": "4000",
    "I-Frame Interval": "60",
    "Buffering Time": "120",
}

audiopreset_options = {
    "Codec": "AAC",
    "MPEG version": "MPEG4",
    "Profile": "Default",
    "Channels": "Stereo",
    "Sampling Rate": "48000",
    "Bitrate": "128",
}
input_udp_options = {
    "Network URL": "224.30.30.10:15008",
    "Interface": "NIC1",
    "Enable TS over RTP": False,
    "Enable SRT": True,
    "Max input Mbps": "10",
    "Enable HA Mode": "Disabled",
    "Program Selection Mode": "PIDs",
    "Video ID": "1024",
    "Audio ID": "1025",
}

input_sdi_options = {"Signal type": "SDI", "Teletext page": "692", "VBI lines": "1"}

input_playlist_options = {"Type": "Local Static Playlist", "Playlists name": "kt_tvn"}

output_udp_options = {
    "Primary Output Address": "10.1.0.220",
    "Primary Output Port": "19005",
    "Primary Network Interface": "NIC1",
    "Service Name": "testing",
}

output_hls_options = {
    "Segment Naming": "Start Time+Sequential",
    "Duration": "2",
    "Segments ring size": "5",
    "Primary Master playlist path": "videos/ch@@CHIDX@@/",
    "Master playlist name": "master.m3u8",
}

task_options = {
    "Group": "LiveGroup",
    "Channel": "Playlist Testing Channel",
    "Task": "Start channel",
    "Date": datetime.now().strftime("%Y-%m-%d"),
    "Time": datetime.now().strftime("%H:%M:%S"),
    "State": "Enabled",
}

if __name__ == "__main__":
    login_instance = Login()
    device_instance = ConfigureDevice()
    group_instance = ConfigureGroup()
    role_instance = ConfigureRole()
    channel_instance = ConfigureChannel()
    audiopreset_instance = ConfigureAudiopreset()
    videopreset_instance = ConfigureVideopreset()
    task_instance = ConfigureTask()

    login_instance.login("admin", "admin")
    # audiopreset_instance.configure_audiopreset(
    #     preset_name["Audiopreset Name"], audiopreset_options
    # )
    videopreset_instance.configure_videopreset(preset_name["Videopreset Name"], videopreset_options)

    channel_instance.configure_channel(
        "UDP Testing Channel",
        "UDP/IP",
        "TS UDP/IP",
        None,
        input_udp_options,
        output_udp_options,
        None,
    )

    # channel_instance.configure_channel(
    #     "test_channel",
    #     "SDI",
    #     "UDP/IP",
    #     None,
    #     input_sdi_options,
    #     output_udp_options,
    #     None,
    #     preset_name,
    # )

    # channel_instance.configure_channel(
    #     'Playlist Testing Channel', 'Playlist', 'HLS', None, input_playlist_options, output_hls_options, None, preset_name)

    # role_instance.configure_role('test role', 'UDP Testing Channel')
    # group_instance.configure_group('test group', 'live')
    # device_instance.configure_device(
    #     "Local Device", '10.1.0.145', 'test group', 'test role')
    # task_instance.configure_task('New task testing', task_options)

    WebDriverMethod().quit_driver()
