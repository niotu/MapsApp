from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow

from lib.maps_stuff.map_parser import MapParser
from lib.windows.main_window import Ui_MainWindow


class MainPage(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.v_shift = 0  # Сдвиг карты по вертикали
        self.h_shift = 0  # Сдвиг карты по горизонтали

        self.zoom = 1  # Показатель зума

        self.layer = 'map'  # текущий слой

        self.check_click_for_index = False  # показатель из 9 задачи
        self.point = None  # показатель из 6 задачи

        self.mapParser = MapParser()

        self.show_map()
        self.maps_view.setFocus()
        self.search_button.clicked.connect(self.check_for_index)

    def check_for_index(self):
        self.check_click_for_index = not self.check_for_index
        self.mapParser.search_place(self.mapParser.search_place(self.lineEdit.text()))
        self.mapParser.get_map_image()
        self.show_map()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print(event.pos())

        self.set_layer()

        print(self.layer)
        self.check_for_index()

    def set_layer(self):
        if self.layer_map_btn.isChecked():
            self.layer = 'map'
        elif self.layer_sat_btn.isChecked():
            self.layer = 'sat'
        else:
            self.layer = 'sat,skl'
        self.mapParser.change_layer(self.layer)


    def show_map(self):
        # loading map image
        map = QPixmap()

        map.loadFromData(self.mapParser.get_map_image())

        self.maps_view.setPixmap(map)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.zoom / 1.5 > 0.001:
                self.zoom /= 1.5
        elif event.key() == Qt.Key_PageDown:
            if self.zoom * 1.5 < 90:
                self.zoom *= 1.5
        if event.key() == Qt.Key_Left:
            if 0 < self.h_shift - self.zoom < 180:
                self.h_shift -= self.zoom
        if event.key() == Qt.Key_Up:
            if -90 < self.v_shift + self.zoom < 90:
                self.v_shift += self.zoom
        if event.key() == Qt.Key_Right:
            if 0 < self.h_shift + self.zoom < 180:
                self.h_shift += self.zoom
        if event.key() == Qt.Key_Down:
            if -90 < self.v_shift - self.zoom < 90:
                self.v_shift -= self.zoom
        print(f'zoom: {self.zoom},h_shift: {self.h_shift},v_shift {self.v_shift}')
