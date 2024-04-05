from Common.convert_date import ConvertDate


class WebLog:
    @staticmethod
    def exec_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: {log}")

    @staticmethod
    def step_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [STEP] {log}")

    @staticmethod
    def sub_step_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [SUB STEP] {log}")

    @staticmethod
    def info_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [INFO] {log}")

    @staticmethod
    def option_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:     [OPTION] {log}")

    @staticmethod
    def warning_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [WARNING] {log}")

    @staticmethod
    def error_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [ERROR] {log}")
