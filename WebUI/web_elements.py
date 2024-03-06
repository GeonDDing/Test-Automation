class GaGaWebElements:
    # XPATH
    gaga_active_stream_table = "/html/body/div/table[1]"
    gaga_stream_in_table = "/html/body/div/table[3]"

    # Repositories Link
    gaga_repositories_nana_server = "/html/body/div/li/a[1]"
    gaga_repositories_home = "/html/body/div/li/a[2]"
    gaga_repositories_local_streams = "/html/body/div/li/a[3]"

    # CSS Selectorß
    gaga_stream_cast_to = 'input[type="text"][id="dst"]'
    gaga_start_streaming_button = 'input[type="button"][value="Start Streaming"]'


class LoginElements:
    ### CSS Selector ###
    login = 'input[type="text"][name="login"]'
    password = 'input[type="password"][name="password"]'
    login_button = '.grey-button[type="submit"][value="Login"]'


class MainMenuElements:
    monitor, configure, events, settings = [f'//*[@id="page-menu-inner"]/a[{i}]' for i in range(1, 5)]
    (
        configure_groups,
        configure_devices,
        configure_roles,
        configure_channels,
        configure_video_presets,
        configure_audio_presets,
        configure_tasks,
        configure_file_jobs,
        configure_watch_folders,
    ) = [f'//*[@id="page-submenu-inner"]/div/a[{i}]' for i in range(1, 10)]

    (
        settings_mgmtsys_settings,
        settings_events,
        settings_event_action,
        settings_maintenance,
        settings_update,
        settings_networking,
        settings_source_replacement,
    ) = [f'//*[@id="page-submenu-inner"]/div/a[{i}]' for i in range(1, 8)]


class EventElements:
    event_delete_all_button = 'input[type="submit"][name="deleteAll"][value="Delete All"]'
    event_save_to_csv_file_button = 'input[type="submit"][name="savetocsv"][value="Save to a CSV file"]'


class ConfigureGroupElements:
    ### XPATH ###
    # Group table XPATH
    group_table = '//*[@id="page-body-inner"]/div[2]/div[1]/table'

    ### CSS Selector ###
    group_add_button = 'input.black-button[title="Click to add a new group"]'
    group_save_button = 'input.black-button[type="submit"][name="action"][value="Save"]'
    group_name = 'input[type="text"][name="Name"]'
    group_domain = 'input[type="radio"][name="domain"]'
    group_live_trigger_evergreen0 = (
        'input[class="inputbox"][type="radio"][name="/group/FailoverPolicy/onInputLinkFailure"][value="0"]'
    )
    group_live_trigger_evergreen1 = (
        'input[class="inputbox"][type="radio"][name="/group/FailoverPolicy/onInputLinkFailure"][value="2"]'
    )
    group_live_trigger_none = (
        'input[class="inputbox"][type="radio"][name="/group/FailoverPolicy/onInputLinkFailure"][value="1"]'
    )
    group_live_link_loss_continue = (
        'input[class="inputbox"][type="radio"][name="/group/FailoverPolicy/onMgtLinkFailure"][value="0"]'
    )
    group_live_link_loss_stop = (
        'input[class="inputbox"][type="radio"][name="/group/FailoverPolicy/onMgtLinkFailure"][value="1"]'
    )
    group_default_event_configuration_button = 'input[type="submit"][name="action][value="Set to default"]'
    group_error = "#errorMessage"


class ConfigureDeviceElements:
    ### XPATH ###
    device_table = '//*[@id="page-body-inner"]/div[2]/div[1]/table'

    ### CSS Selector ###
    device_add_button = 'input.black-button[type="button"][value="Add"]'
    device_save_button = 'input.black-button[type="submit"][name="action"][value="Save"]'
    device_name = 'input[type="text"][name="Name"]'
    device_ip_address = 'input[type="text"][id="host"][name="host"]'
    device_include_group = 'select[name="groupId"]'
    device_include_role = 'select[id="rolesel"][name="roleId"]'
    device_error = "#errorMessage"


class ConfigureRoleElements:
    ### CSS Selector ###
    role_name = 'input[type="text"][name="Name"]'
    role_add_button = 'input.black-button[type="button"][value="Add"]'
    role_save_button = 'input.black-button[type="submit"][name="action"][value="Save"]'

    ### XPATH ###
    add_channel_list = '//*[@id="channelAdd"]'
    role_table = '//*[@id="page-body-inner"]/div[2]/div[1]/table'


class ConfigureChannelElements:
    ### XPATH ###
    channel_table = '//*[@id="page-body-inner"]/div[2]/div[1]/table'

    ### CSS Selector ##
    channel_name = 'input[type="text"][name="Name"]'
    channel_add_button = 'input.black-button[type="button"][value="Add"]'
    channel_import_button = 'input.black-button[type="button"][value="Import"]'
    channel_save_button = 'input.black-button[type="submit"][name="action"][value="Save"]'
    channel_delete_button = 'input.black-button[type="submit"][name="action"][value="Delete"]'
    channel_copy_button = 'input.black-button[type="submit"][name="action"][value="Copy"]'
    channel_export_button = 'input.black-button[type="submit"][name="action"][value="Export"]'


