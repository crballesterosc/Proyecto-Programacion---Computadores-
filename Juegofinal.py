import tkinter as tk
import pygame
import time
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("FIREBASE/firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


#Colores - Pygame
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
GRIS = (128, 128, 128)
ROJO = (200, 50, 50)
MARRON = (160, 90, 40)
ANCHO, ALTO, FPS = 800, 550, 60

#Medidas - Pygame
ANCHOG, ALTOG , FPSG = 1280,720,60
WSLIDER = 375
HSLIDER = 60
W_PSLIDER = 40
H_PSLIDER = 40
SRANGEI = 0 
SRANGEF = 100

#Datos - JUGADOR
SCORE = 50
VIDAS = 10
SKIN = "UNAL Student"
SONIDO = 0

running = True


#Pantalla - Tkinter(Jugador)
def TKINTER_SCREEN():
    nombre_usuario = None

    def GlobalData():
        nonlocal nombre_usuario
        nombre_usuario = entry_nombre.get()
        
        valido = True
        
        if not nombre_usuario:
            LNombre.config(text="Incorrecto", fg="red")
            valido = False
        else:
            LNombre.config(text="Correcto :D", fg="green")
    
        if valido:
            db.collection("Usuarios").document(nombre_usuario).set({
                "Jugador": nombre_usuario,
                "Puntaje": SCORE,
                "Volumen": SRANGEI
            })
            ventana.destroy()
        else:
            print("Porfavor ingrese su usuario!")
    
    ventana = tk.Tk()
    ventana.title("Recolección de Datos")
    ventana.protocol("WM_DELETE_WINDOW", lambda: None)

    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
    LNombre = tk.Label(ventana, text=" ...", fg="black")
    LNombre.grid(row=0, column=2, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(ventana, text="Continuar",
              command=lambda: GlobalData()).grid(row=2, column=0, columnspan=2, pady=10)

    ventana.mainloop()
    return nombre_usuario

nombre_usuario = TKINTER_SCREEN()




#Crear la coleccion en Firebase y funcion de actualizacion de datos
def SAVE_DATA_FB(Sound, Score, Lifes, Skin):
    db.collection("Juego - PC").document(nombre_usuario).set({
        "Jugador": nombre_usuario,
        "Volumen": Sound,
        "Puntaje": Score,
        "Vidas": Lifes,
        "Skin": Skin,
    }, merge=True)

def UPLOAD_DATA():
    doc = db.collection("Juego - PC").document(nombre_usuario).get()
    if doc.exists:
        return doc.to_dict()
    return None

SAVE_DATA_FB(SONIDO, SCORE, VIDAS, SKIN)





pygame.init()
print("Bienvenido a la Aventura UNAL")

fuente_carga = pygame.font.Font("FUENTES/ORBITRON/ORBitron.ttf", 30)


#Funciones - Cambio de Tamaño(Pantalla)
def RESIZE_LOAD(nuevo_ancho, nuevo_alto, fondo_original=None):
    global pantalla, ANCHO, ALTO

    ANCHO, ALTO = nuevo_ancho, nuevo_alto
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)

    if fondo_original:
        return pygame.transform.scale(fondo_original, (ANCHO, ALTO))
    return None

def RESTORE_SIZE():
    global pantalla, ANCHO, ALTO, background

    ANCHO, ALTO = 800, 550
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)

    fondo_menu = pygame.image.load("IMAGENES/MENU.jpg")
    background = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))



# Fuente del Texto - Datos
fuente = pygame.font.SysFont("Highland Gothic", 20)
texto = f"Jugador: {nombre_usuario}"

# Pantalla - Fondo
background = pygame.image.load("IMAGENES/MENU.jpg")
background = pygame.transform.scale(background, (ANCHO, ALTO))

# Configuración Básica - Pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Vive la aventura UNAL")
clock = pygame.time.Clock()




# Caracteristicas - Texto
class Texto:
    def __init__(self, texto, color, size, fuente, x, y):
        self.texto = texto
        self.color = color
        self.fuente = pygame.font.Font(fuente, size)
        self.render = self.fuente.render(self.texto, True, self.color)
        self.x = x
        self.y = y
        
    def set_text(self, nuevo_texto):
        self.texto = nuevo_texto
        self.render = self.fuente.render(self.texto, True, self.color)
    
    def Position(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, pantalla):
        pantalla.blit(self.render, (self.x, self.y))


