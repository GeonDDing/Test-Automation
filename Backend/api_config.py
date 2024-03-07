# api_config.py
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Common.convert_date import ConvertDate


class ApiConfig:
    def __init__(self, headers=None, base_url="http://10.1.0.145/hms/rest/"):
        if headers == None:
            headers = {"Content-type": "application/json", "Accept": "text/plain"}
        self.headers = headers
        self.base_url = base_url

    def convert_json(self, json_file, http_method):
        data_list = []
        try:
            file_path = os.path.join(os.getcwd(), "Backend", "json", f"{http_method}_{json_file}.json")
            with open(file_path, "r") as f:
                json_data = json.load(f)

                if isinstance(json_data, list):
                    data_list = [item["data"] for item in json_data if "data" in item]
                elif "data" in json_data:
                    data_list = [json_data["data"]]
                if json_file in ["videopresets", "audiopresets"]:
                    for data in data_list:
                        if "name" in data:
                            data["name"] = f"{data.get('name', '')}_{ConvertDate.convert_date()[0]}"

        except FileNotFoundError:
            print(f"Error: File '{json_file}' not found.")
        except json.JSONDecodeError as e:
            print(f"Error: decoding JSON in file '{json_file}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return data_list
