import requests
import pygame
import io #Stellt BytesIO zur Verfügung, um binäre Daten (z. B. Bild-Bytes) im Speicher zu halten.
from PIL import Image



API_TOKEN = "9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
MAPS_KEY = "Privater Gooogle API KEY"

ICAO = input("Geben sie den gewünschten ICAO Code ein: ")
url = f"https://airportdb.io/api/v1/airport/{ICAO}?apiToken=9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
response = requests.get(url) #response ist info die https anfrage funktioniert hat
print(response)


data = response.json() #data ist die json von der url
print(f"Flughafen Name: {data['name']}")
lat = data["latitude_deg"]
lon = data["longitude_deg"]
print(lat,lon)
url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=14&size=600x400&maptype=satellite&key={MAPS_KEY}"
img_bytes = io.BytesIO(url.content)
img = Image.open(img_bytes)
img.save("airport.png")
print("in dr if")