class ConfigureInputElements:
    ### CSS Selector ###
    input_type = 'select[id="/source/sourceType"][name="/source/sourceType"]'
    input_common_modulated_audio_track = 'select[id="/source/modulatedAudioTrack"][name="/source/modulatedAudioTrack"]'
    input_common_start_with_evergreen = (
        'input[type="checkbox"][id="/source/enableIdleStart"][name="/source/enableIdleStart"]'
    )
    input_common_evergreen_timeout = (
        'input[type="text"][id="/source/inputBufferingTimeMSeconds"][name="/source/inputBufferingTimeMSeconds"]'
    )
    input_common_analysis_window = (
        'input[type="text"][id="/source/analysisWindowLength"][name="/source/analysisWindowLength"]'
    )
    input_common_nielsen_id3 = 'input[type="checkbox"][id="/source/enableNielsenID3"][name="/source/enableNielsenID3"]'
    input_common_distributor_id = (
        'input[type="text"][id="/source/nielsenDistributorID"][name="/source/nielsenDistributorID"]'
    )
    input_common_error_message = "#errorMessage"

    # UDP Options CSS Selector
    input_udp_network_url = (
        'input[type="text"][id="/source/mpeg2/netConfig/networkUrl"][name="/source/mpeg2/netConfig/networkUrl"]'
    )
    input_udp_interface = 'select[id="/source/mpeg2/netConfig/interfaceId"][name="/source/mpeg2/netConfig/interfaceId"]'
    input_udp_enable_ts_over_rtp = (
        'input[type="checkbox"][id="/source/mpeg2/enableTsOverRtp"][name="/source/mpeg2/enableTsOverRtp"]'
    )
    input_udp_max_input_mbps = 'input[type="text"][id="/source/mpeg2/netConfig/maxInputBitrateMbps"][name="/source/mpeg2/netConfig/maxInputBitrateMbps"]'
    input_udp_enable_ha_mode = (
        'select[id="/source/mpeg2/enableHighAvailabilityMode"][name="/source/mpeg2/enableHighAvailabilityMode"]'
    )

    # SRT sub options CSS Selector
    input_udp_enable_srt = 'input[type="checkbox"][id="/source/mpeg2/enableSrt"][name="/source/mpeg2/enableSrt"]'
    input_udp_latency = 'input[type="text"][id="/source/mpeg2/srtLatency"][name="/source/mpeg2/srtLatency"]'
    input_udp_password = 'input[type="text"][id="/source/mpeg2/srtPassphrase"][name="/source/mpeg2/srtPassphrase"]'
    input_udp_crypto_key_length = 'select[id="/source/mpeg2/srtPbkeylen"][name="/source/mpeg2/srtPbkeylen"]'
    input_udp_advanced_parmaneters = (
        'input[type="text"][id="/source/mpeg2/srtAdvancedParameters"][name="/source/mpeg2/srtAdvancedParameters"]'
    )

    # Program Selection Mode sub options CSS Selector
    input_udp_program_selection_mode = (
        'select[id="/source/mpeg2/programSelectionMode"][name="/source/mpeg2/programSelectionMode"]'
    )
    input_udp_video_id = 'input[type="text"][id="/source/videoId"][name="/source/videoId"]'
    input_udp_audio_id = 'input[type="text"][id="/source/audioId"][name="/source/audioId"]'
    input_udp_program_number = (
        'input[type="text"][id="/source/mpeg2/programNumber"][name="/source/mpeg2/programNumber"]'
    )
    input_udp_service_name = 'input[type="text"][id="/source/mpeg2/serviceName"][name="/source/mpeg2/serviceName"]'

    # RTP Options CSS Selector
    input_rtp_sdp_file = 'input[type="text"][id="/source/rtp/sdpFile"][name="/source/rtp/sdpFile"]'

    # RTMP Options CSS Selector
    input_rtmp_url = 'input[type="text"][id="/source/rtmp/url"][name="/source/rtmp/url"]'

    # HLS Options CSS Selector
    input_hls_url = 'input[type="text"][id="/source/hls/url"][name="/source/hls/url"]'

    # Playlist Options CSS Selector
    input_playlist_type = 'select[id="/source/fileList/type"][name="/source/fileList/type"]'
    input_playlist_playlists_name = 'select[id="/source/fileList/fileName"][name="/source/fileList/fileName"]'
    input_playlist_clipcasting_uri = 'input[type="text"][id="/source/fileList/url"][name="/source/fileList/url"]'
    input_playlist_remote_media_asset_uri = 'input[type="text"][id="/source/fileList/url"][name="/source/fileList/url"]'
    input_playlist_recurring_the_last_n_files = (
        'input[type="text"][id="/source/fileList/recurring"][name="/source/fileList/recurring"]'
    )
    input_playlist_sort_by = 'select[id="/source/fileList/sortMode"][name="/source/fileList/sortMode"]'

    # SMPTE ST 2110 Options CSS Selector
    input_smpte_st_2110_video_sdp_url = (
        'input[type="text"][id="/source/st2110/video/sdpUrl"][name="/source/st2110/video/sdpUrl"]'
    )
    input_smpte_st_2110_video_first_nic = (
        'select[id="/source/st2110/video/interfaceId"][name="/source/st2110/video/interfaceId"]'
    )
    input_smpte_st_2110_video_second_nic = (
        'select[id="/source/st2110/video/secondInterfaceId"][name="/source/st2110/video/secondInterfaceId"]'
    )
    input_smpte_st_2110_audio_sdp_url = (
        'input[type="text"][id="/source/st2110/audio/sdpUrl"][name="/source/st2110/audio/sdpUrl"]'
    )
    input_smpte_st_2110_audio_first_nic = (
        'select[id="/source/st2110/audio/interfaceId"][name="/source/st2110/audio/interfaceId"]'
    )
    input_smpte_st_2110_audio_second_nic = (
        'select[id="/source/st2110/audio/secondInterfaceId"][name="/source/st2110/audio/secondInterfaceId"]'
    )
    input_smpte_st_2110_ancillary_sdp_url = (
        'input[type="text"][id="/source/st2110/anc/sdpUrl"][name="/source/st2110/anc/sdpUrl"]'
    )
    input_smpte_st_2110_ancillary_first_nic = (
        'select[id="/source/st2110/anc/interfaceId"][name="/source/st2110/anc/interfaceId"]'
    )
    input_smpte_st_2110_ancillary_second_nic = (
        'select[id="/source/st2110/anc/secondInterfaceId"][name="/source/st2110/anc/secondInterfaceId"]'
    )

    # NDI Options CSS Selector
    input_ndi_name = 'input[type="text"][id="/source/ndi/sourceNameToConnect"][name="/source/ndi/sourceNameToConnect"]'
    input_ndi_group = 'input[type="text"][id="/source/ndi/groupName"][name="/source/ndi/groupName"]'
    input_ndi_url = 'input[type="text"][id="/source/ndi/url"][name="/source/ndi/url"]'

    # SDI Options CSS Selector
    input_sdi_signal_type = 'select[id="/source/sdi/signalType"][name="/source/sdi/signalType"]'
    input_sdi_video_format = 'select[id="/source/sdi/videoStandard"][name="/source/sdi/videoStandard"]'
    input_sdi_1080p_30mode = 'select[id="/source/sdi/sdi1080p30Mode"][name="/source/sdi/sdi1080p30Mode"]'
    input_sdi_1080p_60mode = 'select[id="/source/sdi/sdi1080p60Mode"][name="/source/sdi/sdi1080p60Mode"]'
    input_sdi_2160p_30mode = 'select[id="/source/sdi/sdi2160p30Mode"][name="/source/sdi/sdi2160p30Mode"]'
    input_sdi_2160p_60mode = 'select[id="/source/sdi/sdi2160p60Mode"][name="/source/sdi/sdi2160p60Mode"]'
    input_sdi_enable_ha_mode = (
        'select[id="/source/sdi/enableHighAvailabilityMode"][name="/source/sdi/enableHighAvailabilityMode"]'
    )
    input_sdi_time_code_type = 'select[id="/source/sdi/timeCodeType"][name="/source/sdi/timeCodeType"]'
    input_sdi_aspect_ratio = 'select[id="/source/sdi/aspectRatio"][name="/source/sdi/aspectRatio"]'
    input_sdi_timed_text_source = 'select[id="/source/sdi/timedTextSource"][name="/source/sdi/timedTextSource"]'
    input_sdi_teletext_page = 'input[type="text"][id="/source/sdi/wstPage"][name="/source/sdi/wstPage"]'
    input_sdi_teletext_character_set = (
        'select[id="/source/sdi/wstDefaultCharSet"][name="/source/sdi/wstDefaultCharSet"]'
    )
    input_sdi_vbi_lines = 'input[type="text"][id="/source/sdi/timedTextVbiLines"][name="/source/sdi/timedTextVbiLines"]'
    input_sdi_teletext_language_tag = (
        'select[id="/source/sdi/timedTextLanguageTag"][name="/source/sdi/timedTextLanguageTag"]'
    )


