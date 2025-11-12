import tkinter as tk
import pygame
import sys
import time

#Medidas y Colores - Pygame
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (20, 80, 20)
ANCHO, ALTO, FPS = 850, 550, 60


#Funcion - Recoleccion de datos
def GlobalData():
    global nombre_usuario, edad_usuario
    nombre_usuario = entry_nombre.get()
    edad_usuario = entry_edad.get()

    # Cerrar ventana Tkinter
    ventana.destroy()
    print("Iniciando juego...")

# Crear ventana Tkinter
ventana = tk.Tk()
ventana.title("Recoleccion de Datos")

tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

tk.Label(ventana, text="Edad:").grid(row=1, column=0, padx=10, pady=10)
entry_edad = tk.Entry(ventana)
entry_edad.grid(row=1, column=1, padx=10, pady=10)

tk.Button(ventana, text="Continuar", command=GlobalData).grid(row=2, column=0, columnspan=2, pady=10)

ventana.mainloop()



pygame.init()
print("Bienvenido a la Aventura UNAL")

#Fuente del Texto - Datos
fuente = pygame.font.SysFont("Highland Gothic", 20)
texto = f"Nombre: {nombre_usuario} | Edad: {edad_usuario}"

#Pantalla - Fondo
background = pygame.image.load("IMAGENES/MENU.jpg")
background = pygame.transform.scale(background,(ANCHO,ALTO))


#Caracteristicas - Botones
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, spritenormal, spritehover, action):
        super().__init__()
        self.image_normal = pygame.transform.scale(pygame.image.load(spritenormal), (width, height))
        self.image_hover = pygame.transform.scale(pygame.image.load(spritehover), (width, height))
        self.image = self.image_normal
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action
        self.pressed = False
    
    def update(self):
        if self.pressed:
            self.image = self.image_hover
        else:
            self.image = self.image_normal
            
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True  # Cambia sprite al presionar
                self.action()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False  # Vuelve a sprite normal al soltar                         


#Acciones - Botones
def StartGame():
    print("Iniciando...")
    LoadingScreen(pantalla)
    print("El juego comenzó ✅")

    running_game = True
    clock = pygame.time.Clock()

    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False  # Cierra el juego y regresa al menú

        # Fondo del juego
        pantalla.fill(VERDE)

        # Texto de bienvenida
        texto_juego = fuente.render("¡Bienvenido a la Aventura UNAL!", True, BLANCO)
        pantalla.blit(texto_juego, (ANCHO // 2 - texto_juego.get_width() // 2, ALTO // 2))

        Information = fuente.render(f"Jugador: {nombre_usuario} | Edad: {edad_usuario}", True, BLANCO)
        pantalla.blit(Information, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)
    print("Saliendo del modo juego y volviendo al menú...")

def QuitGame():
    print("Saliendo del juego...")
    pygame.quit()
    raise SystemExit

def ConfigG():
    print("Configuracion")

def Map():
    print("Mapa del juego")


#Pantalla de Carga
def LoadingScreen(pantalla):
    ANCHO, ALTO = pantalla.get_size()
    clock = pygame.time.Clock()
    fuente_carga = pygame.font.Font("FUENTES/ORBITRON/ORBitron.ttf", 30)

    # Efecto de oscurecimiento progresivo
    for alpha in range(0, 180, 8):
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.fill(NEGRO)
        overlay.set_alpha(alpha)
        pantalla.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(30)

    # Mostrar texto "CARGANDO..."
    pantalla.fill(NEGRO)
    texto_carga = fuente_carga.render("CARGANDO...", True, BLANCO)
    pantalla.blit(
        texto_carga,
        (ANCHO // 2 - texto_carga.get_width() // 2, ALTO // 2 - texto_carga.get_height() // 2),
    )
    pygame.display.flip()

    # Tiempo de Carga
    time.sleep(5)


#Botones - Menu
ButtonStart = Button(
    x = ANCHO//2 - 35,
    y = ALTO//2 - 1,
    width= 230,
    height= 70,
    spritenormal = "SPRITES/Button/BotonPlayF.png",
    spritehover = "SPRITES/Button/BotonPlayFHover.png",    
    action = StartGame    
)

ButtonEnd = Button(
    x = ANCHO//2 + 50,
    y = ALTO//2 + 170,
    width= 165,
    height= 66,
    spritenormal = "SPRITES/Button/BotonSalirF.png",    
    spritehover = "SPRITES/Button/BotonSalirFHover.png",    
    action = QuitGame  
)

ButtonConfig = Button(
    x = ANCHO//2 - 35,
    y = ALTO//2 + 87,
    width= 320,
    height= 80,
    spritenormal = "SPRITES/Button/BotonConfigF.png", 
    spritehover = "SPRITES/Button/BotonConfigFHover.png" ,      
    action = ConfigG
)

ButtonMap = Button(
    x = ANCHO//2 - 130 ,
    y = ALTO//2 + 170,
    width= 149,
    height= 69,
    spritenormal = "SPRITES/Button/BotonMapaF.png",   
    spritehover = "SPRITES/Button/BotonMapaFHover.png",     
    action = Map
)


#Insertar Sprites - Botones
allsprites = pygame.sprite.Group()
allsprites.add(ButtonStart)
allsprites.add(ButtonEnd)
allsprites.add(ButtonConfig)
allsprites.add(ButtonMap)


#Configuracion Basica - Pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Vive la aventura UNAL")
clock = pygame.time.Clock()


#Bucle Principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        ButtonStart.handle_event(event)
        ButtonEnd.handle_event(event)
        ButtonConfig.handle_event(event)
        ButtonMap.handle_event(event)
           
    allsprites.update()        
    pantalla.blit(background,(0,0))
    allsprites.draw(pantalla)
    
    superficie_texto = fuente.render(texto, True, (255, 255, 255))
    rect_texto = superficie_texto.get_rect(topright=(ANCHO - 20, 40))
    pantalla.blit(superficie_texto, rect_texto)
    
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
        
        
        

