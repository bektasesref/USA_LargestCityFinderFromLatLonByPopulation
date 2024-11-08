import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from fake_useragent import UserAgent


useGUI = False
lat = 45.0358911
lon = -109.5215668


def get_county_by_coordinates(latitude, longitude):

    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }

    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=10&addressdetails=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'address' in data and 'county' in data['address']:
        country = data['address']['country']
        state = data['address']['state']
        county = data['address']['county']
        bounding_box = data['boundingbox']
        print(f"Country: {country}")
        print(f"State: {state}")
        print(f"County: {county}")
        print(f"Bounding Box: {bounding_box}")
        return country, state, county, bounding_box
    else:
        return None


def get_largest_city_by_population_in_county(county_name, state_name, bounding_box):
    south, north, west, east = bounding_box

    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
        [out:json];
        (
          node["place"="city"]({south},{west},{north},{east});
          node["place"="town"]({south},{west},{north},{east});
        );
        out body;
        """

    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }

    response = requests.post(overpass_url, data={'data': query}, headers=headers)
    data = response.json()
    cities = data.get('elements', [])

    if not cities:
        print(f"No cities found in {county_name}, {state_name}.")
        return None

    largest_city = max(cities, key=lambda x: int(x.get('tags', {}).get('population', 0)), default=None)
    if largest_city:
        city_name = largest_city['tags']['name']
        print(f"The largest city in {county_name}, {state_name}, is {city_name}.")
        return city_name
    else:
        print(f"Could not determine the largest city in {county_name}, {state_name}.")
        return None

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Largest City Finder')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.title_label = QLabel('Enter Coordinates to Find the Largest City')
        layout.addWidget(self.title_label)

        self.lat_input = QLineEdit(self)
        self.lat_input.setPlaceholderText('Enter Latitude')
        layout.addWidget(self.lat_input)

        self.lon_input = QLineEdit(self)
        self.lon_input.setPlaceholderText('Enter Longitude')
        layout.addWidget(self.lon_input)

        self.get_button = QPushButton('Get', self)
        self.get_button.clicked.connect(self.on_click)
        layout.addWidget(self.get_button)

        self.result_label = QLabel('', self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def on_click(self):
        try:
            latitude = self.lat_input.text()
            longitude = self.lon_input.text()
        except ValueError:
            self.result_label.setText('Invalid coordinates. Please enter valid numbers.')
            return
        county_info = get_county_by_coordinates(latitude, longitude)
        if county_info:
            country_name, state_name, county_name, bounding_box = county_info
            result = get_largest_city_by_population_in_county(county_name, state_name, bounding_box)
            self.result_label.setText(result)
        else:
            self.result_label.setText('No county found within the specified coordinates.')


if __name__ == '__main__':
    if useGUI:
        app = QApplication(sys.argv)
        ex = App()
        ex.show()
        sys.exit(app.exec_())
    else:
        county_info = get_county_by_coordinates(lat, lon)
        #county_info = "United States","California","Alameda County",["37.4542627","37.9066896","-122.3738430","-121.4690903"] #test purpose only
        if county_info:
            country_name, state_name, county_name, bounding_box = county_info
            get_largest_city_by_population_in_county(county_name, state_name, bounding_box)