class ConfigureBackupSourceElements:
    ### CSS Selector ###
    # Backup
    backup_source_type = 'slect[id="/source/secondSource/sourceType"][name="/source/secondSource/sourceType"]'
    backup_source_common_modulate_audio_track = (
        'select[id="/source/secondSource/modulatedAudioTrack"][name="/source/secondSource/modulatedAudioTrack"]'
    )

    # Backup Soruce UDP options CSS Selector
    backup_source_udp_network_url = 'input[type="text"][id="/source/secondSource/mpeg2/netConfig/networkUrl"][name="/source/secondSource/mpeg2/netConfig/networkUrl"]'
    backup_source_udp_interface = 'select[id="/source/secondSource/mpeg2/netConfig/interfaceId"][name="/source/secondSource/mpeg2/netConfig/interfaceId"]'
    backup_source_udp_enable_ts_over_rtp = 'input[type="checkbox"][id="/source/secondSource/mpeg2/enableTsOverRtp"][name="/source/secondSource/mpeg2/enableTsOverRtp"]'
    backup_soruce_udp_enable_srt = (
        'input[type="checkbox"][id="/source/secondSource/mpeg2/enableSrt"][name="/source/secondSource/mpeg2/enableSrt"]'
    )
    backup_source_udp_latency = (
        'input[type="text"][id="/source/secondSource/mpeg2/srtLatency"][name="/source/secondSource/mpeg2/srtLatency"]'
    )
    backup_source_udp_password = 'input[type="text"][id="/source/secondSource/mpeg2/srtPassphrase"][name="/source/secondSource/mpeg2/srtPassphrase"]'
    backup_source_udp_crypto_key_length = (
        'select[id="/source/secondSource/mpeg2/srtPbkeylen"][name="/source/secondSource/mpeg2/srtPbkeylen"]'
    )
    backup_source_udp_advanced_parmaneters = 'input[type="text"][id="/source/secondSource/mpeg2/srtAdvancedParameters"][name="/source/secondSource/mpeg2/srtAdvancedParameters"]'
    backup_source_udp_max_input_mbps = 'input[type="text"][id="/source/secondSource/mpeg2/netConfig/maxInputBitrateMbps"][name="/source/secondSource/mpeg2/netConfig/maxInputBitrateMbps"]'
    backup_source_udp_enable_ha_mode = 'select[id="/source/secondSource/mpeg2/enableHighAvailabilityMode"][name="/source/secondSource/mpeg2/enableHighAvailabilityMode"]'
    backup_source_udp_program_selection_mode = 'select[id="/source/secondSource/mpeg2/programSelectionMode"][name="/source/secondSource/mpeg2/programSelectionMode"]'
    backup_source_udp_video_id = (
        'input[type="text"][id="/source/secondSource/videoId"][name="/source/secondSource/videoId"]'
    )
    backup_source_udp_audio_id = (
        'input[type="text"][id="/source/secondSource/audioId"][name="/source/secondSource/audioId"]'
    )
    backup_source_udp_program_number = 'input[type="text"][id="/source/secondSource/mpeg2/programNumber"][name="/source/secondSource/mpeg2/programNumber"]'
    backup_source_udp_service_name = (
        'input[type="text"][id="/source/secondSource/mpeg2/serviceName"][name="/source/secondSource/mpeg2/serviceName"]'
    )

    # Backup Source RTP/RTSP options CSS Selector
    backup_source_rtp_sdp_file = (
        'input[type="text"][id="/source/secondSource/rtp/sdpFile"][name="/source/secondSource/rtp/sdpFile"]'
    )

    # Backup Source RTMP options CSS Selector
    backup_source_rtmp_url = (
        'input[type="text"][id="/source/secondSource/rtmp/url"][name="/source/secondSource/rtmp/url"]'
    )

    # Backup Source HLS options CSS Selector
    backup_source_hls_url = 'input[type="text"][id="/source/secondSource/hls/url"][name="/source/secondSource/hls/url"]'

    # Backup Source SDI options CSS Selector
    backup_source_sdi_input_port = (
        'select[id="/source/secondSource/sdi/channelId"][name="/source/secondSource/sdi/channelId"]'
    )
    backup_source_sdi_signal_type = (
        'select[id="/source/secondSource/sdi/signalType"][name="/source/secondSource/sdi/signalType"]'
    )
    backup_source_sdi_video_format = (
        'select[id="/source/secondSource/sdi/videoStandard"][name="/source/secondSource/sdi/videoStandard"]'
    )
    backup_source_sdi_1080p_30mode = (
        'select[id="/source/secondSource/sdi/sdi1080p30Mode"][name="/source/secondSource/sdi/sdi1080p30Mode"]'
    )
    backup_source_sdi_1080p_60mode = (
        'select[id="/source/secondSource/sdi/sdi1080p60Mode"][name="/source/secondSource/sdi/sdi1080p60Mode"]'
    )
    backup_source_sdi_enable_ha_mode = 'select[id="/source/secondSource/sdi/enableHighAvailabilityMode"][name="/source/secondSource/sdi/enableHighAvailabilityMode"]'
    backup_source_sdi_time_code_type = (
        'select[id="/source/secondSource/sdi/timeCodeType"][name="/source/secondSource/sdi/timeCodeType"]'
    )
    backup_source_sdi_aspect_ratio = (
        'select[id="/source/secondSource/sdi/aspectRatio"][name="/source/secondSource/sdi/aspectRatio"]'
    )
    backup_source_sdi_timed_text_source = (
        'select[id="/source/secondSource/sdi/timedTextSource"][name="/source/secondSource/sdi/timedTextSource"]'
    )
    backup_source_sdi_teletext_page = (
        'input[type="text"][id="/source/secondSource/sdi/wstPage"][name="/source/secondSource/sdi/wstPage"]'
    )
    backup_source_sdi_teletext_character_set = (
        'select[id="/source/secondSource/sdi/wstDefaultCharSet"][name="/source/secondSource/sdi/wstDefaultCharSet"]'
    )
    backup_source_sdi_vbi_lines = 'input[type="text"][id="/source/secondSource/sdi/timedTextVbiLines"][name="/source/secondSource/sdi/timedTextVbiLines"]'
    backup_source_sdi_teletext_language_tag = 'select[id="/source/secondSource/sdi/timedTextLanguageTag"][name="/source/secondSource/sdi/timedTextLanguageTag"]'

    # Backup Source Playlist options CSS Selector
    backup_source_playlist_type = (
        'select[id="/source/secondSource/fileList/type"][name="/source/secondSource/fileList/type"]'
    )
    backup_source_playlist_playlists_name = (
        'select[id="/source/secondSource/fileList/fileName"][name="/source/secondSource/fileList/fileName"]'
    )
    backup_source_playlist_clipcasting_uri = (
        'input[type="text"][id="/source/secondSource/fileList/url"][name="/source/secondSource/fileList/url"]'
    )
    backup_source_playlist_remote_media_asset_uri = (
        'input[type="text"][id="/source/secondSource/fileList/url"][name="/source/secondSource/fileList/url"]'
    )
    backup_source_playlist_recurring_the_last_n_files = 'input[type="text"][id="/source/secondSource/fileList/recurring"][name="/source/secondSource/fileList/recurring"]'
    backup_soruce_playlist_sort_by = (
        'select[id="/source/secondSource/fileList/sortMode"][name="/source/secondSource/fileList/sortMode"]'
    )

    # Backup Source SMPTE ST 2110 options CSS Selector
    backup_soruce_smpte_st_2110_video_sdp_url = 'input[type="text"][id="/source/secondSource/st2110/video/sdpUrl"][name="/source/secondSource/st2110/video/sdpUrl"]'
    backup_soruce_smpte_st_2110_video_first_nic = 'select[id="/source/secondSource/st2110/video/interfaceId"][name="/source/secondSource/st2110/video/interfaceId"]'
    backup_soruce_smpte_st_2110_video_second_nic = 'select[id="/source/secondSource/st2110/video/secondInterfaceId"][name="/source/secondSource/st2110/video/secondInterfaceId"]'
    backup_soruce_smpte_st_2110_audio_sdp_url = 'input[type="text"][id="/source/secondSource/st2110/audio/sdpUrl"][name="/source/secondSource/st2110/audio/sdpUrl"]'
    backup_soruce_smpte_st_2110_audio_first_nic = 'select[id="/source/secondSource/st2110/audio/interfaceId"][name="/source/secondSource/st2110/audio/interfaceId"]'
    backup_soruce_smpte_st_2110_audio_second_nic = 'select[id="/source/secondSource/st2110/audio/secondInterfaceId"][name="/source/secondSource/st2110/audio/secondInterfaceId"]'
    backup_soruce_smpte_st_2110_ancillary_sdp_url = (
        'input[type="text"][id="/source/secondSource/st2110/anc/sdpUrl"][name="/source/secondSource/st2110/anc/sdpUrl"]'
    )
    backup_soruce_smpte_st_2110_ancillary_first_nic = (
        'select[id="/source/secondSource/st2110/anc/interfaceId"][name="/source/secondSource/st2110/anc/interfaceId"]'
    )
    backup_soruce_smpte_st_2110_ancillary_second_nic = 'select[id="/source/secondSource/st2110/anc/secondInterfaceId"][name="/source/secondSource/st2110/anc/secondInterfaceId"]'

    # Backup Source NDI options CSS Selector
    backup_source_ndi_name = 'input[type="text"][id="/source/secondSource/ndi/sourceNameToConnect"][name="/source/secondSource/ndi/sourceNameToConnect"]'
    backup_source_ndi_group = (
        'input[type="text"][id="/source/secondSource/ndi/groupName"][name="/source/secondSource/ndi/groupName"]'
    )
    backup_source_ndi_url = 'input[type="text"][id="/source/secondSource/ndi/url"][name="/source/secondSource/ndi/url"]'


