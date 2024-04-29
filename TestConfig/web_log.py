from Config.common_convert_date import ConvertDate


class WebLog:

    def exec_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: {log}", flush=True)

    def step_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [STEP] {log}", flush=True)

    def sub_step_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [SUB STEP] {log}", flush=True)

    def info_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:   [INFO] {log}", flush=True)

    def option_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}:     [OPTION] {log}", flush=True)

    def warning_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [WARNING] {log}", flush=True)

    def error_log(log):
        date = ConvertDate.convert_date()[1]
        return print(f"{date}: [ERROR] {log}", flush=True)
