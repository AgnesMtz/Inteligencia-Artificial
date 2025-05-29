import pygame
import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego IA: Esquiva Balas")

# Colores básicos
COLOR_FONDO = (0, 0, 0)
COLOR_TEXTO = (255, 255, 255)

# Carga de recursos gráficos
frames_personaje = [
    pygame.image.load('assets/sprites/sage.png'),
    pygame.image.load('assets/sprites/sage.png'),
    pygame.image.load('assets/sprites/sage.png'),
    pygame.image.load('assets/sprites/sage.png')
]
img_bala = pygame.image.load('assets/sprites/bola1.png')
img_fondo = pygame.transform.scale(pygame.image.load('assets/game/fondo2.png'), (ANCHO, ALTO))
img_nave = pygame.image.load('assets/game/ufo.png')

# Rectángulos
rect_jugador = pygame.Rect(50, ALTO - 100, 32, 48)
rect_bala_h = pygame.Rect(ANCHO - 50, ALTO - 90, 16, 16)
rect_bala_v = pygame.Rect(50, 0, 16, 16)
rect_nave = pygame.Rect(ANCHO - 100, ALTO - 100, 64, 64)
rect_nave_sup = pygame.Rect(20, 0, 64, 64)

# Variables animación
indice_frame = 0
contador_frames = 0
VEL_FRAME = 10

# Juego: estado
en_salto = False
salto_vel = 15
gravedad = 1
en_suelo = True
adelante = False
retorno = False
posicion_inicial = True

# Balas
vel_bala_h = -10
vel_bala_v = 2
disparo_h = False
disparo_v = False

# Fondo
fondo_x1 = 0
fondo_x2 = ANCHO

# IA
modo_auto = False
datos = []
modelo_salto = None
modelo_adelante = None

# Fuente
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
pausa = False

# Funciones de juego
def disparo_horizontal():
    global disparo_h, vel_bala_h
    if not disparo_h:
        vel_bala_h = random.randint(-4, -3)
        disparo_h = True

def disparo_vertical():
    global disparo_v
    if not disparo_v:
        disparo_v = True

def reiniciar_bala_h():
    global disparo_h
    rect_bala_h.x = ANCHO - 50
    disparo_h = False

def reiniciar_bala_v():
    global disparo_v
    rect_bala_v.x, rect_bala_v.y = 50, 0
    disparo_v = False

def actualizar_fondo():
    global fondo_x1, fondo_x2
    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -ANCHO:
        fondo_x1 = ANCHO
    if fondo_x2 <= -ANCHO:
        fondo_x2 = ANCHO
    ventana.blit(img_fondo, (fondo_x1, 0))
    ventana.blit(img_fondo, (fondo_x2, 0))

def procesar_salto():
    global en_salto, salto_vel, en_suelo
    if en_salto:
        rect_jugador.y -= salto_vel
        salto_vel -= gravedad
        if rect_jugador.y >= ALTO - 100:
            rect_jugador.y = ALTO - 100
            en_salto = False
            salto_vel = 15
            en_suelo = True

def mover_adelante():
    global adelante, retorno, posicion_inicial
    if adelante and not retorno:
        rect_jugador.x += 9
        if rect_jugador.x >= ANCHO - 670:
            rect_jugador.x = ANCHO - 670
            retorno = True
    elif retorno:
        rect_jugador.x -= 9
        if rect_jugador.x <= 50:
            rect_jugador.x = 50
            retorno = False
            adelante = False
            posicion_inicial = True
#Guarda los datos Feature 1 y 2 Target 1 y 2
def guardar_dato():
    distancia_h = abs(rect_jugador.x - rect_bala_h.x)
    distancia_v = abs(rect_jugador.y - rect_bala_v.y)
    datos.append((vel_bala_h, distancia_h, int(en_salto), vel_bala_v, distancia_v, int(adelante)))