class ConfigureOutputElements:
    ### XPATH ###
    output_table = '//*[@id="output_list_table"]'
    ### CCS Selector ###
    # Output Common options
    output_add_output_button = 'span.orange-button-nopad[onclick="redirectToCreateURL()"]'
    output_create_button = "button#save-btn.orange-button-nopad"
    output_type = 'select[id="output-type-select"]'

    output_save_button = "button#save-btn.black-button"
    output_delete_button = "button#delete-btn.black-button"

    output_edit_stream = "span.edit-icon"
    output_add_stream_button = 'button[id="add-stream-btn"]'
    output_video_profile = 'select[name="video-profile"]'
    output_audio_profile = 'select[name="audioProfiles"]'
    output_edit_stream_save_button = "button#save-btn.black-button"
    output_edit_stream_delete_button = "button#delete-btn.black-button"

    ### XPATH ###
    # UDP/IP output options
    # Both ID and Name are the same, so it is used as full XPATH.
    output_udp_primary_output_address = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[5]/span/input"
    output_udp_primary_output_port = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[6]/span/input"
    output_udp_primary_network_interface = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[8]/span/select"
    output_udp_secondary_output_address = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[9]/span/input"
    output_udp_secondary_output_port = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[10]/span/input"
    output_udp_secondary_network_interface = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[12]/span/select"
    output_udp_multicast_ttl = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[13]/span/input"
    output_udp_tos = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[14]/span/input"
    output_udp_ts_id = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[16]/span/input"
    output_udp_program_number = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[17]/span/input"
    output_udp_service_name = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[18]/span/input"
    output_udp_service_provider = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[19]/span/input"
    output_udp_pmt_pid = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[20]/span/input"
    output_udp_pcr_pid = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[21]/span/input"
    output_udp_psi_interval = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[22]/span/input"
    output_udp_mux_rate = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[23]/span/input"
    output_udp_null_packet_padding = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[25]/span/select"
    output_udp_on_input_loss = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[26]/span/select"
    output_udp_dvb_subtitle_track_checkbox = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[28]/span/input"
    output_udp_dvb_subtitle_track = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[29]/span/input"
    output_udp_dvb_teletext_track_checkbox = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[31]/span/input"
    output_udp_dvb_teletext_track = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[32]/span/input"
    output_udp_enable_scte_35_passthru = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[35]/span/input"
    output_udp_enable_id3_tden_tag = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[37]/span/input"
    output_udp_enable_ts_over_rtp = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[38]/span/input"
    output_udp_srt = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[42]/span/input"
    output_udp_ats_ebp_checkbox = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[49]/span/input"
    output_udp_ats_ebp_fragment_duration = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[50]/span/input"
    output_udp_ats_ebp_segment_duration = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[51]/span/input"
    output_udp_vct_checkbox = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[52]/span/input"
    output_udp_vct_table_id = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[53]/span[2]/span/select"
    output_udp_vct_short_name = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[53]/span[3]/span/input"
    output_udp_vct_major_channel_number = (
        "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[53]/span[4]/span/input"
    )
    output_udp_vct_minor_channel_number = (
        "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[53]/span[5]/span/input"
    )
    output_udp_vct_modulation_mode = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[53]/span[6]/span/select"
    output_udp_vct_service_type = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[53]/span[7]/span/select"
    output_udp_vct_source_id = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[53]/span[8]/span/input"
    # CSS Selector : Radio button
    output_udp_broadcasting_standard_atsc = 'input[type="radio"][name="Broadcasting standard:"][value="0"]'
    output_udp_broadcasting_standard_dvb = 'input[type="radio"][name="Broadcasting standard:"][value="1"]'

    # HLS output options
    # Both ID and Name are the same, so it is used as full XPATH.
    output_hls_segment_naming = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[3]/span/select"
    output_hls_duration = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[6]/span/input"
    output_hls_segments_ring_size = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[7]/span/input"
    output_hls_keep_remote_segments = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[8]/span/input"
    output_hls_primary_master_playlist_path = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[9]/span/input"
    output_hls_backup_master_playlist_path = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[10]/span/input"
    output_hls_primary_playback_url = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[11]/span/input"
    output_hls_backup_playback_url = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[12]/span/input"
    output_hls_master_playlist_name = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[13]/span/input"
    output_hls_subtitle_playlist_name = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[14]/span/input"
    output_hls_subtitle_type = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[15]/span/select"
    output_hls_dvb_subtitle = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[16]/span/input"
    output_hls_dvb_teletext = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[19]/span/input"
    output_hls_create_subfolder = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[22]/span/input"
    output_hls_create_iframe_playlist = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[23]/span/input"
    output_hls_tagging_playlists_with_timestamp = (
        "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[24]/span/input"
    )
    output_hls_scte35_signaling = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[25]/span/select"
    output_hls_enable_id3_tden_tag = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[26]/span/input"
    output_hls_enable_encryption = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[27]/span/input"
    output_hls_append_endlist_at_stop = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[38]/span/input"

    # RTSP output option
    output_rtsp_publishing_point = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[2]/span/input"

    # RTMP output options
    output_rtmp_broadcast_address = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[2]/span/input"
    output_rtmp_secondary_address = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[3]/span/input"
    output_rtmp_broadcast_port = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[4]/span/input"
    output_rtmp_broadcast_path = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[5]/span/input"
    output_rtmp_secondary_path = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[6]/span/input"
    output_rtmp_stream_name = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[7]/span/input"
    output_rtmp_connection_timeout = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[8]/span/input"
    output_rtmp_send_timeout = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[9]/span/input"
    output_rtmp_subtitle_language = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[10]/span/select"
    output_rtmp_cdn_authentication = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[11]/span/select"
    output_rtmp_username = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[12]/span/input"
    output_rtmp_password = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[13]/span/input"

    # Live Smooth Streaming output options
    output_lss_fragment_duration = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[3]/span/input"
    otuput_lss_publishing_server_type = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[4]/span/select"
    output_lss_time_scale = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[5]/span/select"
    output_lss_hevc_codec_tag = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[6]/span/select"
    output_lss_publishing_point_url = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[7]/span/input"
    output_lss_secondary_point_url = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[8]/span/input"
    output_lss_ismt_properties = 'input[type="radio"][name="ISMT Properties"]'
    output_lss_dvb_subtitle = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[10]/span/input"
    output_lss_dvb_teletext = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[13]/span/input"
    output_lss_enable_secte35 = 'input[type="radio"][name="Enable SCTE35"]'
    output_lss_stream_naing = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[17]/span/select"
    output_lss_playready_drm = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[18]/span/select"
    output_lss_on_input_loss = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[30]/span/select"
    output_lss_send_mfra_at_stop = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[31]/span/input"

    # DASH output options
    output_dash_mpd_name = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[3]/span/input"
    output_dash_mpd_update_interval = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[4]/span/input"
    output_dash_primary_base_url = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[5]/span/input"
    output_dash_primary_path = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[6]/span/input"
    output_dash_secondary_base_url = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[7]/span/input"
    output_dash_secondary_path = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[8]/span/input"
    output_dash_segment_naming = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[9]/span/select"
    output_dash_segments_ring_size = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[10]/span/input"
    output_dash_segment_duration = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[11]/span/input"
    output_dash_min_buffer_time = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[13]/span/input"
    output_dash_mode = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[14]/span/select"
    output_dash_segment_template_mode = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[15]/span/select"
    output_dash_hevc_codec_tag = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[16]/span/select"
    output_dash_subtitle_type = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[17]/span/select"
    output_dash_scte35_signalling = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[18]/span/input"
    output_dash_drm_type = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[20]/span/select"

    # CMAF output options
    output_cmaf_ingest_protocol = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[4]/span/select"
    output_cmaf_base_publishing_point = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[5]/span/input"
    output_cmaf_enable_low_latency_transfer = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[6]/span/input"
    output_cmaf_http_method = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[7]/span/select"
    output_cmaf_create_subfolder = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[8]/span/input"
    output_cmaf_segment_naming = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[9]/span/select"
    output_cmaf_dvr_window_length = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[10]/span/input"
    output_cmaf_min_buffer_time = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[11]/span/input"
    output_cmaf_segment_duration = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[12]/span/input"
    output_cmaf_chunk_duration = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[13]/span/input"
    output_cmaf_hevc_codec_tag = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[14]/span/select"
    output_cmaf_dvb_sutitle_track = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[17]/span/input"
    output_cmaf_dvb_teletext_track = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[20]/span/input"
    output_cmaf_scte35_signalling = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[23]/span/input"
    output_cmaf_enable_id3 = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[26]/span/input"
    output_cmaf_use_utc_in_tfdt = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[27]/span/input"
    output_cmaf_use_negative_time_offset_in_trun = (
        "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[28]/span/input"
    )
    output_cmaf_drm_type = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[29]/span/select"
    output_cmaf_dash_segment_template_mode = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[53]/span/select"
    output_cmaf_dash_mpd_name = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[54]/span/input"
    output_cmaf_hls_master_playlist_name = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[55]/span/input"
    otuput_cmaf_append_endlist_at_stop = "/html/body/div/div[4]/div/div[1]/div/div[2]/div[3]/span[57]/span/input"


