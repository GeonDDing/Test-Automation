from Common.convert_date import ConvertDate


class WebLog:
    @classmethod
    def exec_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: {log}")

    @classmethod
    def step_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:" + f"\033[35m [STEP] \033[0m{log}")

    @classmethod
    def sub_step_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:" + f"\033[35m   [SUB STEP] \033[0m{log}")

    @classmethod
    def info_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:" + f"\033[32m   [INFO] \033[0m{log}")

    @classmethod
    def option_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:" + f"\033[34m     [OPTION] \033[0m{log}")

    @classmethod
    def warning_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:" + f"\033[33m    [WARNING] \033[0m{log}")

    @classmethod
    def error_log(cls, log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:" + f"\033[91m [ERROR] \033[0m{log}")
