import requests

apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"


def get_params(toponym):
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = [toponym_longitude, toponym_lattitude]
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split()
    r, t = envelope["upperCorner"].split()

    dx = abs(float(l) - float(r)) / 2
    dy = abs(float(t) - float(b)) / 2
    span = f"{dx},{dy}"
    return ll, span


class MapParser:
    def __init__(self):
        self.url = "http://static-maps.yandex.ru/1.x/"
        self.geocoder_params = {
            "apikey": apikey,
            "geocode": None,
            "format": "json"
        }
        self.map_params = {
            "ll": None,
            "spn": None,
            "l": "map",
            "pt": None,
            "z": 10
        }
        self.ll = None
        self.spn = None
        self.layer = "sat,skl"
        self.zoom = 10
        self.point = None

    def get_map_image(self):
        s = requests.Session()
        r = s.request('GET', self.url, params=self.map_params)
        content = r.content  # bytes
        # response = requests.get(self.url, params=self.map_params)
        # content = response.content
        return content

    def change_layer(self, layer):
        self.layer = layer
        self.map_params["l"] = self.layer

    def clear_point(self):
        self.point = None
        self.refresh_map()

    def move(self, dx, dy):
        # print(self.ll)
        self.ll[0] = str(float(self.ll[0]) + dx)
        self.ll[1] = str(float(self.ll[1]) + dy)
        res = ",".join(self.ll)
        self.map_params["ll"] = res

    def search_place(self, toponym_to_find):
        self.geocoder_params["geocode"] = toponym_to_find
        response = requests.get(geocoder_api_server, params=self.geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            return
        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        self.ll, spn = get_params(toponym)
        self.point = ",".join(self.ll)
        # Собираем параметры для запроса к StaticMapsAPI:
        self.refresh_map()

    def refresh_map(self):
        self.map_params = {
            "ll": ",".join(self.ll),
            "l": self.layer,
            "pt": self.point,
            "z": self.zoom
        }
