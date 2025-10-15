
import pygame 

#Pantalla - Medidas
ANCHO = 850
ALTO = 550
FPS = 60

#Pantalla - Fondo
background = pygame.image.load("IMAGENES/MENU.jpg")
background = pygame.transform.scale(background,(ANCHO,ALTO))


pygame.init()


#Caracteristicas - Botones
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, spritenormal, action):
        super().__init__()
        self.image_normal = pygame.image.load(spritenormal)
        self.image_normal = pygame.transform.scale(self.image_normal, (width, height))
        self.image = self.image_normal
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action
    
    def update(self):
        mousepos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousepos):
            self.image = self.image_normal
        else: 
            self.image = self.image_normal
            
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

def StartGame():
    print("El juego comenzo")
    
def QuitGame():
    print("Saliendo del juego")
    pygame.quit()
    exit()
    
def ConfigG():
    print("Configuracion")
    
def Map():
    print("Mapa del juego")


ButtonStart = Button(
    x = ANCHO//2 - 35,
    y = ALTO//2 - 1,
    width= 230,
    height= 70,
    spritenormal = "SPRITES/Button/BotonPlayF.png",    
    action = StartGame    
)

ButtonEnd = Button(
    x = ANCHO//2 + 50,
    y = ALTO//2 + 170,
    width= 165,
    height= 66,
    spritenormal = "SPRITES/Button/BotonSalirF.png",    
    action = QuitGame  
)

ButtonConfig = Button(
    x = ANCHO//2 - 35,
    y = ALTO//2 + 87,
    width= 320,
    height= 80,
    spritenormal = "SPRITES/Button/BotonConfigF.png",    
    action = ConfigG
)

ButtonMap = Button(
    x = ANCHO//2 - 130 ,
    y = ALTO//2 + 170,
    width= 149,
    height= 69,
    spritenormal = "SPRITES/Button/BotonMapaF.png",    
    action = Map
)


allsprites = pygame.sprite.Group()
allsprites.add(ButtonStart)
allsprites.add(ButtonEnd)
allsprites.add(ButtonConfig)
allsprites.add(ButtonMap)

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
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
        
        