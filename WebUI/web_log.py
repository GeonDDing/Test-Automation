from Common.convert_date import ConvertDate


class WebLog:
    @classmethod
    def exec_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: {log}")

    @classmethod
    def step_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [STEP] {log}")

    @classmethod
    def sub_step_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [SUB STEP] {log}")

    @classmethod
    def info_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [INFO] {log}")

    @classmethod
    def option_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:     [OPTION] {log}")

    @classmethod
    def warning_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [WARNING] {log}")

    @classmethod
    def error_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [ERROR] {log}")