# Características - Botones
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
        self.image = self.image_hover if self.pressed else self.image_normal
            
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                self.action()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False


# Caracteristicas - Sliders
class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, minvalue, maxvalue, spritethumb, spritebar):
        super().__init__()
        self.x = x
        self.y = y
        self.ancho = width
        self.alto = height
        
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.value = minvalue
        
        self.thumb = pygame.image.load(spritethumb).convert_alpha()
        self.thumb = pygame.transform.scale(self.thumb, (W_PSLIDER, H_PSLIDER))
        
        self.sprite_bar = pygame.image.load(spritebar).convert_alpha()
        self.sprite_bar = pygame.transform.scale(self.sprite_bar, (width, height))
        
        self.background = self.sprite_bar
        self.rect = self.background.get_rect(topleft=(x, y))

        thumb_y = y + (self.rect.height - self.thumb.get_height()) // 2
        self.thumb_rect = self.thumb.get_rect(topleft=(self.x, thumb_y))
        
        self.dragging = False
    
    def update(self, mouse_x):
        if self.dragging:
            min_x = self.x
            max_x = self.x + self.ancho - self.thumb_rect.width            
            new_x = mouse_x - self.thumb_rect.width // 2
            self.thumb_rect.x = max(min_x, min(new_x, max_x))

            porcentaje = (self.thumb_rect.x - min_x) / (max_x - min_x)
            self.value = self.minvalue + porcentaje * (self.maxvalue - self.minvalue)
            
    def draw(self, pantalla):
        pantalla.blit(self.background, self.rect.topleft)
        pantalla.blit(self.thumb, self.thumb_rect.topleft)
        
    def get_value(self):
        return round(self.value)

def gestionar_slider(event, slider):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if slider.thumb_rect.collidepoint(event.pos):
            slider.dragging = True
    elif event.type == pygame.MOUSEBUTTONUP:
        slider.dragging = False
    elif event.type == pygame.MOUSEMOTION and slider.dragging:
        slider.update(event.pos[0])


# Cargar - Sprites(Estaticos)
class SpriteStatic(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite):
        super().__init__()
        self.image_normal = pygame.transform.scale(pygame.image.load(sprite), (width, height))
        self.image = self.image_normal
        self.rect = self.image.get_rect(center=(x, y))


# Cambio - Tamaño de Pantalla
def cambiar_resolucion(NEW_WIDTH, NEW_HEIGHT, ORG_BACK):
    global pantalla, ANCHO, ALTO, fondo

    ANCHO, ALTO = NEW_WIDTH, NEW_HEIGHT
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
    fondo = pygame.transform.scale(ORG_BACK, (ANCHO, ALTO))




