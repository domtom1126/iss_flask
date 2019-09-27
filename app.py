from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from geopy.geocoders import Nominatim
from haversine import haversine, Unit

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless")
geolocator = Nominatim(user_agent='ISS_Tracker')
driver = webdriver.Chrome(chrome_options=chrome_options)
url = driver.get('http://wsn.spaceflight.esa.int/iss/index_portal.php')

iss_latitude = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
    (By.XPATH, "//div[text()='Latitude']//following::div[1]"))).get_attribute("innerHTML")

iss_latitude_float = (float(iss_latitude.split(" ")[0].replace(",", ".")))

iss_longitude = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
    (By.XPATH, "//div[text()='Longitude']//following::div[1]"))).get_attribute("innerHTML")

iss_longitude_float = (
    float(iss_longitude.split(" ")[0].replace(",", ".")))

iss_speed = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
    (By.XPATH, "//div[text()='Speed']//following::div[1]"))).get_attribute("innerHTML")
int_iss_speed = [iss_speed.replace("km/h", "") for speed in iss_speed]

iss_location = iss_latitude_float, iss_longitude_float

driver.close()


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/<user_city>', methods=['GET', 'POST'])
def user_city(user_city):
    user_city = request.form['user_city']
    geolocator = Nominatim()
    user_location = geolocator.geocode(user_city)
    user_coor = user_location.latitude, user_location.longitude
    distance = haversine(user_coor, iss_location, unit=Unit.MILES)
    return render_template('city.html', user_city=user_coor, distance=distance)