def entrenar():
    global modelo_salto, modelo_adelante
    if len(datos) < 20:
        print("Datos insuficientes.")
        return
    #Datos para saltar
    Xs = np.array([[v, d] for v, d, _, _, _, _ in datos]) #Velocidad/Distancia
    Ys = np.array([s for _, _, s, _, _, _ in datos])
   #Datos para moverse adelante
    Xm = np.array([[v2, d2] for _, _, _, v2, d2, _ in datos])
    Ym = np.array([m for _, _, _, _, _, m in datos])
    modelo_salto = DecisionTreeClassifier().fit(Xs, Ys) #Arbol salto
    modelo_adelante = DecisionTreeClassifier().fit(Xm, Ym) #Arbol movimiento

#Prediccion para modo automatico
def decision_salto():
    if modelo_salto is None:
        return False
    d = abs(rect_jugador.x - rect_bala_h.x)
    pred = modelo_salto.predict([[vel_bala_h, d]]) #Predición con el arbol
    return pred[0] == 1

def decision_adelante():
    if modelo_adelante is None:
        return False
    d = abs(rect_jugador.y - rect_bala_v.y)
    pred = modelo_adelante.predict([[vel_bala_v, d]])
    return pred[0] == 1
##
def reiniciar_juego():
    global menu_activo, en_salto, en_suelo, adelante, retorno, posicion_inicial
    rect_jugador.x, rect_jugador.y = 50, ALTO - 100
    reiniciar_bala_h()
    reiniciar_bala_v()
    rect_nave.x, rect_nave.y = ANCHO - 100, ALTO - 100
    rect_nave_sup.x, rect_nave_sup.y = 20, 0
    en_salto = False
    en_suelo = True
    adelante = False
    retorno = False
    posicion_inicial = True
    menu_activo = True
    print("Datos recopilados:", datos)
    mostrar_menu()

def mostrar_menu():
    global menu_activo, modo_auto
    ventana.fill(COLOR_FONDO)
    texto = fuente.render("Presiona 'A'=Auto, 'M'=Manual, 'Q'=Salir", True, COLOR_TEXTO)
    ventana.blit(texto, (ANCHO//4, ALTO//2))
    pygame.display.flip()
    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    entrenar()
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    datos.clear()
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    exit()

def actualizar():
    global indice_frame, contador_frames
    actualizar_fondo()
    contador_frames += 1
    if contador_frames >= VEL_FRAME:
        indice_frame = (indice_frame + 1) % len(frames_personaje)
        contador_frames = 0
    ventana.blit(frames_personaje[indice_frame], (rect_jugador.x, rect_jugador.y))
    ventana.blit(img_nave, (rect_nave.x, rect_nave.y))
    ventana.blit(img_nave, (rect_nave_sup.x, rect_nave_sup.y))
    if disparo_h:
        rect_bala_h.x += vel_bala_h
    if rect_bala_h.x < 0:
        reiniciar_bala_h()
    ventana.blit(img_bala, (rect_bala_h.x, rect_bala_h.y))
    if disparo_v:
        rect_bala_v.y += vel_bala_v
    if rect_bala_v.y > ALTO:
        reiniciar_bala_v()
    ventana.blit(img_bala, (rect_bala_v.x, rect_bala_v.y))
    if rect_jugador.colliderect(rect_bala_h) or rect_jugador.colliderect(rect_bala_v):
        reiniciar_juego()

def main():
    global en_salto, en_suelo, adelante, posicion_inicial
    reloj = pygame.time.Clock()
    mostrar_menu()
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo:
                    en_salto = True
                    en_suelo = False
                elif evento.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    adelante = True
                    posicion_inicial = False
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    exit()
        if not pausa:
            if modo_auto:
                if en_suelo and decision_salto():
                    en_salto = True
                    en_suelo = False
                if en_salto:
                    procesar_salto()
                if posicion_inicial and decision_adelante():
                    adelante = True
                    posicion_inicial = False
                if adelante:
                    mover_adelante()
            else:
                if en_salto:
                    procesar_salto()
                if adelante:
                    mover_adelante()
                guardar_dato()
            if not disparo_h:
                disparo_horizontal()
            if not disparo_v:
                disparo_vertical()
            actualizar()
        pygame.display.flip()
        reloj.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
