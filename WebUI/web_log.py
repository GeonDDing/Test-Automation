import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.convert_date import ConvertDate


class WebLog:
    @classmethod
    def step_log(self, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [STEP] {log}")

    @classmethod
    def sub_step_log(self, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [SUB STEP] {log}")

    @classmethod
    def info_log(self, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [INFO] {log}")

    @classmethod
    def option_log(self, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [OPTION] {log}")

    @classmethod
    def error_log(self, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [ERROR] {log}")
