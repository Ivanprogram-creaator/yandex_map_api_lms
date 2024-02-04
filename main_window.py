from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from PIL import Image
from io import BytesIO


class Map(QMainWindow):
    def __init__(self):
        self.marker = None
        self.search = None
        self.textedit = None
        self.switch = None
        self.pic = None
        self.pic_label = None
        self.API = 'https://static-maps.yandex.ru/1.x/'
        self.API_GEOCODER = 'http://geocode-maps.yandex.ru/1.x/'
        self.API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
        self.kind = 'sat,skl'
        try:
            self.longitude = float(input('Введите долготу >>> '))
            self.latitude = float(input('Введите широту  >>> '))
            self.length = float(input('Введите протяженность области показа карты >>> '))
        except Exception:
            print('Неверный ввод. Должно быть числом с плавающей точкой')
            quit()
        super().__init__()
        self.setWindowTitle('Map preview')
        self.setGeometry(100, 100, 1000, 500)
        self.creator()
        self.show_pic()
        self.switcher()

    def creator(self):
        self.switch = QPushButton(self)
        self.switch.setGeometry(10, 10, 150, 30)
        self.switch.clicked.connect(self.switcher)
        self.switch.show()

        self.textedit = QTextEdit(self)
        self.textedit.setGeometry(170, 10, 150, 30)
        self.textedit.show()

        self.search = QPushButton(self)
        self.search.setGeometry(330, 10, 150, 30)
        self.search.clicked.connect(self.searcher)
        self.search.setText('Искать')
        self.search.show()

        self.search = QPushButton(self)
        self.search.setGeometry(490, 10, 170, 30)
        self.search.clicked.connect(self.delete_marker)
        self.search.setText('Сброс поискового результата')
        self.search.show()

    def delete_marker(self):
        self.textedit.setText('')
        self.marker = None
        self.new_map()

    def searcher(self):
        if not self.textedit.toPlainText():
            return None
        params = {
            "apikey": self.API_KEY,
            "geocode": self.textedit.toPlainText(),
            "format": 'json'
        }

        response = requests.get(self.API_GEOCODER, params)
        if response.status_code != 200:
            print(response.reason)
            quit()
        self.longitude, self.latitude = map(lambda x: float(x), response.json()["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]["Point"]["pos"].split(" "))
        self.length = 0.1
        self.marker = ",".join([str(self.longitude), str(self.latitude), 'pm2blm'])
        self.new_map()

    def show_pic(self, name='map'):
        pic = QPixmap(f"{name}.png")
        pic_label = QLabel(self)
        pic_label.setGeometry(10, 60, pic.width(), pic.height())
        pic_label.setPixmap(pic)
        pic_label.show()

    def switcher(self):
        kinds = {'map': 'sat', 'sat': 'sat,skl', 'sat,skl': 'map'}
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
        if self.marker:
            params['pt'] = self.marker
        response = requests.get(self.API, params)
        if response.status_code != 200:
            print(response.reason)
            quit()
        Image.open(BytesIO(response.content)).save(f'{name}.png')
        self.show_pic(name=name)
