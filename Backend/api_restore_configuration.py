import requests
import json


class ResotreConfiguration:
    base_url = "http://10.1.0.145/hms/rest/"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    device_data = {"ip": "127.0.0.1", "groupid": 24, "roleid": 1, "name": "10.1.0.145"}

    def restore_device(self):
        put_reponse = requests.put(
            f"{self.base_url}devices.php?id=6", headers=self.headers, data=json.dumps(self.device_data)
        )

        if put_reponse.status_code == 200:
            print(f"Restore Device : {put_reponse.json()}", flush=True)
        else:
            print(f"{put_reponse.status_code}, {put_reponse.text}", flush=True)

    def delete_groups(self):
        group_dict = dict()
        exist_group_flag = bool()
        get_reponse = requests.get(f"{self.base_url}groups.php?id=-1", headers=self.headers)

        if get_reponse.status_code == 200:
            group_dict = get_reponse.json()
            for i in range(0, len(group_dict)):
                if "Live Group" in group_dict[i]["name"]:
                    exist_group_flag = True
                    delete_reponse = requests.delete(
                        f"{self.base_url}groups.php?id={group_dict[i]['id']}",
                        headers=self.headers,
                    )
                    if delete_reponse.status_code == 200:
                        print(f"Delete Groups : {group_dict[i]['name']}", flush=True)
                else:
                    exist_group_flag = False

        if not exist_group_flag:
            print("There are no more testing group left.")

    def delete_roles(self):
        role_dict = dict()
        exist_role_flag = bool()
        get_reponse = requests.get(f"{self.base_url}roles.php?id=-1", headers=self.headers)
        if get_reponse.status_code == 200:
            role_dict = get_reponse.json()
            for i in range(0, len(role_dict)):
                if "API Test Role" in role_dict[i]["name"]:
                    exist_role_flag = True
                    delete_reponse = requests.delete(
                        f"{self.base_url}roles.php?id={role_dict[i]['id']}",
                        headers=self.headers,
                    )
                    if delete_reponse.status_code == 200:
                        print(f"Delete Roles : {role_dict[i]['name']}", flush=True)
                else:
                    exist_role_flag = False

        if not exist_role_flag:
            print("There are no more testing roles left.", flush=True)

    def delelte_channels(self):
        channel_dict = dict()
        exist_channel_flag = bool()
        get_response = requests.get(f"{self.base_url}channels.php?id=-1", headers=self.headers)

        if get_response.status_code == 200:
            channel_dict = get_response.json()

            for i in range(0, len(channel_dict)):
                if "Testing" in channel_dict[i]["name"] or "New" in channel_dict[i]["name"]:
                    exist_channel_flag = True
                    delete_reponse = requests.delete(
                        f"{self.base_url}channels.php?id={channel_dict[i]['id']}",
                        headers=self.headers,
                    )
                    if delete_reponse.status_code == 200:
                        print(f"Delete Channel : {channel_dict[i]['name']}", flush=True)
                else:
                    exist_channel_flag = False

        if not exist_channel_flag:
            print("There are no more test channels left.", flush=True)


if __name__ == "__main__":
    restore = ResotreConfiguration()
    # restore.delelte_channels()
    # restore.restore_device()
    restore.delete_groups()
    restore.delete_roles()
