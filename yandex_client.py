import requests


class YandexApi:
    def __init__(self, token, api_url, api_version):
        self.token = token
        self.api_url = api_url + api_version
        self.api_version = api_version
        self.headers = {"Authorization": f"OAuth {self.token}"}

    def get_folders(self, path):
        response = requests.get(self.api_url + "/disk/resources",
                                params={"path": path}, headers=self.headers)
        return response

    def delete_folder(self, path):
        response = requests.delete(self.api_url + "/disk/resources",
                                   params={"path": path}, headers=self.headers)
        return response

    def create_folder(self, path):
        response = requests.put(self.api_url + "/disk/resources",
                                params={"path": path}, headers=self.headers)
        return response
