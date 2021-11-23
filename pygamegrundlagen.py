import pygame 
pygame.init()

#Farbplatte
ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)
BLAU    = ( 0, 0, 255)
TÜRKIS  = ( 54, 151, 177)

FENSTERBREITE = 640 


#Fenster öffnen
pygame.display.set_mode((640, 480))
screen = pygame.display.set_mode((640, 480))

#titel für Fenserkopf
pygame.display.set_caption("1. Pygame-spiel")

#Bildschirm aktualieisrung einstellen
clock = pygame.time.Clock()

# activity boolien 
gameactive = True

#definition of the variables for ball position
ballpos_x = 10 
ballpos_y = 30


#hauptroutine
while gameactive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameactive = False
            print("Spieler hat Quit-Button betätigt")
    '''   elif event.type == pygame.KEYDOWN:
            print("Spieler hat Taste gedrückt")
            
            # Taste für Spieler 1
            if event.key == pygame.K_w:
                print("Spieler hat Taste w gedrückt")
            elif event.key == pygame.K_a:
                print("Spieler hat Taste a gedrückt")
            elif event.key == pygame.K_s:
                print("Spieler hat Taste s gedrückt")
            elif event.key == pygame.K_d:
                print("Spieler hat Taste d gedrückt")
            
            # Taste für Spieler 2
            elif event.key == pygame.K_RIGHT:
                print("Spieler hat Pfeiltaste rechts gedrückt")
            elif event.key == pygame.K_LEFT:
                print("Spieler hat Pfeiltaste links gedrückt")
            elif event.key == pygame.K_UP:
                print("Spieler hat Pfeiltaste hoch gedrückt")
            elif event.key == pygame.K_DOWN:
                print("Spieler hat Pfeiltaste runter gedrückt")
            elif event.key == pygame.K_SPACE:
                print("Spieler hat Leertaste gedrückt") 
        
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Spieler hast Maus abetätigt")    '''

    # Spiellogik hier integrieren

    #Spielfeld löschen 
    screen.fill(TÜRKIS)

    #Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)
    pygame.draw.ellipse(screen, SCHWARZ, [ballpos_x, ballpos_y ,20,20])

    #moving the ball
    ballpos_x += 4
    ballpos_y += 4 

    #Fenster aktualisieren
    pygame.display.flip()

    #Refresh-Zeiten festlegen
    clock.tick(60)

pygame.quit()
