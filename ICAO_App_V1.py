import pygame

#Fernster erstellen
pygame.init()  # startet pygame
screen = pygame.display.set_mode((500, 800))  # Fenstergröße (Breite x Höhe)
pygame.display.set_caption("ICAO info")

#Button einfügen
button_rect = pygame.Rect(350, 25, 100, 60) #left, top, width, heigt
font = pygame.font.SysFont("Arial", 20)
text = font.render("Search", True, (0, 0, 0))


running = True
while running:
    # 1. Events lesen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #wann butten gedrückt wird:
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Button geklickt!")
    # 2. Logik aktualisieren
    # z.B. Mausposition, Text usw.

    # 3. Zeichnen
    screen.fill((255,255,255))  # Fenster weiß füllen
    
    # z.B. screen.blit(...)
    pygame.draw.rect(screen, (0, 200, 255), button_rect) #Zeichnet rechteck mit farbe (0,200,255), button_rect= position und größe des rechteck
    screen.blit(text, (button_rect.x + 20, button_rect.y + 15))
    pygame.display.flip()      # Bildschirm aktualisieren

    # 4. Anzeige aktualisieren
    pygame.display.flip()

pygame.quit()