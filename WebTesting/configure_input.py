# configure_channels.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException, ElementNotVisibleException
from webdriver_method import WebDriverMethod
from web_elements import ConfigureInputElements
import time


class ConfigureInput(WebDriverMethod):
    def __init__(self, input_type):
        self.input_elements = ConfigureInputElements()
        try:
            self.select_element(
                By.CSS_SELECTOR, self.input_elements.input_type, 'text', input_type)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def input_udp(self, input_options):
        input_relevant_keys = ['Network URL', 'SSM host',
                               'Max input Mbps', 'Video ID', 'Audio ID']
        select_relevant_keys = ['Interface',
                                'Enable HA Mode', 'Program Selection Mode']
        try:
            print('UDP/IP Input settings')
            for key, value in input_options.items():
                print(f"  ㆍ{key} : {value}")
                element_selector = getattr(
                    self.input_elements, f"input_udp_{''.join(key.replace(' ', '_').lower().split('-'))}" if '-' in key else f"input_udp_{key.lower().replace(' ', '_')}", None)
                if any(keyword in key for keyword in select_relevant_keys):
                    if 'Program Selection Mode' in key:
                        mode = self.select_element(
                            By.CSS_SELECTOR, element_selector, 'text', value)
                        try:
                            self.accept_alert()
                            self.input_text(
                                By.CSS_SELECTOR, self.input_elements.input_common_analysis_window, '6000')
                            time.sleep(1)
                        except:
                            pass
                        if mode in ['Program number', 'Service name']:
                            mapping = {
                                'Program number': (self.input_elements.input_udp_program_number, '1010'),
                                'Service name': (self.input_elements.input_udp_service_name, 'E2 Channel')
                            }
                            self.input_text(By.CSS_SELECTOR,
                                            *mapping.get(mode))
                    else:
                        self.select_element(
                            By.CSS_SELECTOR, element_selector, 'text', value)
                elif any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    if isinstance(value, bool) and value:
                        self.click_element(By.CSS_SELECTOR, element_selector)
                    else:
                        self.click_element(By.CSS_SELECTOR, element_selector)

            print('UDP/IP Input setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def input_rtsp(self, input_options):
        try:
            print('RTSP Input settings')
            self.input_text(By.CSS_SELECTOR,
                            self.input_elements.input_udp_network_url, input_options.get('SDP File'))
            print('RTSP Input setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def input_rtmp(self, input_options):
        try:
            print('RTMP Input settings')
            self.input_text(By.CSS_SELECTOR,
                            self.input_elements.input_udp_network_url, input_options.get('URL'))
            print('RTMP Input setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def input_hls(self, input_options):
        try:
            print('HLS Input settings')
            self.input_text(By.CSS_SELECTOR,
                            self.input_elements.input_udp_network_url, input_options.get('URL'))
            print('HLS Input setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def input_sdi(self, input_options):
        input_relevant_keys = ['Teletext page', 'VBI lines']
        try:
            print('SDI Input settings')
            for key, value in input_options.items():
                print(f"  ㆍ{key} : {value}")
                element_selector = getattr(
                    self.input_elements, f"input_sdi_{''.join(key.replace(' ', '_').lower().split('-'))}" if '-' in key else f"input_sdi_{key.replace(' ', '_').lower()}", None)
                if any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR,
                                    element_selector, value)
                else:
                    self.select_element(
                        By.CSS_SELECTOR, element_selector, 'text', value)

            print('SDI Input setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def input_playlist(self, input_options):
        input_relevant_keys = ['URI', 'Recurring the last N files']
        try:
            print('Playlist Input settings')
            # playlist_type = input_options.get('Type')
            # self.select_element(
            #     By.CSS_SELECTOR, self.input_elements.input_playlist_type, 'text', playlist_type)

            for key, value in input_options.items():
                print(f"  ㆍ{key} : {value}")
                element_selector = getattr(
                    self.input_elements, f"input_playlist_{''.join(key.replace(' ', '_').lower().split('-'))}" if '-' in key else f"input_playlist_{key.replace(' ', '_').lower()}", None)
                if any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR, element_selector, value)
                else:
                    self.select_element(
                        By.CSS_SELECTOR, element_selector, 'text', value)
                    if 'Type' == key:
                        time.sleep(1)

            print('Playlist Input setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def input_smpte_st_2110(self, input_options):
        input_relevant_keys = [
            'Video SDP URL', 'Audio SDP URL', 'Ancillary SDP URL', 'Teletext page']
        try:
            print('SMPTE ST 2110 Input settings')
            for key, value in input_options.items():
                print(f"  ㆍ{key} : {value}")
                element_selector = getattr(
                    self.input_elements, f"input_smpte_st_2110_{''.join(key.replace(' ', '_').lower().split('-'))}" if '-' in key else f"input_smpte_st_2110_{key.replace(' ', '_').lower()}", None)
                if any(keyword in key for keyword in input_relevant_keys):
                    self.input_text(By.CSS_SELECTOR,
                                    element_selector, value)
                else:
                    self.select_element(
                        By.CSS_SELECTOR, element_selector, 'text', value)

            print('SMTPE ST 2110 Input setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")

    def input_ndi(self, input_options):
        try:
            print('NDI Input settings')
            for key, value in input_options.items():
                print(f"{key} : {value}")
                element_selector = getattr(
                    self.input_elements, f"input_ndi_{''.join(key.replace(' ', '_').lower().split('-'))}" if '-' in key else f"input_ndi_{key.replace(' ', '_').lower()}", None)
                self.input_text(By.CSS_SELECTOR,
                                element_selector, value)

            print('NDI Input setting complete')
            time.sleep(1)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException) as e:
            print(f"Error: {e}")
