from multiprocessing import Process, Queue, Manager
from TestConfig.web_stats_sender import StatsSender
from TestConfig.web_log import WebLog
from TestConfig.web_stream_capture import StreamCapture
import time


class StatsReceiver(WebLog):
    def stats_receiver(self, queue, formatted_messages):
        is_evergreen = True
        prev_source_layer = prev_source_stat = None
        while True:
            try:
                get_stats = queue.get()
                if get_stats == "Channel names do not match":
                    break
                elif get_stats == "quit":
                    break
                else:
                    chidx = f"0{get_stats[0]+1:02}"
                    source_layer, source_stat = get_stats[2:4]  # list[2], list[3]

                    if prev_source_layer is not None and source_layer != prev_source_layer:
                        if prev_source_layer == "0":
                            self.info_log(
                                f"   #{chidx} User replaced source, Input Changed"
                                if source_layer == "1"
                                else f"   #{chidx} Source changed (source:#1)"
                            )
                            formatted_messages.append(
                                f"   #{chidx} User replaced source, Input Changed"
                                if source_layer == "1"
                                else f"   #{chidx} Source changed (source:#1)"
                            )
                        elif prev_source_layer == "1":
                            self.info_log(
                                f"#{chidx} Restored to the {'Primary' if source_layer == '0' else 'Backup'} source"
                            )
                            formatted_messages.append(
                                f"#{chidx} Restored to the {'Primary' if source_layer == '0' else 'Backup'} source"
                            )
                        elif prev_source_layer == "2":
                            self.info_log(
                                f"   #{chidx} User replaced source, Input Changed"
                                if source_layer == "1"
                                else f"   #{chidx} Source changed (source:#0)"
                            )
                            formatted_messages.append(
                                f"   #{chidx} User replaced source, Input Changed"
                                if source_layer == "1"
                                else f"   #{chidx} Source changed (source:#0)"
                            )

                    if source_stat == "-1" and is_evergreen:
                        self.info_log(f"   #{chidx} Evergreen occurred.")
                        formatted_messages.append(f"   #{chidx} Evergreen occurred.")
                        is_evergreen = False
                    elif source_stat != "-1":
                        if not is_evergreen and prev_source_stat != source_stat:
                            self.info_log(f"   #{chidx} Evergreen recovered.")
                            formatted_messages.append(f"   #{chidx} Evergreen recovered.")
                            is_evergreen = True
                        self.exec_log(
                            f'#{chidx} {"Primary" if source_layer == "0" else "Backup" if source_layer == "2" else "Replaced"} Source : {get_stats[4]}'
                        )
                        formatted_messages.append(
                            f'{self.convert_date()[1]}: #{chidx} {"Primary" if source_layer == "0" else "Backup" if source_layer == "2" else "Replaced"} Source : {get_stats[4]}'
                        )

                    prev_source_layer, prev_source_stat = source_layer, source_stat
                    time.sleep(2)

            except Exception as e:
                self.error_log(f"stats receiver error | {repr(e)}")
                formatted_messages.append(f"stats receiver error | {repr(e)}")

    def exec_multiprocessing(self, chidx, channel_name, url, output_name):
        stats_queue = Queue()
        capture_queue = Queue()
        sender = StatsSender()
        stream_capture = StreamCapture()
        manager = Manager()
        formatted_messages = manager.list()
        config_channel_name = manager.list()
        capture_image = manager.list()
        time.sleep(10)

        if url != None and output_name != None:
            sender_process = Process(
                target=sender.stats_sender,
                args=(
                    stats_queue,
                    capture_queue,
                    chidx,
                    channel_name,
                    config_channel_name,
                ),
            )
            receiver_process = Process(
                target=self.stats_receiver,
                args=(
                    stats_queue,
                    formatted_messages,
                ),
            )
            stream_capture_process = Process(
                target=stream_capture.stream_capture,
                args=(
                    capture_queue,
                    url,
                    output_name,
                    capture_image,
                ),
            )

            sender_process.start()
            receiver_process.start()
            stream_capture_process.start()
            sender_process.join()
            receiver_process.join()
            stream_capture_process.join()

            if formatted_messages and capture_image:
                return True, formatted_messages, capture_image
            else:
                return str(config_channel_name)[2:-2]
        else:
            sender_process = Process(
                target=sender.stats_sender,
                args=(
                    stats_queue,
                    capture_queue,
                    chidx,
                    channel_name,
                    config_channel_name,
                ),
            )
            receiver_process = Process(
                target=self.stats_receiver,
                args=(
                    stats_queue,
                    formatted_messages,
                ),
            )
            sender_process.start()
            receiver_process.start()
            sender_process.join()
            receiver_process.join()

            if formatted_messages:
                return True, formatted_messages, None
            else:
                return str(config_channel_name)[2:-2]
