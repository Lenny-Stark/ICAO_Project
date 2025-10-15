import requests
import pygame
import io #Stellt BytesIO zur Verfügung, um binäre Daten (z. B. Bild-Bytes) im Speicher zu halten.
from PIL import Image

API_TOKEN = "9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
MAPS_KEY = "Privater Google API KEY"


def get_airport_data():
    ICAO = input("Geben sie den gewünschten ICAO Code ein: ")
    url = f"https://airportdb.io/api/v1/airport/{ICAO}?apiToken=9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
    response = requests.get(url) 
    if response.status_code==200:  #Aufruf erfolgreich
        data = response.json() #data ist die json von der url
        return data
    return None

def get_coordinates(data):
    lat = data["latitude_deg"]
    lon = data["longitude_deg"]
    return lat, lon

def get_satellite_image(coordinates):
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={coordinates[0]},{coordinates[1]}&zoom=14&size=600x400&maptype=satellite&key={MAPS_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        img_bytes = io.BytesIO(r.content)
        img = Image.open(img_bytes)
        img.save("airport.png")
        return pygame.image.load("airport.png")
    return None

#print(type(get_coordinates(get_airport_data())))
airport_data=get_airport_data() #Airport data ist die json datei
coordinates=get_coordinates(airport_data)
get_satellite_image(coordinates)
