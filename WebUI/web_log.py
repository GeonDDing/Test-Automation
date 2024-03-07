import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.convert_date import ConvertDate


class WebLog:
    @classmethod
    def web_log(self, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: {log}")