class ConfigureVideopresetElements:
    ### XPATH ###
    videopreset_table = '//*[@id="page-body-inner"]/div[2]/div[1]/table'

    ### CSS Selector###
    videopreset_name = 'input[type="text"][name="Name"]'
    videopreset_codec = 'select[id="/video/codecType"][name="/video/codecType"]'
    videopreset_encoding_engine = 'select[id="/video/subType"][name="/video/subType"]'
    videopreset_resolution = 'select[id="videoResizeSetting"][name="videoResizeSetting"]'
    videopreset_frame_rate = 'input[type="text"][id="/video/frameRate"][name="/video/frameRate"]'
    videopreset_bframe = 'input[type="text"][id="/video/bframes"][name="/video/bframes"]'
    videopreset_bitrate = 'input[type="text"][id="/video/bitrate"][name="/video/bitrate"]'
    videopreset_h264_profile = 'select[id="/video/h264Profile"][name="/video/h264Profile"]'
    videopreset_iframe_interval = 'input[type="text"][id="/video/gopSize"][name="/video/gopSize"]'
    videopreset_buffering_time = 'input.inputbox[type="text"][id="/video/lookaheaddepth"][name="/video/lookaheaddepth"]'
    videopreset_add_button = 'input.black-button[type="button"][value="Add"]'
    videopreset_save_button = 'input.black-button[type="submit"][name="action"][value="Save"]'


