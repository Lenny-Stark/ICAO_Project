import requests
import pygame

pygame.init()

# --- Fenster / Schrift ---
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("ICAO Code Eingabe")
font = pygame.font.Font(None, 32)
info_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

# --- Eingabefeld ---
input_box = pygame.Rect(260, 35, 200, 30)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ""
icao_code = ""

# --- Platz für Informationen ---
# (werden nach Enter neu befüllt)
info_lines = []

# --- Beispielhafte Funktionen, die später echte API-Aufrufe sein können ---
#funktion muss Sting zurückgeben
API_TOKEN = "9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"


def get_airport_data(icao_code):
    url = f"https://airportdb.io/api/v1/airport/{icao_code}?apiToken=9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
    response = requests.get(url) 
    if response.status_code==200:  #Fehlerbehandlung
        data = response.json() #data ist die json von der url
        return data
    return None

def get_coordinates(data):
    lat = data["latitude_deg"]
    long = data["longitude_deg"]
    return f"Latitude:{lat}, Longitude{long}"

def get_name(data):
    #get airport name
    airport_name= data["name"]
    return f"airport name: {airport_name}"

def get_rw(data):
    rw_count=0
    rnway_le=[]
    rnway_he=[]
    for i in data["runways"]:
        if i:
            rw_count += 1
        rnway_le.append(i.get("le_ident"))
        rnway_he.append(i.get("he_ident"))
    return f"{rw_count} Runways: {','.join(rnway_le)} and {','.join(rnway_he)}"

def get_twr_freq(data):
    freqs = data.get("freqs", [])
    twr_freq=None
    for entry in freqs:
        if entry.get("type") == "TWR":
            twr_freq = entry.get("frequency_mhz")
            break

    return f"TWR-Frequenz: {twr_freq} MHz"


# --- Hauptloop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Klick in die Eingabebox?
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            color = color_active if active else color_inactive

        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    icao_code = text.upper()
                    print("Eingegebener ICAO Code:", icao_code)

                    # Eingabefeld leeren
                    text = ""
                    data = get_airport_data(icao_code)
                    # 🔹 Hier rufen wir unsere einzelnen Funktionen auf
                    info_lines = [
                        get_name(data),
                        get_coordinates(data),
                        get_rw(data),
                        get_twr_freq(data)
                    ]

                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    # --- Hintergrund ---
    screen.fill((255, 255, 255))

    # --- Beschriftung links oben ---
    label = font.render("ICAO Code eingeben:", True, (0, 0, 0))
    screen.blit(label, (30, 40))

    # --- Eingabefeld mit Text ---
    txt_surface = font.render(text, True, (0, 0, 0))
    input_box.w = max(200, txt_surface.get_width() + 10)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    # --- Informationen anzeigen ---
    y_start = 120
    for line in info_lines:
        info_surface = info_font.render(str(line), True, (0, 0, 0))
        text_rect = info_surface.get_rect(center=(screen.get_width() / 2, y_start))
        screen.blit(info_surface, text_rect)
        y_start += 35

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
