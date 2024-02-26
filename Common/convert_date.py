# convert_date.py
from datetime import datetime


class ConvertDate:
    def convert_date(self):
        time = datetime.now()

        hour_minute_second = time.strftime("%H%M%S")
        iso_format = time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        compact_format = time.strftime("%Y%m%d%H%M%S")
        compact2_format = time.strftime("%Y%m%d")

        return hour_minute_second, iso_format, compact_format, compact2_format
