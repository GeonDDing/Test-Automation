from multiprocessing import Process, Queue, Manager
from stats_sender import StatsSender
from web_log import WebLog
import time
import sys
import os

# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.convert_date import ConvertDate


class StatsReceiver:
    def stats_receiver(self, queue, formatted_messages):
        is_evergreen_flag = True
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
                            WebLog.info_log(
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
                            WebLog.info_log(
                                f"#{chidx} Restored to the {'Primary' if source_layer == '0' else 'Backup'} source"
                            )
                            formatted_messages.append(
                                f"#{chidx} Restored to the {'Primary' if source_layer == '0' else 'Backup'} source"
                            )
                        elif prev_source_layer == "2":
                            WebLog.info_log(
                                f"   #{chidx} User replaced source, Input Changed"
                                if source_layer == "1"
                                else f"   #{chidx} Source changed (source:#0)"
                            )
                            formatted_messages.append(
                                f"   #{chidx} User replaced source, Input Changed"
                                if source_layer == "1"
                                else f"   #{chidx} Source changed (source:#0)"
                            )

                    if source_stat == "-1" and is_evergreen_flag:
                        WebLog.info_log(f"   #{chidx} Evergreen occurred.")
                        formatted_messages.append(f"   #{chidx} Evergreen occurred.")
                        is_evergreen_flag = False
                    elif source_stat != "-1":
                        if not is_evergreen_flag and prev_source_stat != source_stat:
                            WebLog.info_log(f"   #{chidx} Evergreen recovered.")
                            formatted_messages.append(f"   #{chidx} Evergreen recovered.")
                            is_evergreen_flag = True
                        WebLog.exec_log(
                            f'   #{chidx} {"Primary" if source_layer == "0" else "Backup" if source_layer == "2" else "Replaced"} Source : {get_stats[4]}'
                        )
                        formatted_messages.append(
                            f'{ConvertDate.convert_date()[1]}:    #{chidx} {"Primary" if source_layer == "0" else "Backup" if source_layer == "2" else "Replaced"} Source : {get_stats[4]}'
                        )

                    prev_source_layer, prev_source_stat = source_layer, source_stat
                    time.sleep(2)

            except Exception as e:
                WebLog.error_log(f"An error occurred: {e}")
                formatted_messages.append(f"An error occurred: {e}")

    def exec_multiprocessing(self, chidx, channel_name):
        stats_queue = Queue()
        sender = StatsSender()
        manager = Manager()
        formatted_messages = manager.list()
        config_channel_name = manager.list()

        sender_process = Process(
            target=sender.stats_sender,
            args=(
                stats_queue,
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

        # for message in formatted_messages:
        #     parse_message.append(message + "\n")

        if formatted_messages:
            return True
        else:
            return str(config_channel_name)[2:-2]


if __name__ == "__main__":
    test = StatsReceiver()
    test.exec_multiprocessing(0)
