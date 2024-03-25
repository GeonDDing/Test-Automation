from api_operation import ApiOperation
import requests


class DeleteNewChannels(ApiOperation):
    def delelte_new_channels(self):
        channel_dict = dict()
        new_channel_flag = bool()
        get_response = requests.get(f"{self.api_url}?id=-1", headers=self.headers)

        if get_response.status_code == 200:
            channel_dict = get_response.json()

            for i in range(0, len(channel_dict)):
                if "Testing" in channel_dict[i]["name"]:
                    new_channel_flag = True
                    print(channel_dict[i]["name"], channel_dict[i]["id"])
                    delete_reponse = requests.delete(
                        f"{self.api_url}?id={channel_dict[i]['id']}",
                        headers=self.headers,
                    )
                    if delete_reponse.status_code == 200:
                        print(f"Delete Channel : {channel_dict[i]['name']}")
                else:
                    new_channel_flag = False

        if not new_channel_flag:
            print("There are no more new channels left.")


if __name__ == "__main__":
    test = DeleteNewChannels("channels")
    test.delelte_new_channels()
