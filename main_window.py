from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from PIL import Image
from io import BytesIO


class Map(QMainWindow):
    def __init__(self):
        self.API = 'https://static-maps.yandex.ru/1.x/'
        self.kind = 'hybrid'
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
        self.switch = QPushButton(self)
        self.switch.setGeometry(10, 10, 150, 30)
        self.switch.clicked.connect(self.switcher)
        self.switch.show()
        self.switcher()

    def show_pic(self, name='map'):
        pic = QPixmap(f"{name}.png")
        pic_label = QLabel(self)
        pic_label.setGeometry(10, 60, pic.width(), pic.height())
        pic_label.setPixmap(pic)
        pic_label.show()

    def switcher(self):
        kinds = {'map': 'sat', 'sat': 'map', 'hybrid': 'map'}
        self.kind = kinds[self.kind]
        self.switch.setText(f'Режим на {self.kind}')
        self.new_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.length += self.length / 10
        elif event.key() == Qt.Key_PageDown:
            self.length -= self.length / 10
        elif event.key() == Qt.Key_Right:
            self.longitude += self.length
        elif event.key() == Qt.Key_Left:
            self.longitude -= self.length
        elif event.key() == Qt.Key_Up:
            self.latitude += self.length
        elif event.key() == Qt.Key_Down:
            self.latitude -= self.length
        self.new_map()

    def new_map(self, name='map'):
        if (0 >= self.length >= 25) or (-90 >= self.latitude >= 90) or (-180 >= self.length >= 180):
            return None
        params = {
            "ll": ",".join([str(self.longitude), str(self.latitude)]),
            "spn": ",".join([str(self.length), str(self.length)]),
            "l": self.kind
        }

        response = requests.get(self.API, params)
        if response.status_code != 200:
            print(response.reason)
            quit()
        Image.open(BytesIO(response.content)).save(f'{name}.png')
        self.show_pic(name=name)
