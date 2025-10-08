import gmplot
import requests
import pygame
import io #Stellt BytesIO zur Verfügung, um binäre Daten (z. B. Bild-Bytes) im Speicher zu halten.
from PIL import Image

API_TOKEN = "9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
MAPS_KEY = "AIzaSyAChzelYp5YLjzy-lYgCHLRuGsv1RizfLc"

# Fenstergröße
WIDTH, HEIGHT = 800, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ICAO Flughafen Info")

font = pygame.font.SysFont("Arial", 24)
input_box = pygame.Rect(50, 50, 200, 40)
color_inactive = pygame.Color('white')
color_active = pygame.Color('red')
color = color_inactive
active = False
text = ""

def get_airport_data():
    ICAO = input("Geben sie den gewünschten ICAO Code ein: ")
    url = f"https://airportdb.io/api/v1/airport/{ICAO}?apiToken=9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
    response = requests.get(url) 
    if response.status_code==200:  #Fehlerbehandlung
        data = response.json() #data ist die json von der url
        return data
    return None

def get_coordinates(data):
    lat = data["latitude_deg"]
    long = data["longitude_deg"]
    return lat, long

def get_satellite_image(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=14&size=600x400&maptype=satellite&key={MAPS_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        img_bytes = io.BytesIO(r.content)
        img = Image.open(img_bytes)
        img.save("airport.png")
        return pygame.image.load("airport.png")
    return None
# Coordinates for Innsbruck, Austria

latitude,longitude=get_coordinates(get_airport_data())
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    airport_info = get_airport_data()
                    if airport_info and "location" in airport_info:
                        lat = airport_info["location"]["latitude"]
                        lon = airport_info["location"]["longitude"]
                        airport_img = get_satellite_image(lat, lon)
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill((30, 30, 30))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

    if airport_info:
        name = airport_info.get("name", "Unbekannt")
        city = airport_info.get("city", "Unbekannt")
        country = airport_info.get("country", "Unbekannt")

        info_text = font.render(f"{name} - {city}, {country}", True, (255, 255, 255))
        screen.blit(info_text, (50, 120))

    if airport_img:
        screen.blit(airport_img, (50, 200))

    pygame.display.flip()

pygame.quit()