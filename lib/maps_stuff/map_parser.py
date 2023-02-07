import requests


class MapParser:
    def __init__(self):
        self.url = "http://static-maps.yandex.ru/1.x/"
        self.ll = None
        self.spn = None

    def get_map_image(self):
        s = requests.Session()
        r = s.request('GET', self.url)
        content = r.content  # bytes
        return content

    def search_place(self):
        pass
