import requests


class MapParser:
    def __init__(self):
        self.url = "http://static-maps.yandex.ru/1.x/"

    def get_map_image(self):
        # func must return bytes of the image
        return "some_bytes"