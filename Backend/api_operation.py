import requests
import json
from time import sleep
from api_config import ApiConfig


class ApiOperation(ApiConfig):
    def __init__(self, api_resource):
        super().__init__()
        self.api_resource = api_resource
        self.api_url = f"{self.base_url}{self.api_resource}.php"
        # print(self.api_url)

    def send_request(self, method, id_value=None, *args, data=None):
        try:
            api_url = f"{self.api_url}?id={id_value}" if id_value else self.api_url
            if args:
                args_dict = dict(zip(args[::2], args[1::2]))
                if not id_value == None:
                    # ex) args = ("color", "blue", "size", "large")
                    #     my_dict = my_function(*args)
                    #     print(my_dict) → {'color': 'blue', 'size': 'large'}
                    api_url += "&" + "&".join([f"{key}={value}" for key, value in args_dict.items()])
                else:
                    api_url += f"?{args[0]}={args[1]}"
                    for key, value in args_dict.items():
                        if key == args[0]:
                            continue
                        api_url += f"&{key}={value}"
            print(f"API URL : {api_url}")
            if method == "get":
                response = requests.get(api_url, headers=self.headers)
            elif method == "post":
                response = requests.post(api_url, headers=self.headers, data=json.dumps(data))
            elif method == "put":
                response = requests.put(api_url, headers=self.headers, data=json.dumps(data))
            elif method == "delete":
                response = requests.delete(api_url, headers=self.headers)
            else:
                raise ValueError(f"Invalid HTTP method: {method}")

            response.raise_for_status()

            if response.status_code == 200:
                print(json.dumps(response.json(), indent=4))
            else:
                print(f"Unexpected status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")

        return response.status_code, response.json()

    def get_api_operation(self, id_value=None, *args):
        print("GET API Request")
        return self.send_request("get", id_value, *args)

    def post_api_operation(self, *args):
        print("POST API Request")
        request = list()
        post_data_list = self.convert_json(self.api_resource, "post")
        for i, post_data in enumerate(post_data_list):
            request.append(self.send_request("post", *args, data=post_data))
            if len(post_data_list) > 1:
                sleep(20)
        return request

    def put_api_operation(self, id_value=None, *args):
        print("PUT API Request")
        request = list()
        put_data_list = self.convert_json(self.api_resource, "put")
        for i, put_data in enumerate(put_data_list):
            request.append(self.send_request("put", id_value, *args, data=put_data))
            if len(put_data_list) > 1:
                sleep(20)
        return request

    def delete_api_operation(self, id_value=None, *args):
        print("DELETE API Request")
        return self.send_request("delete", id_value, *args)
