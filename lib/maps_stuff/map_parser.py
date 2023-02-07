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
            "pt": None
        }
        self.ll = None
        self.spn = None
        self.layer = "sat,skl"

    def get_map_image(self):
        s = requests.Session()
        r = s.request('GET', self.url, params=self.map_params)
        content = r.content  # bytes
        # response = requests.get(self.url, params=self.map_params)
        # content = response.content
        return content

    def change_layer(self, layer):
        self.layer = layer

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
        ll, spn = get_params(toponym)

        # Собираем параметры для запроса к StaticMapsAPI:
        self.map_params = {
            "ll": ",".join(ll),
            "spn": spn,
            "l": self.layer,
            "pt": ",".join(ll)
        }
