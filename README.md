# Proyecto-Programacion---Computadores-


## DESCRIPCIÓN DEL JUEGO

Vive la Aventura UNAL (ArcUnal) es un videojuego de plataformas arcade que toma como referencia la Universidad Nacimiento de Colombia y su campus,
además se intenta representar los niveles como edificios de la misma, y al personaje como uno de sus estudiantes, aparte de ello  se usa  una modalidad
inspirada en el juego muy conocido llamado “Mario Bross” .

### 1. Información general
Antes de iniciar, se debe descomprimir la carpeta del archivo ZIP en archivos y guardarla, ya que trabajar únicamente dentro de la carpeta descomprimida. 

ArcUnal fue desarrollado en python, utilizando:
Tkinter → Pantalla de recolección de datos. 
Pygame → Menú y niveles en 2D. 
Firebase Firestore → Almacenamiento del nombre y vidas del jugador,volumen, y puntaje. 
Toda la ejecución, desarrollo y administración del proyecto se realiza desde Visual Studio Code (VS Code). 

 ### 2. Requisitos del Sistema 
Sistema Operativo: 
Windows, macOS o Linux 
Software necesario ::
Python 3.8 o superior 
Visual Studio Code 
Extensión Python para Visual Studio Code 
Librerías necesarias :
pygame 
firebase-admin 
tkinter (incluida en la mayoría de instalaciones) 
Conectividad:
Se requiere conexión a Internet para conectarse a Firebase. 

### 3. Instalación y Preparación del juego

3.1 Instalar Visual Studio Code : 
Instalarlo desde la web oficial de VS code o desde la tienda de aplicaciones.

3.2 Instalar Python:
Abrir la aplicación Visual Studio Code(VSC)
Dirigirse al panel lateral izquierdo, buscar la opción Extensions > Python > Install
Abrir Microsoft Store > Buscar Python > Python 3.13(o la más nueva) > Obtener
Abrir Visual Studio Code nuevamente > Panel Superior > File(Archivo) > New file(Nuevo archivo) > Python File

3.3 Abrir el proyecto en Visual Studio Code:
Abrir VS Code 
Selecionar File: Open Folder
Escoger la carpeta original descomprimida desde archivos 
Seleccionar el archivo del código con la terminal “.py”

3.4 Instalar dependencias desde el terminal integrado:
3.4.1 Instalar pygame 
Panel Superior > Terminal > New Terminal > Escribir “pip install pygame”
Para comprobar: Escribir en el Editor 
“import pygame
print(pygame.__version__)”
Esquina Superior Derecha > Run file > Terminal > “2.6.1”

3.4.1 Instalar Firebase
Panel Superior > Terminal > New Terminal > Escribir “pip install firebase-admin”
Para comprobar: Escribir “pip show firebase-admin” > aparecera algo asi:
			    “Name: firebase_admin
    Versión: 7.1.0
    Summary: Firebase Admin Python SDK
    Home-page: https://firebase.google.com/docs/admin/setup/
    Author: Firebase”

3.5 Especificaciones respecto a firebase:
EL juego ya está completamente vinculado a la cuenta principal en la base de datos de firebase y ya se cuenta con la llave 
de acceso en la misma carpeta, por lo que no se deberá modificar nada en el código.




### 4. Ejecución del juego en Visual Studio Code

4.1 Desde la interfaz gráfica:
Se selecciona el botón ejecución (Run) que se encuentra en la parte superior derecha del editor de código, y se da click derecho en la opción Run python file.

4.2 Proceso de ejecución:
Se abre la pantalla tkinter en la cuál se pide el registro de usuario del jugador.
Al validar el nombre se guardan los datos en la base de datos (firebase).
Se abre el menú principal desarrollado con pygame.



### 5. Pantalla de recolección de datos: Tkinter

5.1 Funcionamiento: 
Campo con subtítulo : Nombre
Botón : Continuar

5.2 Validación: 
Si el campo está vacío el programa no continua e imprime incorrecto en la terminal.
Si el nombre es válido se crea o actualiza un documento en Firebase con:
Jugador
Puntaje
Volumen
Vidas
Luego la ventana se cierra y carga el juego.


### 6. Menú principal : Pygame
Incluye:
Jugar : Inicia el nivel 1
Configuración:
 Volumen:
 Volumen 0% → icono de sonido desactivado. 
 Volumen > 0% → icono de sonido activo. 
  Vista de Skin:
Vista previa de la apariencia del jugador. 

Salir: Cierra el juego
En la pantalla aparece: 
Nombre del jugador
Vidas del jugador


### 7. Nivel 1: Edificio de  Química
7.1 Objetivo 
 Superar el escenario evitando lava roja y caídas, y llegar a la meta verde. 
7.2 Controles 
Flecha derecha → mover a la derecha 
Flecha izquierda → mover a la izquierda 
Flecha arriba → saltar (solo si está en el suelo) 
7.3 Mecánicas 
3 vidas iniciales. 
Se pierde una vida al: 
caer fuera del las plataformas 
tocar lava 
Se muestra: 
Te quedan X vidas 
Si las vidas llegan a cero: 
Animación de muerte 
Regreso al menú principal 
7.4 Final del nivel 
Al tocar la zona verde: 
Se muestra “Nivel completado” 
Se carga Nivel 2 



### 8. Nivel 2 : Edificio de Ingeniería

8.1 Objetivo 
Superar el segundo escenario con plataformas y lava. 

8.2 Mecánicas
 Se mantiene el sistema de vidas global, por lo que si en el nivel 1 se perdió                    una vida, en el segundo se continuará con una vida menos.
Se mantienen los mismos controles.
Sin vidas: animación de muerte y retorno al menú. 
8.3 Final del juego 
Al llegar a la meta: 
Se muestra “Nivel completado” 
Se abre la Pantalla Final siguiendo con la temática principal.


### 9. Guardado
Al salir de la configuración se guardan en Firestore:
 Jugador 
Puntaje
Volumen
Vidas del jugador


### 10. Salir del juego
Opciones: 
 Botón Salir del menú principal. 
Cerrar la ventana de Pygame con el botón X. 
Ambos métodos ejecutan: pygame.quit()


### 11. Posibles problemas
Tkinter no cierra: El campo de nombre está vacío. 
Error de importación de pygame / firebase_admin 
Las librerías no están instaladas en el intérprete seleccionado:
 Solución: usar Python: Select Interpreter y reinstalar. 
Python no encuentra firebase_key.json: 
 Revisar ruta: FIREBASE/firebase_key.json 
Asegurarse de que la ventana Tkinter ya se haya cerrado. 

# Mockups utilizados

## Este es el mockup del menu del juego

![Imagen de WhatsApp 2025-10-13 a las 23 51 22_f843539d](https://github.com/user-attachments/assets/91b0d946-74b7-4041-91f4-23106f5b81f9)



## Este es el mapa del juego


<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/6ac008e1-f8fd-4895-a9e1-5322d622cf0b" />


<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/b7ba1b09-e083-4265-a23f-2ac8346a4f37" />




## Este es el personaje del juego

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/ef0e0588-cdf2-44bd-99d7-18d21cb3f463" />





## Este es el mockup de pantalla de Configuracion
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/9ebdde19-5e2e-4a8a-a8a7-dc641aa0c5d0" />




## Este es el mockup del Final del Juego

<img width="1088" height="960" alt="image" src="https://github.com/user-attachments/assets/b7c6b400-2642-41ae-8dca-fb8773215472" />



