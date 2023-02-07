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

        self.zoom = 10  # Показатель зума

        self.layer = 'map'  # текущий слой

        self.check_click_for_index = False  # показатель из 9 задачи
        self.point = None  # показатель из 6 задачи

        self.mapParser = MapParser()

        self.show_map()
        self.maps_view.setFocus()
        self.search_button.clicked.connect(self.check_for_index)
        self.layer_map_btn.clicked.connect(self.set_layer)
        self.layer_sat_btn.clicked.connect(self.set_layer)
        self.radioButton_3.clicked.connect(self.set_layer)
        # self.s

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
        self.show_map()

    def set_layer(self):
        if self.layer_map_btn.isChecked():
            self.layer = 'map'
        elif self.layer_sat_btn.isChecked():
            self.layer = 'sat'
        else:
            self.layer = 'sat,skl'
        self.mapParser.change_layer(self.layer)
        self.show_map()

    def show_map(self):
        # loading map image
        map = QPixmap()

        map.loadFromData(self.mapParser.get_map_image())

        self.maps_view.setPixmap(map)

    def keyPressEvent(self, event):
        v_shift = 0
        h_shift = 0
        speed = 1 / self.zoom
        if event.key() == Qt.Key_Escape:
            self.maps_view.setFocus()
            print(1)
        if event.key() == Qt.Key_PageUp:
            if self.zoom < 17:
                self.zoom += 1
        elif event.key() == Qt.Key_PageDown:
            if self.zoom > 1:
                self.zoom -= 1
        if event.key() == Qt.Key_Left:
            h_shift -= speed
        if event.key() == Qt.Key_Up:
            v_shift += speed
        if event.key() == Qt.Key_Right:
            h_shift += speed
        if event.key() == Qt.Key_Down:
            v_shift -= speed
        self.mapParser.zoom = self.zoom
        self.mapParser.move(h_shift, v_shift)
        self.mapParser.refresh_map()
        self.show_map()
        print(f'zoom: {self.zoom},h_shift: {h_shift},v_shift {v_shift}')