class ConfigureAudiopresetElements:
    ### XPATH ###
    audiopreset_table = '//*[@id="page-body-inner"]/div[2]/div[1]/table'

    ### CSS Selector ###
    audiopreset_name = 'input[type="text"][name="Name"]'
    audiopreset_codec = 'select[id="/audio/audioEncoder"][name="/audio/audioEncoder"]'
    audiopreset_mpeg_version = 'select[id="/audio/mpegVersion"][name="/audio/mpegVersion"]'
    audiopreset_profile = 'select[id="/audio/aacProfile"][name="/audio/aacProfile"]'
    audiopreset_version = 'select[id="/audio/version"][name="/audio/version"]'
    audiopreset_layer = 'select[id="/audio/mpegLayer"][name="/audio/mpegLayer"]'
    audiopreset_channels = 'select[id="/audio/channels"][name="/audio/channels"]'
    audiopreset_sampling_rate = 'select[id="/audio/samplingRate"][name="/audio/samplingRate"]'
    audiopreset_bitrate = 'select[id="/audio/bitrate"][name="/audio/bitrate"]'
    audiopreset_add_button = 'input.black-button[type="button"][value="Add"]'
    audiopreset_save_button = 'input.black-button[type="submit"][name="action"][value="Save"]'


class ConfigureTaskElements:
    ### XPATH ###
    task_table = '//*[@id="page-body-inner"]/div[2]/div[1]/table'

    ### CSS Selector ###
    task_add_button = 'input.black-button[type="button"][value="Add"]'
    task_save_button = 'input.black-button[type="submit"][name="action"][value="Save"]'
    task_name = 'input[type="text"][name="Name"]'
    task_group = 'select.inputbox[name="groupId"]'
    task_channel = 'select.inputbox[name="channelId"]'
    task_task = 'select[id="taskType"][name="taskType"][onchange="DoTaskChange()"]'
    task_replacement_image = 'select.inputbox[id="/task/replacementImage"][name="/task/replacementImage"]'
    task_replacement_playlist = 'select.inputbox[id="/task/replacementPlaylist"][name="/task/replacementPlaylist"]'
    task_date = 'input[type="text"]["id="taskDate"][name="taskDate"]'
    task_time = 'input[type="text"][id="taskTime"][name="taskTime"]'
    task_recurring_daily = 'select.inputbox[id="recurringDaily"][name="recurringDaily"]'
    task_recurring_weekly_mo = 'input[type="checkbox"][id="recurringWeeklyMo"][name="Mo"]'
    task_recurring_weekly_tu = 'input[type="checkbox"][id="recurringWeeklyTu"][name="Tu"]'
    task_recurring_weekly_we = 'input[type="checkbox"][id="recurringWeeklyWe"][name="We"]'
    task_recurring_weekly_th = 'input[type="checkbox"][id="recurringWeeklyTh"][name="Th"]'
    task_recurring_weekly_fr = 'input[type="checkbox"][id="recurringWeeklyFr"][name="Fr"]'
    task_recurring_weekly_sa = 'input[type="checkbox"][id="recurringWeeklySa"][name="Sa"]'
    task_recurring_weekly_su = 'input[type="checkbox"][id="recurringWeeklySu"][name="Su"]'
    task_state = 'select.inputbox[name="taskState"]'


