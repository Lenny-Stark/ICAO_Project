import requests
import pygame

'''
    V2=neue GUI
    Eigentliches Ziel:
    Zusätzlich noch ein Sateliten Bild oder Karte hinzufügen
    Problem: Goolge API funktioniert nicht mehr Stand: 14.10.2025 da sie an unserem Standort nicht MEHR verfügbar ist
'''

pygame.init()

# --- Fenster / Schrift ---
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("ICAO Code Eingabe - Neumorph Style")
font = pygame.font.Font(None, 32)
info_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

# Farben im Neumorph-Stil
BG_COLOR = (233, 236, 245)
SHADOW_LIGHT = (255, 255, 255)
SHADOW_DARK = (190, 195, 210)
TEXT_COLOR = (50, 50, 70)
ACTIVE_COLOR = (100, 140, 255)
BLUE_BORDER = (90, 130, 255)

# --- Eingabefeld und Button ---
input_box = pygame.Rect(280, 35, 150, 38)  
button_box = pygame.Rect(450, 35, 120, 40)
active = False
text = ""
icao_code = ""
info_lines = []

# --- API ---
def get_airport_data(icao_code):
    url = f"https://airportdb.io/api/v1/airport/{icao_code}?apiToken=9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_coordinates(data):
    lat = data["latitude_deg"]
    long = data["longitude_deg"]
    return f"Latitude: {lat}, Longitude: {long}"

def get_name(data):
    return f"Airport Name: {data['name']}"

def get_rw(data):
    rw_count = 0
    rnway_le, rnway_he = [], []
    for i in data["runways"]:
        if i:
            rw_count += 1
            rnway_le.append(i.get("le_ident"))
            rnway_he.append(i.get("he_ident"))
    return f"{rw_count} Runways: {', '.join(rnway_le)} and {', '.join(rnway_he)}"

def get_twr_freq(data):
    freqs = data.get("freqs", [])
    twr_freq = None
    for entry in freqs:
        if entry.get("type") == "TWR":
            twr_freq = entry.get("frequency_mhz")
            break
    return f"TWR-Frequenz: {twr_freq} MHz"


# --- Neumorph Helper ---
def draw_neumorph_rect(surface, rect, radius=10, pressed=False, border_color=None):
    """Zeichnet ein weiches Neumorph-Style-Rechteck mit optionalem Rand"""
    x, y, w, h = rect
    offset = 3

    if pressed:
        pygame.draw.rect(surface, SHADOW_DARK, (x, y, w, h), border_radius=radius)
        pygame.draw.rect(surface, SHADOW_LIGHT, (x + offset, y + offset, w - offset, h - offset), border_radius=radius)
    else:
        pygame.draw.rect(surface, SHADOW_LIGHT, (x - offset, y - offset, w, h), border_radius=radius)
        pygame.draw.rect(surface, SHADOW_DARK, (x + offset, y + offset, w, h), border_radius=radius)

    pygame.draw.rect(surface, BG_COLOR, (x, y, w, h), border_radius=radius)
    
    # blauer Rahmen bei Aktivität oder für Info-Box
    if border_color:
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=radius)


# --- Hauptloop ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False

            if button_box.collidepoint(event.pos):
                icao_code = text.upper()
                text = ""
                data = get_airport_data(icao_code)
                if data:
                    info_lines = [
                        get_name(data),
                        get_coordinates(data),
                        get_rw(data),
                        get_twr_freq(data)
                    ]
                else:
                    info_lines = [f"Keine Daten gefunden für {icao_code}"]

        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    icao_code = text.upper()
                    text = ""
                    data = get_airport_data(icao_code)
                    if data:
                        info_lines = [
                            get_name(data),
                            get_coordinates(data),
                            get_rw(data),
                            get_twr_freq(data)
                        ]
                    else:
                        info_lines = [f"Keine Daten gefunden für {icao_code}"]
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    # --- Hintergrund ---
    screen.fill(BG_COLOR)

    # --- Titel ---
    label = font.render("ICAO Code eingeben:", True, TEXT_COLOR)
    screen.blit(label, (40, 45))

    # --- Eingabefeld ---
    border_color = BLUE_BORDER if active else None
    draw_neumorph_rect(screen, input_box, radius=12, pressed=active, border_color=border_color)
    txt_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(txt_surface, (input_box.x + 10, input_box.y + 8))

    # --- Button ---
    hovered = button_box.collidepoint(mouse_pos)
    draw_neumorph_rect(screen, button_box, radius=12, pressed=hovered and mouse_pressed)
    btn_text = font.render("Bestätigen", True, ACTIVE_COLOR if hovered else TEXT_COLOR)
    text_rect = btn_text.get_rect(center=button_box.center)
    screen.blit(btn_text, text_rect)

    # --- Info-Box mit blauem Rand ---
    info_rect = pygame.Rect(50, 100, 600, 270)
    draw_neumorph_rect(screen, info_rect, radius=20, border_color=BLUE_BORDER)
    y_start = 130
    for line in info_lines:
        info_surface = info_font.render(str(line), True, TEXT_COLOR)
        screen.blit(info_surface, (70, y_start))
        y_start += 35

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
