from Common.convert_date import ConvertDate


class WebLog:
    @staticmethod
    def exec_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: {log}", flush=True)

    @staticmethod
    def step_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [STEP] {log}", flush=True)

    @staticmethod
    def sub_step_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [SUB STEP] {log}", flush=True)

    @staticmethod
    def info_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [INFO] {log}", flush=True)

    @staticmethod
    def option_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:     [OPTION] {log}", flush=True)

    @staticmethod
    def warning_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [WARNING] {log}", flush=True)

    @staticmethod
    def error_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [ERROR] {log}", flush=True)
