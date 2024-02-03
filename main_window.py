from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from PIL import Image
from io import BytesIO


class Map(QMainWindow):
    def __init__(self):
        self.API = 'https://static-maps.yandex.ru/1.x/'
        try:
            self.longitude = float(input('Введите долготу >>> '))
            self.latitude = float(input('Введите широту  >>> '))
            self.length = float(input('Введите протяженность области показа карты >>> '))
        except Exception:
            print('Неверный ввод. Должно быть числом с плавающей точкой')
            quit()
        super().__init__()
        self.pic = None
        self.pic_label = None
        self.setWindowTitle('Map preview')
        self.setGeometry(100, 100, 1000, 500)
        self.show_pic()

    def show_pic(self, name='map'):
        pic = QPixmap(f"{name}.png")
        pic_label = QLabel(self)
        pic_label.setGeometry(10, 10, pic.width(), pic.height())
        pic_label.setPixmap(pic)
        pic_label.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.length = self.length + self.length / 10
            self.new_map()
        elif event.key() == Qt.Key_PageDown:
            self.length = self.length - self.length / 10
            self.new_map()

    def new_map(self, name='map'):
        if 0 >= float(self.length) >= 25:
            print('crash')
            return None
        params = {
            "ll": ",".join([str(self.longitude), str(self.latitude)]),
            "spn": ",".join([str(self.length), str(self.length)]),
            "l": "map"
        }

        response = requests.get(self.API, params)
        if response.status_code != 200:
            print(response.reason)
            quit()
        Image.open(BytesIO(response.content)).save(f'{name}.png')
        self.show_pic(name=name)
