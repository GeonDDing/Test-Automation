from multiprocessing import Process, Queue, Manager
import time
from stats_sender import StatsSender
from webdriver_method import WebDriverMethod
from web_log import WebLog


class StatsReceiver(WebDriverMethod):
    def stats_receiver(self, queue):
        self.close_driver()
        is_evergreen_flag = True
        prev_source_layer = prev_source_stat = None
        while True:
            try:
                get_stats = queue.get()
                if get_stats == "quit":
                    break
                chidx = f"0{get_stats[0]+1:02}"
                source_layer, source_stat = get_stats[1:3]

                if prev_source_layer is not None and source_layer != prev_source_layer:
                    if prev_source_layer == "0":
                        WebLog.exec_log(
                            f"   #{chidx} User replaced source, Input Changed"
                            if source_layer == "1"
                            else f"   #{chidx} Source changed (source:#1)"
                        )
                    elif prev_source_layer == "1":
                        WebLog.exec_log(
                            f"#{chidx} Restored to the {'Primary' if source_layer == '0' else 'Backup'} source"
                        )
                    elif prev_source_layer == "2":
                        WebLog.exec_log(
                            f"   #{chidx} User replaced source, Input Changed"
                            if source_layer == "1"
                            else f"   #{chidx} Source changed (source:#0)"
                        )

                if source_stat == "-1" and is_evergreen_flag:
                    WebLog.exec_log(f"   #{chidx} Evergreen occurred.")
                    is_evergreen_flag = False
                elif source_stat != "-1":
                    if not is_evergreen_flag and prev_source_stat != source_stat:
                        WebLog.exec_log(f"   #{chidx} Evergreen recovered.")
                        is_evergreen_flag = True
                    WebLog.exec_log(
                        f'   #{chidx} {"Primary" if source_layer == "0" else "Backup" if source_layer == "2" else "Replaced"} Source : {get_stats[3]}'
                    )

                prev_source_layer, prev_source_stat = source_layer, source_stat
                time.sleep(2)

            except Exception as e:
                WebLog.error_log(f"An error occurred: {e}")

    def exec_multiprocessing(self, chidx):
        stats_queue = Queue()
        sender = StatsSender()
        # shared_dict = Manager().dict()

        sender_process = Process(
            target=sender.stats_sender,
            args=(
                stats_queue,
                chidx,
            ),
        )
        receiver_process = Process(target=self.stats_receiver, args=(stats_queue,))

        sender_process.start()
        receiver_process.start()

        sender_process.join()
        receiver_process.join()