class MonitorDeviceElements:
    chindex = int()
    ### XPATH ###
    monitor_table = '//*[@id="dev_info0"]/div[2]/table/tbody/tr/td[1]/div[2]/table'
    monitor_device_edit_device = '//*[@id="configform"]/div[1]/span[2]/a'
    monitor_device_edit_group = '//*[@id="configform"]/div[1]/span[4]/a'
    monitor_device_edit_role = '//*[@id="configform"]/div[1]/span[6]/a'

    ### CSS Selector ###
    monitor_device_admin = 'a[class="no-decoration black"][title="Edit privileged device configuration"]'
    monitor_device_event_log = 'a[class="no-decoration black"][title="Event Log for this device"]'
    monitor_device_output = 'a[class="no-decoration black"][title="Click to access output file(s)"]'
    monitor_device_sacn_asi_sdi = 'a[id="scanAsiSdi"][name="scanAsiSdi"][title="Click to view ASI/SDI stats"]'
    monitor_device_multicast_traffic = 'a[id="checkInput"][name="checkInput"][title="Click to view multicast traffic"]'
    monitor_device_start_all = 'button[type="submit"][id="btnstart"][name="startall"][value="Start All"]'
    monitor_device_stop_all = 'button[type="submit"][id="btnstop"][name="stopall"][value="Stop All"]'
    monitor_device_preview_all = 'input[type="button"][id="previewAll"][name="previewAll"][value=" Preview All"]'

    ### In Channel Box ###
    channel_start = "div#ChannelBoxStopped{} > input.start"
    channel_stop = "div#ChannelBoxStopped{} > input.stop"
    monitor_device_channel_start = (
        'input[type="button"][id="StartChannel{}"][title="Click to start this channel"][value="Start"]'
    )
    monitor_device_channel_stop = (
        'input[type="button"][id="StopChannel{}"][title="Click to stop this channel"][value="Stop"]'
    )
    monitor_device_switch_source = 'input[type="button"][id="SwitchSourceBtn{}"][title="Click to toggle switch between primary and backup source"][value="Switch"]'
    moniotr_device_replace_source = 'a[id="open-source-replacement-menu"][title="Show replace input source menu"]'
    monitor_device_page = (
        # "#dev_info0 > div.devline-1-body > table > tbody > tr > td:nth-child(1) > div.devline-1-channel"
        'document.querySelector("#dev_info0 > div.devline-1-body")'
    )