#Funciones - Niveles
def StartGame():
    global pantalla, nombre_usuario, VIDAS, SCORE

    print("Iniciando...\n")
    LoadingScreenGame(pantalla)

    fondo_original = pygame.image.load("IMAGENES/quimica.png")
    background = RESIZE_LOAD(1280, 720, fondo_original)

    print("The Game Starts :D!")
    
    jugador_img1 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento1.png"), (80, 80))
    jugador_img2 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento2.png"), (80, 80))
    jugador_img3 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento3.png"), (80, 80))
    jugador_img4 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento4.png"), (80, 80))
    jugador_img5 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento5.png"), (80, 80))
    jugador_img6 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento6.png"), (80, 80))
    jugador_img7 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento7.png"), (80, 80))
    jugador_img8 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento8.png"), (80, 80))

    imagenes_mov = [
        jugador_img1, jugador_img2, jugador_img3, jugador_img4,
        jugador_img5, jugador_img6, jugador_img7, jugador_img8
    ]

    # Imágenes jugador caminando izquierda
    jugador_inv1 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso1.png"), (80, 80))
    jugador_inv2 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso2.png"), (80, 80))
    jugador_inv3 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso3.png"), (80, 80))
    jugador_inv4 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso4.png"), (80, 80))
    jugador_inv5 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso5.png"), (80, 80))
    jugador_inv6 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso6.png"), (80, 80))
    jugador_inv7 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso7.png"), (80, 80))
    jugador_inv8 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso8.png"), (80, 80))

    imagenes_mov_inv = [
        jugador_inv1, jugador_inv2, jugador_inv3, jugador_inv4,
        jugador_inv5, jugador_inv6, jugador_inv7, jugador_inv8
    ]

    # Imágenes de salto y muerte
    salto_izquierdo = pygame.transform.scale(pygame.image.load("IMAGENES/PLAYERJUMP.png"), (80, 80))
    salto_derecho = pygame.transform.scale(pygame.image.load("IMAGENES/PLAYERJUMPR.png"), (80, 80))
    jugadordead = pygame.transform.scale(pygame.image.load("IMAGENES/PLAYERDEAD.png"), (100, 100))

    class Jugador(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()

            self.imagenes = imagenes_mov
            self.indice = 0
            self.contador = 0
            self.velocidad_anim = 6

            self.imagenes_inv = imagenes_mov_inv
            self.indice_inv = 0
            self.contador_inv = 0
            self.velocidad_anim_inv = 6

            self.image = self.imagenes[0]
            self.rect = self.image.get_rect(topleft=(x, y))

            self.vel_y = 0
            self.en_suelo = False
            self.direccion = "derecha"
            self.game_over = False  

        def animar_derecha(self):
            self.contador += 1
            if self.contador >= self.velocidad_anim:
                self.contador = 0
                self.indice = (self.indice + 1) % len(self.imagenes)
                self.image = self.imagenes[self.indice]

        def animar_izquierda(self):
            self.contador_inv += 1
            if self.contador_inv >= self.velocidad_anim_inv:
                self.contador_inv = 0
                self.indice_inv = (self.indice_inv + 1) % len(self.imagenes_inv)
                self.image = self.imagenes_inv[self.indice_inv]

        def update(self, plataformas, lava):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
                self.direccion = "derecha"
                if self.en_suelo:
                    self.animar_derecha()
            elif keys[pygame.K_LEFT]:
                self.rect.x -= 5
                self.direccion = "izquierda"
                if self.en_suelo:
                    self.animar_izquierda()
            else:
                if self.en_suelo:
                    self.indice = 0
                    self.indice_inv = 0
                    if self.direccion == "derecha":
                        self.image = self.imagenes[0]
                    else:
                        self.image = self.imagenes_inv[0]

            if keys[pygame.K_UP] and self.en_suelo:
                self.vel_y = -15
                self.en_suelo = False

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            self.rect.y += self.vel_y

            if not self.en_suelo:
                if self.direccion == "derecha":
                    self.image = salto_derecho
                else:
                    self.image = salto_izquierdo

            self.en_suelo = False
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.en_suelo = True
                    elif self.vel_y < 0:
                        self.rect.top = p.rect.bottom
                        self.vel_y = 0

            if self.rect.top > ALTO:
                self.morir()

            for l in lava:
                if self.rect.colliderect(l.rect):
                    self.morir()

        def morir(self):
            global VIDAS, SCORE
            VIDAS -= 1
            SCORE -= 10

            if VIDAS > 0:
                mostrar_mensaje(f"Te quedan {VIDAS} vidas")
                self.rect.topleft = (100, ALTO - 120)
                self.vel_y = 0
            else:
                mostrar_mensaje("Sin vidas")
                animacion_muerte_nivel1()
                self.game_over = True  # Sale al menu

    class Plataforma(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.image = pygame.Surface((w, h))
            self.image.set_alpha(350)
            self.image.fill(GRIS)
            self.rect = self.image.get_rect(topleft=(x, y))
    
    class Meta(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.image = pygame.Surface((w, h))
            self.image.set_alpha(50)
            self.image.fill(VERDE)
            self.rect = self.image.get_rect(topleft=(x, y))
        
    class Lava(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.image = pygame.Surface((w, h))
            self.image.set_alpha(50)
            self.image.fill(ROJO)
            self.rect = self.image.get_rect(topleft=(x, y))


    # Animación de muerte nivel 1 (jugador cayendo)
    def animacion_muerte_nivel1():
        y = -200
        vel = 0
        while y < ALTO + 200:
            pantalla.blit(background, (0, 0))
            vel += 1
            y += vel
            pantalla.blit(jugadordead, (ANCHO // 2 - 50, y))
            pygame.display.flip()
            pygame.time.delay(30)

    jugador = Jugador(100, ALTO - 120)
    
    plataformas = pygame.sprite.Group(
        Plataforma(0, ALTO - 40, ANCHO, 40),
        Plataforma(130, ALTO - 100, 120, 15),
        Plataforma(280, ALTO - 220, 150, 15),
        Plataforma(565, ALTO - 270, 150, 15),
        Plataforma(810, ALTO - 290, 220, 15),
        Plataforma(450, ALTO - 360, 160, 15),
        Plataforma(800, ALTO - 550, 180, 15),
        Plataforma(0, ALTO - 275, 190, 15),
        Plataforma(230, ALTO - 360, 120, 15),
        Plataforma(540, ALTO - 460, 180, 15),
        Plataforma(0, ALTO - 275, 190, 15)
    )
    
    lava = pygame.sprite.Group(
        Lava(290, ALTO - 180, 130, 250),
        Lava(430, ALTO - 75, 530, 50)
    )
    
    meta = Meta(ANCHO - 416, 98, 64, 75)
    grupo_meta = pygame.sprite.Group(meta)
    
    boton_rect = pygame.Rect(ANCHO - 160, 20, 140, 40)
    fuente_boton = pygame.font.SysFont("Arial", 24, bold=True)

    def mostrar_mensaje(texto):
        fuente_local = pygame.font.SysFont("Arial", 48, bold=True)
        render = fuente_local.render(texto, True, BLANCO)
        pantalla.blit(
            render,
            (ANCHO // 2 - render.get_width() // 2,
             ALTO // 2 - render.get_height() // 2)
        )
        pygame.display.flip()
        pygame.time.wait(2000)
    
    running_game = True
    clock = pygame.time.Clock()

    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    print("Menú de ajustes")
        
        jugador.update(plataformas, lava)

        # si el jugador se quedó sin vidas se sale al menú
        if jugador.game_over:
            RESTORE_SIZE()
            VIDAS = 10
            return
        
        if pygame.sprite.spritecollideany(jugador, grupo_meta):
            mostrar_mensaje("Nivel completado")
            SCORE += 50
            pygame.time.wait(800)
            Nivel2()
            return
        
        pantalla.blit(background, (0, 0))
        info = fuente.render(f"Jugador: {nombre_usuario}", True, BLANCO)
        pantalla.blit(info, (20, 20))
        vidas_text = fuente.render(f"Vidas: {VIDAS}", True, BLANCO)
        pantalla.blit(vidas_text, (20, 60))

        plataformas.draw(pantalla)
        lava.draw(pantalla)
        grupo_meta.draw(pantalla)
        pantalla.blit(jugador.image, jugador.rect)
        
        pygame.draw.rect(pantalla, (50, 50, 200), boton_rect)
        texto_boton = fuente_boton.render("AJUSTES", True, BLANCO)
        pantalla.blit(texto_boton, (boton_rect.x + 15, boton_rect.y + 8))
        
        pygame.display.flip()
        clock.tick(FPSG)
    
    RESTORE_SIZE()

def return_to_menu_after_level2():
    RESTORE_SIZE()
    pygame.time.delay(500)
    return

def Nivel2():
    global pantalla, ANCHO, ALTO, VIDAS, SCORE

    ANCHO_2, ALTO_2 = 1280, 720
    ANCHO, ALTO = ANCHO_2, ALTO_2
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("facultad_ingenieria")

    fondo_original = pygame.image.load("IMAGENES/facultad_ingenieria.png")
    fondo = pygame.transform.scale(fondo_original, (ANCHO, ALTO))

    jugador_img1 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento1.png"), (80, 80))
    jugador_img2 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento2.png"), (80, 80))
    jugador_img3 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento3.png"), (80, 80))
    jugador_img4 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento4.png"), (80, 80))
    jugador_img5 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento5.png"), (80, 80))
    jugador_img6 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento6.png"), (80, 80))
    jugador_img7 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento7.png"), (80, 80))
    jugador_img8 = pygame.transform.scale(pygame.image.load("IMAGENES/movimiento8.png"), (80, 80))

    imagenes_mov = [
        jugador_img1, jugador_img2, jugador_img3, jugador_img4,
        jugador_img5, jugador_img6, jugador_img7, jugador_img8
    ]

    jugador_inv1 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso1.png"), (80, 80))
    jugador_inv2 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso2.png"), (80, 80))
    jugador_inv3 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso3.png"), (80, 80))
    jugador_inv4 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso4.png"), (80, 80))
    jugador_inv5 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso5.png"), (80, 80))
    jugador_inv6 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso6.png"), (80, 80))
    jugador_inv7 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso7.png"), (80, 80))
    jugador_inv8 = pygame.transform.scale(pygame.image.load("IMAGENES/caminadoinverso8.png"), (80, 80))

    imagenes_mov_inv = [
        jugador_inv1, jugador_inv2, jugador_inv3, jugador_inv4,
        jugador_inv5, jugador_inv6, jugador_inv7, jugador_inv8
    ]

    salto_izquierdo = pygame.transform.scale(pygame.image.load("IMAGENES/PLAYERJUMP.png"), (80, 80))
    salto_derecho = pygame.transform.scale(pygame.image.load("IMAGENES/PLAYERJUMPR.png"), (80, 80))
    jugadordead = pygame.transform.scale(pygame.image.load("IMAGENES/PLAYERDEAD.png"), (100, 100))

    MARRON = (160, 90, 40)
    VERDE = (0, 255, 0)
    ROJO = (200, 50, 50)
    BLANCO = (255, 255, 255)
    GRIS = (128, 128, 128)
    NARANJA = (208, 73, 28)

    try:
        VIDAS
    except NameError:
        VIDAS
    fuente_vidas = pygame.font.SysFont("Arial", 40, bold=True)

    def animacion_muerte_final():
        y = -200
        vel = 0
        while y < ALTO + 200:
            pantalla.blit(fondo, (0, 0))
            vel += 1
            y += vel
            pantalla.blit(jugadordead, (ANCHO // 2 - 50, y))
            pygame.display.flip()
            pygame.time.delay(30)

    class Jugador2(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.imagenes = imagenes_mov
            self.indice = 0
            self.contador = 0
            self.velocidad_anim = 6
            self.imagenes_inv = imagenes_mov_inv
            self.indice_inv = 0
            self.contador_inv = 0
            self.velocidad_anim_inv = 6
            self.image = self.imagenes[0]
            self.rect = self.image.get_rect(topleft=(x, y))
            self.vel_y = 0
            self.en_suelo = False
            self.direccion = "derecha"

        def animar_derecha(self):
            self.contador += 1
            if self.contador >= self.velocidad_anim:
                self.contador = 0
                self.indice = (self.indice + 1) % len(self.imagenes)
                self.image = self.imagenes[self.indice]

        def animar_izquierda(self):
            self.contador_inv += 1
            if self.contador_inv >= self.velocidad_anim_inv:
                self.contador_inv = 0
                self.indice_inv = (self.indice_inv + 1) % len(self.imagenes_inv)
                self.image = self.imagenes_inv[self.indice_inv]

        def update(self, plataformas, lava):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
                self.direccion = "derecha"
                if self.en_suelo:
                    self.animar_derecha()
            elif keys[pygame.K_LEFT]:
                self.rect.x -= 5
                self.direccion = "izquierda"
                if self.en_suelo:
                    self.animar_izquierda()
            else:
                if self.en_suelo:
                    self.indice = 0
                    self.indice_inv = 0
                    self.image = self.imagenes[0] if self.direccion == "derecha" else self.imagenes_inv[0]

            if keys[pygame.K_UP] and self.en_suelo:
                self.vel_y = -15
                self.en_suelo = False

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            self.rect.y += self.vel_y

            if not self.en_suelo:
                self.image = salto_derecho if self.direccion == "derecha" else salto_izquierdo

            self.en_suelo = False
            for p in plataformas:
                if self.rect.colliderect(p.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.en_suelo = True
                    elif self.vel_y < 0:
                        self.rect.top = p.rect.bottom
                        self.vel_y = 0

            if self.rect.top > ALTO:
                self.morir()

            for l in lava:
                if self.rect.colliderect(l.rect):
                    self.morir()

        def morir(self):
            nonlocal_vidas_decrement()

    def nonlocal_vidas_decrement():
    
        global VIDAS, SCORE
        nonlocal ejecutando
        VIDAS -= 1
        SCORE -= 10
    
        if VIDAS > 0:
            mostrar_mensaje_nivel2(f"Te quedan {VIDAS} vidas")
            jugador2.rect.topleft = (100, ALTO - 120)
            jugador2.vel_y = 0
        else:
            animacion_muerte_final()
            return_to_menu_after_level2()
            ejecutando = False
            return
    
    class Plataforma2(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.image = pygame.Surface((w, h))
            self.image.set_alpha(350)
            self.image.fill(NARANJA)
            self.rect = self.image.get_rect(topleft=(x, y))

    class Meta2(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.image = pygame.Surface((w, h))
            self.image.set_alpha(50)
            self.image.fill(VERDE)
            self.rect = self.image.get_rect(topleft=(x, y))

    class Lava2(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
            super().__init__()
            self.image = pygame.Surface((w, h))
            self.image.set_alpha(50)
            self.image.fill(ROJO)
            self.rect = self.image.get_rect(topleft=(x, y))

    jugador2 = Jugador2(100, ALTO - 120)

    plataformas = pygame.sprite.Group(
        Plataforma2(0, ALTO - 40, ANCHO, 40),
        Plataforma2(370, ALTO - 90, 100, 20),
        Plataforma2(490, ALTO - 150, 80, 20),
        Plataforma2(630, ALTO - 185, 80, 20),
        Plataforma2(750, ALTO - 280, 80, 20),
        Plataforma2(880, ALTO - 360, 100, 20),
        Plataforma2(300, ALTO - 250, 200, 20),
        Plataforma2(390, ALTO - 460, 270, 20),
        Plataforma2(870, ALTO - 510, 80, 20),
        Plataforma2(1050, ALTO - 430, 90, 20),
        Plataforma2(620, ALTO - 530, 150, 20),
        Plataforma2(470, ALTO - 530, 80, 20),
        Plataforma2(280, ALTO - 510, 100, 20)
    )

    meta = Meta2(120, 240, 120, 20)
    grupo_meta2 = pygame.sprite.Group(meta)

    lava = pygame.sprite.Group(
        Lava2(ANCHO - 800, ALTO - 60, 1000, 40),
        Lava2(ANCHO - 890, ALTO - 500, 200, 40),
        Lava2(ANCHO - 1250, ALTO - 400, 200, 160)
    )

    boton_rect = pygame.Rect(ANCHO - 160, 20, 140, 40)
    fuente_boton = pygame.font.SysFont("Arial", 24, bold=True)

    def mostrar_mensaje_nivel2(texto):
        fuente_local = pygame.font.SysFont("Arial", 48, bold=True)
        render = fuente_local.render(texto, True, BLANCO)
        pantalla.blit(
            render,
            (ANCHO // 2 - render.get_width() // 2,
             ALTO // 2 - render.get_height() // 2)
        )
        pygame.display.flip()
        pygame.time.wait(2000)


    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                RESTORE_SIZE()
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    print("Menú de ajustes")

        jugador2.update(plataformas, lava)

        if pygame.sprite.spritecollideany(jugador2, grupo_meta2):
            mostrar_mensaje_nivel2("Nivel completado")
            PantallaFinal()
            return

        pantalla.blit(fondo, (0, 0))
        plataformas.draw(pantalla)
        lava.draw(pantalla)
        grupo_meta2.draw(pantalla)
        pantalla.blit(jugador2.image, jugador2.rect)
        info = fuente_vidas.render(f"Jugador: {nombre_usuario}", True, BLANCO)
        pantalla.blit(info, (20, 70))

        texto_v = fuente_vidas.render(f"Vidas: {VIDAS}", True, BLANCO)
        pantalla.blit(texto_v, (20, 20))

        pygame.draw.rect(pantalla, (50, 50, 200), boton_rect)
        texto_boton = fuente_boton.render("AJUSTES", True, BLANCO)
        pantalla.blit(texto_boton, (boton_rect.x + 15, boton_rect.y + 8))

        pygame.display.flip()
        clock.tick(60)

    RESTORE_SIZE()
    VIDAS = 10
    return

def PantallaFinal():
    global pantalla, ANCHO, ALTO, SCORE, VIDAS
    ANCHO, ALTO = 800, 550
    pantalla = pygame.display.set_mode((ANCHO, ALTO))

    imagen_final = pygame.image.load("IMAGENES/FINAL.png")
    imagen_final = pygame.transform.scale(imagen_final, (ANCHO, ALTO))
    
    db.collection("Juego - PC").document(nombre_usuario).update({
            "Vidas": VIDAS,
            "Puntaje" : SCORE
    })
    
    def Exit():
        nonlocal mostrando  
        print("Regreso al Menu principal")
        mostrando = False
    
    BotonFINAL = Button(
        x=ANCHO//2 ,
        y=ALTO//2 + 25,
        width=700,
        height= 450,
        spritenormal="SPRITES/Button/BOTONVMENU.png",
        spritehover="SPRITES/Button/BOTONVMENU.png",
        action= Exit
    )

    PuntajeFinal = Texto(
        texto= f"PUNTUACION: {SCORE}",
        color= VERDE,
        size= 30,
        fuente="FUENTES/MONO/Mono.ttf",
        x=ANCHO // 2 - 200,
        y=ALTO // 2 + 30,
    )
    
    VidasFinal = Texto(
        texto= f"VIDAS: {VIDAS}",
        color= VERDE,
        size= 30,
        fuente="FUENTES/MONO/Mono.ttf",
        x=ANCHO // 2 - 200 ,
        y=ALTO // 2 + 60,
    )


    LSCREENSprites = pygame.sprite.Group(BotonFINAL)
    

    mostrando = True
    clock = pygame.time.Clock()

    while mostrando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mostrando = False
            for boton in LSCREENSprites:
                boton.handle_event(event)
        
        pantalla.blit(imagen_final, (0, 0))
        
        PuntajeFinal.draw(pantalla)   
        VidasFinal.draw(pantalla)        
        
        LSCREENSprites.update()
        LSCREENSprites.draw(pantalla)
        
        pygame.display.flip()
        clock.tick(60)
        
    
    RESTORE_SIZE()
    
def QuitGame():
    print("Saliendo del juego...")
    pygame.quit()
    raise SystemExit

def ConfigG():
    print("Espere un momento...\n")
    LoadingScreenNormal(pantalla)
    print("Pantalla de Configuracion")
    

    background = pygame.image.load("IMAGENES/CONFIG.png")
    background = pygame.transform.scale(background, (ANCHO, ALTO))
    
    def NoAction():
        pass
    
    def Exit():
        global nombre_usuario
        nonlocal running_game  
        db.collection("Juego - PC").document(nombre_usuario).update({
            "Volumen": ActualSVOL
        })
        print("Regreso al Menu principal")
        running_game = False       
                
    SliderVOL = Slider(
        x=ANCHO // 2 - 150,
        y=ALTO // 2 - 80,
        height=HSLIDER,
        width=WSLIDER,
        minvalue=SRANGEI,
        maxvalue=SRANGEF,
        spritethumb="SPRITES/Button/PSLIDER.png",
        spritebar="SPRITES/Button/SLIDER.png",
    )
    
    ButtonExit = Button(
        x=ANCHO//2 - 280,
        y=ALTO//2 + 198,
        width=140,
        height=70,
        spritenormal="SPRITES/Button/BotonExitF.png",
        spritehover="SPRITES/Button/BotonExitFHover.png",
        action=Exit
    )
    
    SoundSp = SpriteStatic(
        x=ANCHO // 2 - 220,
        y=ALTO // 2 - 50,
        width=100,
        height=100,
        sprite="SPRITES/Button/SOUND.png"
    )
    
    Sonido = Texto(
        texto="VOLUMEN",
        color=VERDE,
        size=25,
        fuente="FUENTES/MONO/Mono.ttf",
        x=ANCHO // 2 - 280,
        y=ALTO // 2 - 15,
    )

    ValorVOL = Texto(
        texto="0%",
        color=VERDE,
        size=25,
        fuente="FUENTES/MONO/Mono.ttf",
        x=ANCHO // 2 + 250,
        y=ALTO // 2 - 65,
    )

    PlayerSkin = Texto(
        texto="Skin",
        color=VERDE,
        size=25,
        fuente="FUENTES/MONO/Mono.ttf",
        x=ANCHO // 2 + 30,
        y=ALTO // 2 + 210,
    )

    Skin1 = Button(
        x=ANCHO//2 + 70,
        y=ALTO//2 + 90,
        width=220,
        height=240,
        spritenormal="SPRITES/Player/PLAYER1/OTHERS/PLAYER1SELECA.png",
        spritehover="SPRITES/Player/PLAYER1/OTHERS/PLAYER1SELEC.png",
        action=NoAction
    )

    LastSVOL = SliderVOL.get_value()
        
    ConfigButtonsprites = pygame.sprite.Group(ButtonExit)
    ConfigSprites = pygame.sprite.Group(SoundSp, Skin1)
    ConfigSliders = [SliderVOL]
    
    SOUND_ON = pygame.transform.scale(
        pygame.image.load("SPRITES/Button/SOUND.png"), 
        (100, 100)
    )

    SOUND_OFF = pygame.transform.scale(
        pygame.image.load("SPRITES/Button/SOUNDNO.png"),
        (100, 100)
    )

    running_game = True
    clock = pygame.time.Clock()

    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            for boton in ConfigButtonsprites:
                boton.handle_event(event)
            for slider in ConfigSliders:
                gestionar_slider(event, slider)
            
        pantalla.blit(background, (0, 0))
        
        ConfigButtonsprites.update()
        ConfigButtonsprites.draw(pantalla)
        
        ConfigSprites.update()
        ConfigSprites.draw(pantalla)
        
        for slider in ConfigSliders:
            slider.update(pygame.mouse.get_pos()[0])
            slider.draw(pantalla)
        
        ActualSVOL = SliderVOL.get_value()  
        
        if ActualSVOL != LastSVOL:
            ValorVOL.set_text(f"{ActualSVOL} %")
            LastSVOL = ActualSVOL
        
        if ActualSVOL == 0:
            SoundSp.image = SOUND_OFF
        else:
            SoundSp.image = SOUND_ON
        
        Sonido.draw(pantalla)
        ValorVOL.draw(pantalla)
        PlayerSkin.draw(pantalla)

        Information = fuente.render(f"Jugador: {nombre_usuario} ", True, BLANCO)
        pantalla.blit(Information, (20, 20))
        
        pygame.display.flip()
        clock.tick(FPS)




# Valores - Botones
ButtonStart = Button(
    x=ANCHO // 2 - 20,
    y=ALTO // 2 - 1,
    width=230,
    height=70,
    spritenormal="SPRITES/Button/BotonPlayF.png",
    spritehover="SPRITES/Button/BotonPlayFHover.png",
    action=StartGame
)

ButtonEnd = Button(
    x=ANCHO // 2 - 25,
    y=ALTO // 2 + 170,
    width=165,
    height=66,
    spritenormal="SPRITES/Button/BotonSalirF.png",
    spritehover="SPRITES/Button/BotonSalirFHover.png",
    action=QuitGame
)

ButtonConfig = Button(
    x=ANCHO // 2 - 15,
    y=ALTO // 2 + 87,
    width=320,
    height=80,
    spritenormal="SPRITES/Button/BotonConfigF.png",
    spritehover="SPRITES/Button/BotonConfigFHover.png",
    action=ConfigG
)


# Pantallas de Carga
def LoadingScreenNormal(pantalla):
    ANCHO, ALTO = pantalla.get_size()
    clock = pygame.time.Clock()
    

    for alpha in range(0, 180, 8):
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.fill(NEGRO)
        overlay.set_alpha(alpha)
        pantalla.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(30)

    pantalla.fill(NEGRO)
    texto_carga = fuente_carga.render("CARGANDO...", True, BLANCO)
    pantalla.blit(texto_carga, (ANCHO // 2 - texto_carga.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    time.sleep(3)

def LoadingScreenGame(pantalla):
    ANCHO, ALTO = pantalla.get_size()
    clock = pygame.time.Clock()
    fuente_carga = pygame.font.Font("FUENTES/ORBITRON/ORBitron.ttf", 30)

    for alpha in range(0, 180, 8):
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.fill(NEGRO)
        overlay.set_alpha(alpha)
        pantalla.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(30)

    pantalla.fill(NEGRO)
    texto_carga = fuente_carga.render("CARGANDO...", True, BLANCO)
    pantalla.blit(texto_carga, (ANCHO // 2 - texto_carga.get_width() // 2, ALTO // 2 - 30))
    texto2_carga = fuente_carga.render("Nivel 1", True, BLANCO)
    pantalla.blit(texto2_carga, (ANCHO // 2 - texto2_carga.get_width() // 2, ALTO // 2 + 30))
    pygame.display.flip()
    time.sleep(3)



# Agrupo los sprites en "MenuButtonSprites"
MenusButtonprites = pygame.sprite.Group(ButtonStart, ButtonEnd, ButtonConfig)


# Bucle Principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for boton in MenusButtonprites:
            boton.handle_event(event)

    MenusButtonprites.update()
    pantalla.blit(background, (0, 0))
    MenusButtonprites.draw(pantalla)

    superficie_texto = fuente.render(texto, True, (255, 255, 255))
    rect_texto = superficie_texto.get_rect(topright=(ANCHO - 20, 40))
    pantalla.blit(superficie_texto, rect_texto)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()