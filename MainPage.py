from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow

from lib.maps_stuff.map_parser import MapParser
from lib.windows.main_window import Ui_MainWindow


class MainPage(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__(self)

        self.setupUi(self)

        self.mapParser = MapParser()

    def update_map(self):
        pass

    def get_map(self):
        pass

    def show_map(self):
        map = QPixmap(self.mapParser.get_map_image())

        self.maps_view.setPixmap(map)