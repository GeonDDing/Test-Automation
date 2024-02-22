import xml.etree.ElementTree as elementTree
import requests
import time
import multiprocessing
from stats_sender import StatsSender

class StatsReceiver():
    def stats_receiver(self, queue):
        is_backupsource_flag = False
        is_replacesource_flag = False
        is_evergreen_flag = True
        prev_source_layer = None
        prev_source_stat = None
        while not queue.get() == 'quit':
            try:
                get_stats = queue.get()
                chidx = get_stats[0]+1
                if int(chidx) > 10:
                    chidx = f"0{chidx}"
                else:
                    chidx = f"00{chidx}"
                source_layer = get_stats[1]
                source_stat = get_stats[2]
                
                if source_layer == '0':
                    if prev_source_layer == '1':
                        print(f"#{chidx} Restored to the Primary source")
                    elif prev_source_layer == '2':
                        print(f"#{chidx} Source changed (source:#0)")
                    if source_stat == '-1' and is_evergreen_flag:
                        print(f"#{chidx} Evergreen occurred.")
                        is_evergreen_flag = False
                    elif not source_stat == '-1':
                        if not prev_source_stat == source_stat:
                            if not is_evergreen_flag:
                                print(f"#{chidx} Evergreen recovered")
                                is_evergreen_flag = True
                        print(f'#{chidx} Primary Source : {get_stats[3]}')
                elif source_layer == '1':
                    if prev_source_layer == '0' or prev_source_layer == '2':
                        print(f"#{chidx} User replaced source, Input Changed")
                    if source_stat == '-1' and is_evergreen_flag:
                        print(f"#{chidx} Evergreen occurred")
                        is_evergreen_flag = False
                    elif not source_stat == '-1':
                        if not prev_source_stat == source_stat:
                            if not is_evergreen_flag:
                                print(f"#{chidx} Evergreen recovered")
                                is_evergreen_flag = True
                        print(f'#{chidx} Replaced Source : {get_stats[3]}')
                elif source_layer == '2':
                    if prev_source_layer == '0':
                        print(f"#{chidx} Source changed (source:#1)")
                    elif prev_source_layer == '1':
                        print(f"#{chidx} Restored to the Backup source")
                    if source_stat == '-1' and is_evergreen_flag:
                        print(f"#{chidx} Evergreen occurred.")
                        is_evergreen_flag = False
                    elif not source_stat == '-1':
                        if not prev_source_stat == source_stat:
                            if not is_evergreen_flag:
                                print(f"#{chidx} Evergreen recovered")
                                is_evergreen_flag = True
                        print(f'#{chidx} Backup Source : {get_stats[3]}')

                prev_source_layer = source_layer
                prev_source_stat = source_stat
                time.sleep(2)

            except Exception as e:
                print("An error occurred:", e)

if __name__ == '__main__':
    stats_queue = multiprocessing.Queue()
    test = StatsReceiver()
    test2 = StatsSender()

    sender_process = multiprocessing.Process(target=test2.stats_sender, args=(stats_queue,))
    receiver_process = multiprocessing.Process(target=test.stats_receiver, args=(stats_queue,))
    
    sender_process.start()
    receiver_process.start()
    
    sender_process.join() 
    receiver_process.join()