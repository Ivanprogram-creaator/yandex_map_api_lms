import sys
import requests

from PIL import Image
from io import BytesIO
from PyQt5.QtWidgets import QApplication

from main_window import Map

API = 'https://static-maps.yandex.ru/1.x/'
# API_KEY = ''

try:
    longitude = str(float(input('Введите долготу >>> ')))
    latitude = str(float(input('Введите широту  >>> ')))
    length = str(float(input('Введите протяженность области показа карты >>> ')))
except Exception:
    print('Неверный ввод. Должно быть числом с плавающей точкой')
    quit()

params = {
    "ll": ",".join([longitude, latitude]),
    "spn": ",".join([length, length]),
    "l": "map"
}

response = requests.get(API, params)
if response.status_code != 200:
    print(response.reason)
    quit()

Image.open(BytesIO(response.content)).save('map.png')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Map()
    window.show()
    sys.exit(app.exec())
