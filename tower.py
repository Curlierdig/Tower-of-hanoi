import pygame
import sys

#Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 400))
pygame.display.set_caption('Torre de Hanoi')

#colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (200, 200, 200)
COLORES_DISCOS = [
    (255, 0, 0),    
    (0, 255, 0),    
    (0, 0, 255),    
    (255, 255, 0),  
    (255, 0, 255)   
]

#fuente para texto
font = pygame.font.Font(None, 36)

class Disco:
    def __init__(self, ancho, x, y):
        self.ancho = ancho
        self.superficie = pygame.Surface((ancho, 20))
        self.superficie.fill(COLORES_DISCOS[ancho // 40 - 1])
        self.rect = self.superficie.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

class Torre:
    def __init__(self, x):
        self.x = x
        self.discos = []

def crear_torres(num_discos):
    #siempre usar 3 torres
    torres = [Torre(200 + i * 300) for i in range(3)]
    
    #crear discos en la primera torre
    for i in range(num_discos, 0, -1):
        disco = Disco(i * 40, torres[0].x, 380 - (num_discos - i) * 20)
        torres[0].discos.append(disco)
    
    return torres

def verificar_victoria(torres, num_discos):
    #verificar si todos los discos están en la última torre
    ultima_torre = torres[-1]
    
    #verificar número de discos
    if len(ultima_torre.discos) != num_discos:
        return False
    
    #verificar orden correcto (de mayor a menor)
    for i in range(len(ultima_torre.discos) - 1):
        if ultima_torre.discos[i].ancho < ultima_torre.discos[i+1].ancho:
            return False
    
    return True

def pantalla_seleccion():
    while True:
        screen.fill(BLANCO)
        
        #texto de selección
        texto_titulo = font.render("Selecciona el número de discos:", True, NEGRO)
        screen.blit(texto_titulo, (250, 100))
        
        #botones de selección
        botones = [
            pygame.Rect(250, 200, 100, 50),
            pygame.Rect(350, 200, 100, 50),
            pygame.Rect(450, 200, 100, 50)
        ]
        
        #texto de los botones
        textos_botones = ["3 Discos", "4 Discos", "5 Discos"]
        
        for i, boton in enumerate(botones):
            #dibujar botón
            pygame.draw.rect(screen, GRIS, boton)
            pygame.draw.rect(screen, NEGRO, boton, 2)
            
            #texto del botón
            texto_boton = font.render(textos_botones[i], True, NEGRO)
            texto_rect = texto_boton.get_rect(center=boton.center)
            screen.blit(texto_boton, texto_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, boton in enumerate(botones):
                    if boton.collidepoint(event.pos):
                        return i + 3  #devuelve 3, 4 o 5

def pantalla_victoria():
    screen.fill(BLANCO)
    
    #texto de victoria
    texto_victoria = font.render("¡GANASTE!", True, VERDE)
    texto_rect = texto_victoria.get_rect(center=(400, 150))
    screen.blit(texto_victoria, texto_rect)
    
    #boton de reinicio
    boton_reinicio = pygame.Rect(300, 250, 200, 50)
    pygame.draw.rect(screen, GRIS, boton_reinicio)
    pygame.draw.rect(screen, NEGRO, boton_reinicio, 2)
    
    texto_reinicio = font.render("Jugar de Nuevo", True, NEGRO)
    texto_rect = texto_reinicio.get_rect(center=boton_reinicio.center)
    screen.blit(texto_reinicio, texto_rect)
    
    pygame.display.flip()
    
    #esperar a que el usuario haga clic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(event.pos):
                    return True

def main():
    while True:
        #pantalla de selección de discos
        num_discos = pantalla_seleccion()
        
        #configuración inicial
        torres = crear_torres(num_discos)
        torre_actual = 0
        disco_seleccionado = None
        torre_objetivo = torres[-1]  #ultima torre como objetivo

        # Bucle principal del juego
        juego_en_curso = True
        while juego_en_curso:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    #cambiar torre seleccionada
                    if event.key == pygame.K_LEFT:
                        torre_actual = max(0, torre_actual - 1)
                    elif event.key == pygame.K_RIGHT:
                        torre_actual = min(len(torres) - 1, torre_actual + 1)
                    
                    #seleccionar/mover disco
                    if event.key == pygame.K_SPACE:
                        #si no hay disco seleccionado
                        if disco_seleccionado is None:
                            #seleccionar el último disco de la torre actual
                            if torres[torre_actual].discos:
                                disco_seleccionado = torres[torre_actual].discos.pop()
                                disco_seleccionado.rect.centery = 50  # Levantar disco
                        
                        #si ya hay un disco seleccionado
                        else:
                            #intentar colocar el disco
                            torre_destino = torres[torre_actual]
                            
                            #verificar si se puede colocar el disco
                            if not torre_destino.discos or disco_seleccionado.ancho < torre_destino.discos[-1].ancho:
                                #colocar disco en la nueva torre
                                disco_seleccionado.rect.centerx = torre_destino.x
                                disco_seleccionado.rect.bottom = 380 - len(torre_destino.discos) * 20
                                torre_destino.discos.append(disco_seleccionado)
                                
                                #verificar victoria
                                if verificar_victoria(torres, num_discos):
                                    if pantalla_victoria():
                                        juego_en_curso = False
                                        break
                                
                                disco_seleccionado = None

            #limpiar pantalla
            screen.fill(BLANCO)

            # Dibujar torres
            for i, torre in enumerate(torres):
                color = (200, 0, 0) if i == torre_actual else (0, 0, 0)
                pygame.draw.rect(screen, color, (torre.x - 10, 200, 20, 180))

            #dibujar discos
            for torre in torres:
                for disco in torre.discos:
                    screen.blit(disco.superficie, disco.rect)

            #dibujar disco seleccionado si existe
            if disco_seleccionado:
                screen.blit(disco_seleccionado.superficie, disco_seleccionado.rect)

            #actualizar pantalla
            pygame.display.flip()
            pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()