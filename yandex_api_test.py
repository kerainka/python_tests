import unittest
from yandex_client import YandexApi

YANDEX_TOKEN = ""
YANDEX_API_URL = "https://cloud-api.yandex.net/"
YANDEX_API_VERSION = "v1"

client = YandexApi(YANDEX_TOKEN, YANDEX_API_URL, YANDEX_API_VERSION)


class TestYandexApiCreateFolder(unittest.TestCase):

    def setUp(self):
        client.delete_folder("test")

    def tearDown(self):
        pass

    def test_response_status(self):
        response = client.create_folder("test")
        self.assertEqual(201, response.status_code)

    def test_folder_in_catalog(self):
        client.create_folder("test")
        response = client.get_folders("/")
        self.assertEqual(200, response.status_code)
        items = response.json()["_embedded"]["items"]
        exists = False
        for item in items:
            if item["name"] == "test":
                exists = True
        self.assertTrue(exists)

    def test_folder_already_exists(self):
        client.create_folder("test")
        response = client.create_folder("test")
        self.assertEqual(409, response.status_code)

    def test_invalid_path(self):
        response = client.create_folder("")
        self.assertEqual(400, response.status_code)


if __name__ == "__main__":
    unittest.main()
